# CISS SE Capstone

**Systems Engineering · Military Operations · Intern Selection**

A course web app for CISS intern cohorts (UAE). Same visual family as the SDC Time Tracker: dark UI, module-based learning, rubric grading to **distinguish candidates** for the main project.

## Purpose

| Goal | How |
|------|-----|
| Teach SE foundations | Modules + offline reading + workshops |
| Teach military air ops literacy | ATO planning & execution modules |
| Use a living case study | Links to SDC Time Tracker `/systems-engineering` |
| Select interns | Weighted assignments + instructor leaderboard (private) |
| Later | Radar situational awareness capstone (placeholder module) |

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
```

Edit Markdown and YAML; restart not always required for content (read on each request).

## App features

- **Modules** — SE track + OPS track, mark complete  
- **Assignments A1–A6** — weighted; student draft/submit  
- **Instructor desk** — leaderboard, per-dimension grading, recommend flag, add interns  
- **My progress** — student weighted % so far  
- **Glossary / Selection / Schedule**  
- **Case study links** — env `CISS_CASE_STUDY_URL` (default `http://localhost:8888/systems-engineering`)

## Scoring (discrimination)

Assignment weights (from catalog):

| ID | Focus | Weight |
|----|--------|--------|
| A1 | Context & stakeholders | 10% |
| A2 | Requirements + ACs | 25% |
| A3 | State + sequence | 20% |
| A4 | RTM + V&V | 20% |
| A5 | Mission card (ops) | 15% |
| A6 | Professionalism | 10% |

Overall % = weighted average of assignments that have grades. Instructor **recommended** flag is separate judgment for main-project select.

## Ports

| App | Default port |
|-----|----------------|
| CISS SE Capstone | **8890** |
| SDC Time Tracker (case study) | **8888** |

## Roadmap

- [x] Scaffold + SE modules + ATO modules  
- [x] Grading / leaderboard  
- [ ] Richer ATO exercises / red-team injects  
- [ ] Full radar SA capstone pack  
- [ ] Export gradebook CSV  
- [ ] Cohort multi-tenancy  

## License

Internal training use unless otherwise noted.
