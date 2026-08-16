"""All HTTP routes for the course app."""

import re
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.auth import (
    create_session_token,
    get_current_user,
    hash_pin,
    verify_pin,
)
from app.config import (
    ALLOWED_IMAGE_EXTS,
    APP_NAME,
    APP_TAGLINE,
    APP_VERSION,
    CASE_STUDY_APP_URL,
    CASE_STUDY_URL,
    MAX_UPLOAD_BYTES,
    SESSION_COOKIE,
    UPLOAD_DIR,
    UPLOAD_URL_PREFIX,
)
from app.curriculum import (
    assignments_by_track,
    assignments_for_module,
    get_assignment,
    get_module,
    list_assignments,
    list_editable_files,
    list_modules,
    list_tracks,
    modules_for_export,
    load_glossary,
    load_schedule,
    load_selection_criteria,
    module_neighbors,
    modules_by_track,
    normalize_track_id,
    read_editable,
    write_editable,
)
from app.database import get_db
from app.models import Candidate, Progress, Role, Score, Submission
from app.services.scoring import (
    candidate_gradebook,
    candidate_totals,
    candidate_track_totals,
    clear_assignment_scores,
    leaderboard,
    submission_status,
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def _ctx(request: Request, db: Session, **extra):
    user = get_current_user(request, db)
    base = {
        "request": request,
        "user": user,
        "app_name": APP_NAME,
        "app_tagline": APP_TAGLINE,
        "app_version": APP_VERSION,
        "case_study_url": CASE_STUDY_URL,
        "case_study_app_url": CASE_STUDY_APP_URL,
    }
    base.update(extra)
    return base


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "home.html",
        _ctx(
            request, db,
            tracks=modules_by_track(),
            assignments=list_assignments()[:6],
            schedule=load_schedule(),
            selection=load_selection_criteria(),
        ),
    )


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, db: Session = Depends(get_db)):
    if get_current_user(request, db):
        return RedirectResponse("/", status_code=303)
    people = (
        db.query(Candidate)
        .filter(Candidate.is_active == True)  # noqa: E712
        .order_by(Candidate.role.desc(), Candidate.name)
        .all()
    )
    return templates.TemplateResponse(
        "login.html",
        _ctx(request, db, people=people, error=None),
    )


@router.post("/login", response_class=HTMLResponse)
async def login_submit(
    request: Request,
    candidate_id: int = Form(...),
    pin: str = Form(...),
    db: Session = Depends(get_db),
):
    people = (
        db.query(Candidate)
        .filter(Candidate.is_active == True)  # noqa: E712
        .order_by(Candidate.name)
        .all()
    )
    cand = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not cand or not verify_pin(pin, cand.pin_hash):
        return templates.TemplateResponse(
            "login.html",
            _ctx(request, db, people=people, error="Invalid PIN"),
            status_code=401,
        )
    token = create_session_token(cand.id, cand.role.value)
    resp = RedirectResponse("/", status_code=303)
    resp.set_cookie(SESSION_COOKIE, token, httponly=True, max_age=12 * 3600)
    return resp


@router.get("/logout")
async def logout():
    resp = RedirectResponse("/login", status_code=303)
    resp.delete_cookie(SESSION_COOKIE)
    return resp


@router.get("/modules", response_class=HTMLResponse)
async def modules_index(request: Request, db: Session = Depends(get_db)):
    track = request.query_params.get("track")
    if track:
        track = normalize_track_id(track)
    return templates.TemplateResponse(
        "modules.html",
        _ctx(
            request,
            db,
            tracks=list_tracks(),
            track_filter=track,
            modules=list_modules(track=track) if track else list_modules(),
            tracks_with_modules=modules_by_track(),
        ),
    )


def _parse_export_ids(request: Request) -> tuple[list[str], str | None]:
    """module_id checkboxes, ids=a,b query, optional track filter."""
    q = request.query_params
    form = getattr(request, "_export_form", None) or {}
    raw: list[str] = []
    if form.get("module_id"):
        val = form.getlist("module_id") if hasattr(form, "getlist") else form.get("module_id")
        if isinstance(val, list):
            raw.extend(val)
        elif val:
            raw.append(val)
    ids_q = q.get("ids") or form.get("ids")
    if ids_q:
        raw.extend(re.split(r"[\s,]+", str(ids_q)))
    track = q.get("track") or form.get("track")
    if track:
        track = normalize_track_id(track)
    seen: set[str] = set()
    ids: list[str] = []
    for item in raw:
        mid = (item or "").strip()
        if mid and mid not in seen:
            seen.add(mid)
            ids.append(mid)
    return ids, track


@router.get("/modules/export", response_class=HTMLResponse)
async def modules_export_picker(request: Request, db: Session = Depends(get_db)):
    track = request.query_params.get("track")
    if track:
        track = normalize_track_id(track)
    ids, _ = _parse_export_ids(request)
    return templates.TemplateResponse(
        "modules_export.html",
        _ctx(
            request,
            db,
            tracks=list_tracks(),
            track_filter=track,
            tracks_with_modules=modules_by_track(),
            selected_ids=set(ids),
        ),
    )


@router.api_route("/modules/print", methods=["GET", "POST"], response_class=HTMLResponse)
async def modules_print_pack(request: Request, db: Session = Depends(get_db)):
    if request.method == "POST":
        request._export_form = await request.form()
    ids, track = _parse_export_ids(request)
    modules = modules_for_export(ids or None, track=track if not ids else None)
    if not modules:
        return RedirectResponse("/modules/export", status_code=303)
    if len(modules) == 1:
        pack_title = modules[0].get("title") or "Module"
    elif track:
        t = next((x for x in list_tracks() if x["id"] == track), None)
        pack_title = f"{(t or {}).get('title') or track} modules"
    else:
        pack_title = "Selected modules"
    return templates.TemplateResponse(
        "modules_print.html",
        _ctx(
            request,
            db,
            modules=modules,
            pack_title=pack_title,
            generated_on=datetime.utcnow().strftime("%Y-%m-%d"),
        ),
    )


@router.api_route("/modules/export.pdf", methods=["GET", "POST"])
async def modules_export_pdf(request: Request, db: Session = Depends(get_db)):
    if request.method == "POST":
        request._export_form = await request.form()
    ids, track = _parse_export_ids(request)
    modules = modules_for_export(ids or None, track=track if not ids else None)
    if not modules:
        return RedirectResponse("/modules/export", status_code=303)
    from io import BytesIO

    from app.services.module_pdf import build_modules_pdf, suggested_filename

    buf = BytesIO()
    build_modules_pdf(modules, buf)
    buf.seek(0)
    filename = suggested_filename(modules)
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/modules/{module_id}", response_class=HTMLResponse)
async def module_detail(module_id: str, request: Request, db: Session = Depends(get_db)):
    mod = get_module(module_id)
    if not mod:
        return RedirectResponse("/modules", status_code=303)
    prev_m, next_m, index, total = module_neighbors(module_id)
    done = False
    user = get_current_user(request, db)
    if user and user.role == Role.student:
        p = (
            db.query(Progress)
            .filter(Progress.candidate_id == user.id, Progress.module_id == module_id)
            .first()
        )
        done = bool(p and p.completed)
    return templates.TemplateResponse(
        "module_detail.html",
        _ctx(
            request, db,
            module=mod,
            completed=done,
            prev_module=prev_m,
            next_module=next_m,
            module_index=index,
            module_total=total,
            related_assignments=assignments_for_module(module_id),
        ),
    )


@router.post("/modules/{module_id}/complete")
async def module_complete(module_id: str, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user or user.role != Role.student:
        return RedirectResponse(f"/modules/{module_id}", status_code=303)
    p = (
        db.query(Progress)
        .filter(Progress.candidate_id == user.id, Progress.module_id == module_id)
        .first()
    )
    if not p:
        p = Progress(candidate_id=user.id, module_id=module_id)
        db.add(p)
    p.completed = True
    p.completed_at = datetime.utcnow()
    db.commit()
    return RedirectResponse(f"/modules/{module_id}", status_code=303)


@router.get("/assignments", response_class=HTMLResponse)
async def assignments_index(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    track = request.query_params.get("track")
    if track:
        track = normalize_track_id(track)
    items = list_assignments(track=track) if track else list_assignments()
    statuses = {}
    if user and user.role == Role.student:
        for a in items:
            sub = submission_status(db, user.id, a["id"])
            statuses[a["id"]] = sub.status if sub else "not_started"
    return templates.TemplateResponse(
        "assignments.html",
        _ctx(
            request,
            db,
            assignments=items,
            statuses=statuses,
            tracks=list_tracks(),
            track_filter=track,
            tracks_with_assignments=assignments_by_track(),
        ),
    )


@router.get("/assignments/{assignment_id}", response_class=HTMLResponse)
async def assignment_detail(assignment_id: str, request: Request, db: Session = Depends(get_db)):
    asg = get_assignment(assignment_id)
    if not asg:
        return RedirectResponse("/assignments", status_code=303)
    user = get_current_user(request, db)
    sub = None
    my_scores = []
    if user and user.role == Role.student:
        sub = submission_status(db, user.id, assignment_id)
        my_scores = (
            db.query(Score)
            .filter(Score.candidate_id == user.id, Score.assignment_id == assignment_id)
            .all()
        )
    return templates.TemplateResponse(
        "assignment_detail.html",
        _ctx(request, db, assignment=asg, submission=sub, my_scores=my_scores, message=None),
    )


@router.post("/assignments/{assignment_id}/submit")
async def assignment_submit(
    assignment_id: str,
    request: Request,
    body: str = Form(""),
    action: str = Form("save"),
    db: Session = Depends(get_db),
):
    user = get_current_user(request, db)
    if not user or user.role != Role.student:
        return RedirectResponse("/login", status_code=303)
    asg = get_assignment(assignment_id)
    if not asg:
        return RedirectResponse("/assignments", status_code=303)
    sub = submission_status(db, user.id, assignment_id)
    if not sub:
        sub = Submission(candidate_id=user.id, assignment_id=assignment_id)
        db.add(sub)
    sub.body = body
    sub.updated_at = datetime.utcnow()
    if action == "submit":
        sub.status = "submitted"
        sub.submitted_at = datetime.utcnow()
    else:
        if sub.status != "submitted" and sub.status != "graded":
            sub.status = "draft"
    db.commit()
    return RedirectResponse(f"/assignments/{assignment_id}", status_code=303)


@router.get("/schedule", response_class=HTMLResponse)
async def schedule_page(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "schedule.html",
        _ctx(request, db, schedule=load_schedule()),
    )


@router.get("/glossary", response_class=HTMLResponse)
async def glossary_page(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "glossary.html",
        _ctx(request, db, terms=load_glossary()),
    )


@router.get("/tutorial", response_class=HTMLResponse)
async def syntax_tutorial(request: Request, db: Session = Depends(get_db)):
    """Markdown, Mermaid, PlantUML, and KaTeX syntax guide with live examples."""
    return templates.TemplateResponse(
        "syntax_tutorial.html",
        _ctx(request, db),
    )


@router.get("/selection", response_class=HTMLResponse)
async def selection_page(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "selection.html",
        _ctx(request, db, selection=load_selection_criteria()),
    )


@router.get("/me", response_class=HTMLResponse)
async def my_progress(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    if user.role == Role.instructor:
        return RedirectResponse("/instructor", status_code=303)
    tot = candidate_totals(db, user.id)
    track_totals = candidate_track_totals(db, user.id)
    progress = db.query(Progress).filter(Progress.candidate_id == user.id).all()
    done_ids = {p.module_id for p in progress if p.completed}
    primary = normalize_track_id(getattr(user, "primary_track", None) or "se")
    track_meta = next((t for t in list_tracks() if t["id"] == primary), None)
    return templates.TemplateResponse(
        "me.html",
        _ctx(
            request,
            db,
            totals=tot,
            track_totals=track_totals,
            done_ids=done_ids,
            modules=list_modules(),
            primary_track=primary,
            primary_track_meta=track_meta,
        ),
    )


def _require_instructor(request: Request, db: Session) -> Candidate | RedirectResponse:
    user = get_current_user(request, db)
    if not user or user.role != Role.instructor:
        return RedirectResponse("/login", status_code=303)
    return user


@router.get("/instructor", response_class=HTMLResponse)
async def instructor_home(request: Request, db: Session = Depends(get_db)):
    user = _require_instructor(request, db)
    if isinstance(user, RedirectResponse):
        return user
    show_inactive = request.query_params.get("inactive") == "1"
    return templates.TemplateResponse(
        "instructor.html",
        _ctx(
            request, db,
            board=leaderboard(db, include_inactive=show_inactive),
            tracks=list_tracks(),
            show_inactive=show_inactive,
            message=request.query_params.get("msg"),
            error=request.query_params.get("err"),
        ),
    )


@router.get("/instructor/students/{candidate_id}", response_class=HTMLResponse)
async def instructor_student_gradebook(
    candidate_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    """Per-student gradebook: score any track; ungraded work is optional."""
    user = _require_instructor(request, db)
    if isinstance(user, RedirectResponse):
        return user
    cand = db.query(Candidate).filter(
        Candidate.id == candidate_id,
        Candidate.role == Role.student,
    ).first()
    if not cand:
        return RedirectResponse("/instructor?err=Student+not+found", status_code=303)
    book = candidate_gradebook(db, cand.id)
    track_filter = request.query_params.get("track")
    if track_filter:
        track_filter = normalize_track_id(track_filter)
    return templates.TemplateResponse(
        "student_gradebook.html",
        _ctx(
            request, db,
            candidate=cand,
            gradebook=book,
            tracks=list_tracks(),
            track_filter=track_filter,
            primary_track=normalize_track_id(getattr(cand, "primary_track", None) or "se"),
            message=request.query_params.get("msg"),
            error=request.query_params.get("err"),
            saved=request.query_params.get("saved") == "1",
        ),
    )


@router.post("/instructor/students/{candidate_id}/update")
async def instructor_student_update(
    candidate_id: int,
    request: Request,
    name: str = Form(...),
    email: str = Form(""),
    cohort: str = Form("2026-UAE"),
    primary_track: str = Form("se"),
    pin: str = Form(""),
    recommended: str = Form("no"),
    notes: str = Form(""),
    is_active: str = Form("yes"),
    db: Session = Depends(get_db),
):
    user = _require_instructor(request, db)
    if isinstance(user, RedirectResponse):
        return user
    cand = db.query(Candidate).filter(
        Candidate.id == candidate_id,
        Candidate.role == Role.student,
    ).first()
    if not cand:
        return RedirectResponse("/instructor?err=Student+not+found", status_code=303)
    cand.name = name.strip() or cand.name
    cand.email = email.strip()
    cand.cohort = cohort.strip() or "2026-UAE"
    cand.primary_track = normalize_track_id(primary_track) or "se"
    cand.recommended = recommended == "yes"
    cand.notes = notes
    cand.is_active = is_active == "yes"
    if pin.strip():
        cand.pin_hash = hash_pin(pin.strip())
    db.commit()
    return RedirectResponse(
        f"/instructor/students/{candidate_id}?saved=1&msg=Student+updated",
        status_code=303,
    )


@router.post("/instructor/students/{candidate_id}/deactivate")
async def instructor_student_deactivate(
    candidate_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    user = _require_instructor(request, db)
    if isinstance(user, RedirectResponse):
        return user
    cand = db.query(Candidate).filter(
        Candidate.id == candidate_id,
        Candidate.role == Role.student,
    ).first()
    if not cand:
        return RedirectResponse("/instructor?err=Student+not+found", status_code=303)
    cand.is_active = False
    db.commit()
    return RedirectResponse(
        f"/instructor?msg=Deactivated+{cand.name.replace(' ', '+')}",
        status_code=303,
    )


@router.post("/instructor/students/{candidate_id}/reactivate")
async def instructor_student_reactivate(
    candidate_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    user = _require_instructor(request, db)
    if isinstance(user, RedirectResponse):
        return user
    cand = db.query(Candidate).filter(
        Candidate.id == candidate_id,
        Candidate.role == Role.student,
    ).first()
    if not cand:
        return RedirectResponse("/instructor?err=Student+not+found", status_code=303)
    cand.is_active = True
    db.commit()
    return RedirectResponse(
        f"/instructor/students/{candidate_id}?msg=Reactivated",
        status_code=303,
    )


@router.post("/instructor/students/{candidate_id}/delete")
async def instructor_student_delete(
    candidate_id: int,
    request: Request,
    confirm: str = Form(""),
    db: Session = Depends(get_db),
):
    """Hard-delete a student and their scores/submissions/progress."""
    user = _require_instructor(request, db)
    if isinstance(user, RedirectResponse):
        return user
    cand = db.query(Candidate).filter(
        Candidate.id == candidate_id,
        Candidate.role == Role.student,
    ).first()
    if not cand:
        return RedirectResponse("/instructor?err=Student+not+found", status_code=303)
    if confirm.strip().upper() != "DELETE":
        return RedirectResponse(
            f"/instructor/students/{candidate_id}?err=Type+DELETE+to+confirm+removal",
            status_code=303,
        )
    name = cand.name
    db.query(Score).filter(Score.candidate_id == candidate_id).delete()
    db.query(Submission).filter(Submission.candidate_id == candidate_id).delete()
    db.query(Progress).filter(Progress.candidate_id == candidate_id).delete()
    db.delete(cand)
    db.commit()
    return RedirectResponse(
        f"/instructor?msg=Removed+{name.replace(' ', '+')}",
        status_code=303,
    )


@router.get("/instructor/content", response_class=HTMLResponse)
async def content_editor_index(request: Request, db: Session = Depends(get_db)):
    """List editable markdown curriculum files."""
    user = get_current_user(request, db)
    if not user or user.role != Role.instructor:
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse(
        "content_editor.html",
        _ctx(
            request, db,
            files=list_editable_files(),
            kind=None,
            content_id=None,
            body="",
            title="Content editor",
            saved=False,
            error=None,
        ),
    )


@router.get("/instructor/content/{kind}/{content_id}", response_class=HTMLResponse)
async def content_editor_page(
    kind: str,
    content_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    user = get_current_user(request, db)
    if not user or user.role != Role.instructor:
        return RedirectResponse("/login", status_code=303)
    body = read_editable(kind, content_id)
    if body is None:
        return RedirectResponse("/instructor/content", status_code=303)
    title = content_id
    if kind == "modules":
        m = get_module(content_id)
        if m:
            title = m["title"]
    elif kind == "assignments":
        a = get_assignment(content_id)
        if a:
            title = a["title"]
    return templates.TemplateResponse(
        "content_editor.html",
        _ctx(
            request, db,
            files=list_editable_files(),
            kind=kind,
            content_id=content_id,
            body=body,
            title=title,
            saved=request.query_params.get("saved") == "1",
            error=None,
        ),
    )


@router.post("/instructor/content/{kind}/{content_id}")
async def content_editor_save(
    kind: str,
    content_id: str,
    request: Request,
    body: str = Form(""),
    db: Session = Depends(get_db),
):
    user = get_current_user(request, db)
    if not user or user.role != Role.instructor:
        return RedirectResponse("/login", status_code=303)
    ok = write_editable(kind, content_id, body)
    if not ok:
        return templates.TemplateResponse(
            "content_editor.html",
            _ctx(
                request, db,
                files=list_editable_files(),
                kind=kind,
                content_id=content_id,
                body=body,
                title=content_id,
                saved=False,
                error="Could not save — invalid path or file.",
            ),
            status_code=400,
        )
    return RedirectResponse(
        f"/instructor/content/{kind}/{content_id}?saved=1",
        status_code=303,
    )


@router.post("/instructor/upload-image")
async def upload_content_image(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Upload an image for curriculum markdown; returns JSON {url, markdown}."""
    user = get_current_user(request, db)
    if not user or user.role != Role.instructor:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)

    original = file.filename or "upload.bin"
    ext = Path(original).suffix.lower()
    if ext not in ALLOWED_IMAGE_EXTS:
        return JSONResponse(
            {"error": f"File type not allowed. Use: {', '.join(sorted(ALLOWED_IMAGE_EXTS))}"},
            status_code=400,
        )

    data = await file.read()
    if len(data) > MAX_UPLOAD_BYTES:
        return JSONResponse(
            {"error": f"File too large (max {MAX_UPLOAD_BYTES // (1024 * 1024)} MB)"},
            status_code=400,
        )
    if not data:
        return JSONResponse({"error": "Empty file"}, status_code=400)

    safe_stem = re.sub(r"[^a-zA-Z0-9_-]+", "-", Path(original).stem)[:40].strip("-") or "img"
    name = f"{safe_stem}-{uuid.uuid4().hex[:10]}{ext}"
    dest = UPLOAD_DIR / name
    dest.write_bytes(data)

    url = f"{UPLOAD_URL_PREFIX}/{name}"
    alt = safe_stem.replace("-", " ")
    return JSONResponse({
        "url": url,
        "markdown": f"![{alt}]({url})",
        "filename": name,
    })


@router.get("/instructor/grade/{candidate_id}/{assignment_id}", response_class=HTMLResponse)
async def grade_form(
    candidate_id: int,
    assignment_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    user = _require_instructor(request, db)
    if isinstance(user, RedirectResponse):
        return user
    asg = get_assignment(assignment_id)
    cand = db.query(Candidate).filter(
        Candidate.id == candidate_id,
        Candidate.role == Role.student,
    ).first()
    if not asg or not cand:
        return RedirectResponse("/instructor", status_code=303)
    sub = submission_status(db, candidate_id, assignment_id)
    existing = {
        s.dimension: s
        for s in db.query(Score)
        .filter(Score.candidate_id == candidate_id, Score.assignment_id == assignment_id)
        .all()
    }
    # Neighbor assignments (any track) for quick next/prev grading
    all_asg = list_assignments()
    ids = [a["id"] for a in all_asg]
    try:
        idx = ids.index(assignment_id)
    except ValueError:
        idx = -1
    prev_asg = all_asg[idx - 1] if idx > 0 else None
    next_asg = all_asg[idx + 1] if 0 <= idx < len(all_asg) - 1 else None
    return templates.TemplateResponse(
        "grade.html",
        _ctx(
            request, db,
            assignment=asg,
            candidate=cand,
            submission=sub,
            existing=existing,
            prev_asg=prev_asg,
            next_asg=next_asg,
            message=request.query_params.get("msg"),
            saved=request.query_params.get("saved") == "1",
        ),
    )


@router.post("/instructor/grade/{candidate_id}/{assignment_id}")
async def grade_submit(
    candidate_id: int,
    assignment_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    user = _require_instructor(request, db)
    if isinstance(user, RedirectResponse):
        return user
    asg = get_assignment(assignment_id)
    if not asg:
        return RedirectResponse("/instructor", status_code=303)
    form = await request.form()
    action = str(form.get("action") or "save")

    if action == "clear":
        clear_assignment_scores(db, candidate_id, assignment_id)
        sub = submission_status(db, candidate_id, assignment_id)
        if sub and sub.status == "graded":
            sub.status = "submitted" if sub.submitted_at else "draft"
        db.commit()
        return RedirectResponse(
            f"/instructor/grade/{candidate_id}/{assignment_id}?msg=Scores+cleared",
            status_code=303,
        )

    for dim in asg.get("rubric") or []:
        d = dim["dimension"]
        raw = form.get(f"points_{d}", "0")
        fb = form.get(f"feedback_{d}", "")
        try:
            pts = float(raw)
        except ValueError:
            pts = 0.0
        max_p = float(dim.get("max_points") or 10)
        pts = max(0.0, min(pts, max_p))
        row = (
            db.query(Score)
            .filter(
                Score.candidate_id == candidate_id,
                Score.assignment_id == assignment_id,
                Score.dimension == d,
            )
            .first()
        )
        if not row:
            row = Score(
                candidate_id=candidate_id,
                assignment_id=assignment_id,
                dimension=d,
                max_points=max_p,
            )
            db.add(row)
        row.points = pts
        row.max_points = max_p
        row.feedback = str(fb)
        row.graded_at = datetime.utcnow()
        row.graded_by = user.name
    sub = submission_status(db, candidate_id, assignment_id)
    if sub:
        sub.status = "graded"
    rec = form.get("recommended")
    cand = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if cand and rec is not None:
        cand.recommended = rec == "yes"
    notes = form.get("notes")
    if cand and notes is not None:
        cand.notes = str(notes)
    db.commit()

    if action == "save_next":
        all_ids = [a["id"] for a in list_assignments()]
        try:
            i = all_ids.index(assignment_id)
            if i + 1 < len(all_ids):
                return RedirectResponse(
                    f"/instructor/grade/{candidate_id}/{all_ids[i + 1]}?saved=1",
                    status_code=303,
                )
        except ValueError:
            pass
        return RedirectResponse(
            f"/instructor/students/{candidate_id}?saved=1",
            status_code=303,
        )

    if action == "save_return":
        return RedirectResponse(
            f"/instructor/students/{candidate_id}?saved=1&msg=Grade+saved",
            status_code=303,
        )

    return RedirectResponse(
        f"/instructor/grade/{candidate_id}/{assignment_id}?saved=1",
        status_code=303,
    )


@router.post("/instructor/add-student")
async def add_student(
    request: Request,
    name: str = Form(...),
    pin: str = Form("1234"),
    cohort: str = Form("2026-UAE"),
    email: str = Form(""),
    primary_track: str = Form("se"),
    db: Session = Depends(get_db),
):
    user = _require_instructor(request, db)
    if isinstance(user, RedirectResponse):
        return user
    track = normalize_track_id(primary_track) or "se"
    cand = Candidate(
        name=name.strip(),
        email=email.strip(),
        pin_hash=hash_pin(pin.strip() or "1234"),
        role=Role.student,
        cohort=cohort.strip() or "2026-UAE",
        primary_track=track,
        is_active=True,
    )
    db.add(cand)
    db.commit()
    db.refresh(cand)
    return RedirectResponse(
        f"/instructor/students/{cand.id}?msg=Student+added",
        status_code=303,
    )
