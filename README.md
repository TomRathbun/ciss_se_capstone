# CISS Capstone

**Systems Engineering · Military Operations · Intern Selection**

A course web app for CISS intern cohorts (UAE). Same visual family as the SDC Time Tracker: dark UI, module-based learning, rubric grading to **distinguish candidates** for the main project.

## Purpose

| Goal | How |
|------|-----|
| Teach SE foundations | Modules + offline reading + workshops |
| Teach military air ops literacy | ATO planning & execution modules |
| Use a living case study | Links to SDC Time Tracker `/systems-engineering` |
| Select interns | Weighted assignments + instructor leaderboard (private) |
| Later | Radar situational awareness capstone (**PRSAS** implementation pack) |

## Lab environment (important)

**Course and program labs use virtual machines (VMs)** — typically RHEL-compatible guests under **vSphere / ESXi** — not Docker containers as the default runtime.

| Expect | Do not assume |
|--------|----------------|
| Postgres, ActiveMQ, JBoss, app hosts as **VMs or services on VMs** | `docker run …` as the primary lab path |
| Hostnames, IPs, and credentials from the instructor / runbook | Localhost-only single-machine demos unless told otherwise |
| `systemctl`, packages, firewall, and IDM on the guest OS | Container-only networking mental models |

Docker may appear in external reading; for CISS work, prefer the **assigned VM** and document connection details (host, port, user) in your notes.

## Rhythm

- **Monday** — 3–4h introduce topic + workshop  
- **Thursday** — Q&A, peer feedback, grading  
- Not every week is an SE lecture; ops weeks and catch-up are scheduled  

See `content/schedule/cohort.yaml`.

## Quick start (uv — same as SDC Time Tracker)

```bash
cd ciss_se_capstone
uv sync
uv run python run.py
```

Ctrl+Click the **Local** URL in the terminal (e.g. `http://127.0.0.1:8890`).

The server still binds `0.0.0.0` so other devices on the network can connect; `0.0.0.0` itself is not a browser address, which is why that link does not open.

Optional:

```bash
uv run python run.py --port 8890
uv run python run.py --host 127.0.0.1   # local-only bind
uv run python run.py --no-reload        # stable if packages are being updated
```

### If the server crashes on reload (`ssl_context_factory`)

That usually means the venv was half-upgraded while the server was running (WatchFiles saw `.venv` change). Fix:

1. Stop every course server window (`Ctrl+C`).
2. `uv sync`
3. `uv run python run.py`

Reload now watches only `app/` and `content/`, not `.venv`.

### Demo logins (change for real cohort)

| Role | PIN |
|------|-----|
| Course Instructor | `4242` |
| Intern Alpha–Delta | `1234` |

## Content layout

```
content/
  catalog.yaml              # modules + assignment metadata + rubrics
  selection_criteria.yaml   # how candidates are judged
  schedule/cohort.yaml      # Mon/Thu plan
  glossary/terms.yaml
  modules/*.md              # lecture / reading bodies
  assignments/*.md          # student-facing briefs
  project/radar_sa_project.md  # UC-CISS_PROJECT-001 PRSAS (+ sister LLAP note)
```

Edit Markdown and YAML; restart not always required for content (read on each request).

## App features

- **Modules** — SE, Software, Networking (Juniper), SysAdmin, Military; mark complete  
- **Print / PDF** — `/modules/export` to pick all, a track, or some modules; download a PDF or browser print (better for Mermaid)  
- **Assignments** — per-track weighted briefs; student draft/submit  
- **Instructor desk** — leaderboard, per-dimension grading, recommend flag, add interns  
- **Content editor** (instructor) — dual-pane Markdown with live **Mermaid**, **PlantUML**, **KaTeX**, and **image upload** (paste or button); saves to `content/modules|assignments/*.md`  
- **Syntax tutorial** — `/tutorial` examples for Markdown, Mermaid, PlantUML, KaTeX, images  
- **My progress** — student weighted % so far  
- **Glossary / Selection / Schedule**  
- **Case study links** — env `CISS_CASE_STUDY_URL` (default `http://localhost:8888/systems-engineering`)

## Scoring (discrimination)

Assignment weights (SE track, from catalog — one Thursday take-home per module):

| ID | Module | Focus | Weight |
|----|--------|--------|--------|
| SE-A00 | se-00 | Track plan & artifact map | 3% |
| SE-A01 | se-01 | SE literacy / failure-mode brief | 5% |
| A1 | se-02 | Vision, context & stakeholders | 10% |
| SE-A03 | se-03 | Use cases from needs | 8% |
| A2 | se-04 | Requirements + ACs (two-week) | 16% |
| SE-A05 | se-05 | Architecture views & allocation | 8% |
| A3 | se-06 | State + sequence | 10% |
| A7 | se-07 | Messaging + API ICD | 8% |
| SE-A11 | se-11 | MBSE / frameworks literacy | 5% |
| A4 | se-08 | RTM + V&V | 10% |
| SE-A09 | se-09 | ETAS artifact hunt | 5% |
| SE-A10 | se-10 | Radar SA framing pack | 5% |
| A6 | se-00 | Professionalism (ongoing) | 7% |

Military ops mission card (**A5**, 15% of the MIL track) is separate. Overall % = weighted average of **foundation** assignments that have grades. **PRSAS / capstone** assignments (`phase: capstone` in the catalog) are scored on a separate 100%-per-track scale so they do not dilute intern-selection standings. Instructor **recommended** flag is separate judgment for main-project select.

## Ports

| App | Default port |
|-----|----------------|
| CISS Capstone | **8890** |
| SDC Time Tracker (case study) | **8888** |

## Roadmap

- [x] Scaffold + SE modules + ATO modules  
- [x] Grading / leaderboard  
- [x] Networking track — older Juniper (EX / SRX / MPLS / IPsec)  
- [ ] Richer ATO exercises / red-team injects  
- [x] Full radar SA capstone pack (PRSAS — modules + assignments per track)  
- [ ] Export gradebook CSV  
- [ ] Cohort multi-tenancy  

## License

Internal training use unless otherwise noted.
