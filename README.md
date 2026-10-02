# CISS Capstone

**Systems Engineering · Military Operations · Intern Selection**

A course web app for CISS intern cohorts (UAE). Same visual family as the SDC Time Tracker: dark UI, module-based learning, rubric grading to **distinguish candidates** for the main project. Delivery is the Masdar-afternoon model (common foundation, week-5 kickoff, then depth).

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

## Rhythm (Masdar afternoons)

Lockheed Martin SMEs work at the Software Development Center (Al Dhafra AFB). Interns stay at the Masdar City LM office. One expert travels each weekday afternoon (~30 minutes).

| | |
|--|--|
| **Morning** | Interns do yesterday’s assignment (~2 hours), due before that day’s lecture |
| **Mon afternoon** | Systems Engineering (mandatory all 36 weeks) |
| **Tue afternoon** | Networking |
| **Wed afternoon** | Software |
| **Thu afternoon** | System Administration |
| **Fri afternoon** | Flex (SE workshop, integration, or a **TAA-cleared** military lecture) |

**Weeks 1–4** — all interns attend every lecture (general literacy).  
**Week 5** — capstone kickoff (PRSAS).  
**Week 6+** — electives; everyone stays in SE.  
**Weeks 25–36** — Masdar continues. SDC on-site is **not** on the intern calendar until approvals exist.

Pre-Masdar lessons are preserved under **Additional / archived** (`content/additional/`). Do not delete them.

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
  catalog.yaml                 # live Masdar path (foundation, kickoff, depth, PRSAS)
  additional/                  # archived pre-Masdar lessons (do not delete)
    catalog.yaml
    modules/*.md
    assignments/*.md
  schedule/cohort.yaml         # Mon–Fri afternoon plan
  glossary/terms.yaml
  modules/*.md                 # live lecture bodies
  assignments/*.md             # live ~2h morning briefs
  project/radar_sa_project.md  # UC-CISS_PROJECT-001 PRSAS
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

Live intern-selection scores use **foundation + kickoff + depth** assignments (each track sums to 100%). Each lecture assigns a **~2 hour** packet due the next morning.

**PRSAS / capstone** assignments (`phase: capstone`) are scored on a separate 100%-per-track scale. **Additional / archived** pre-Masdar assignments do not affect the leaderboard. Instructor **recommended** flag is separate judgment for main-project select.

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
