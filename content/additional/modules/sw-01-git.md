# Working with Git

## Learning outcomes

After this module you can:

- Explain **why** teams use Git (history, branching, collaboration, rollback)  
- Run the **daily loop**: clone/pull → branch → commit → push  
- Write useful **commit messages** and avoid common mistakes  
- Recover from simple errors (`status`, `diff`, `log`, undo unstaged changes)  

## Why Git matters here

On CISS work, Git is not optional paperwork — it is how we:

| Need | Git answer |
|------|------------|
| Multiple people on one codebase | Branches + merge/rebase discipline |
| “What changed and why?” | Commits + messages + blame/log |
| Safe experiments | Branches; easy discard |
| Code review | Push branch → **PR (Bitbucket at work)** / **MR (GitLab in CISS lab)** |
| Traceability to requirements | Commit / MR text can cite `FR-…` IDs |

SE link: a commit that implements `FR-CI-02` is part of the **design → verification** trail when you can point to it.

## Core mental model

```text
Working tree  →  staging area (index)  →  local commits  →  remote (origin)
   edit files        git add               git commit         git push
```

- **Working tree** — files you edit  
- **Staging** — what will go into the next commit  
- **Commit** — immutable snapshot with author, time, message  
- **Remote** — shared copy (**Bitbucket** at work; **GitLab** for CISS labs)

## Install & first-time setup

1. Install Git for your OS ([git-scm.com](https://git-scm.com/)).  
2. Identity (use your real name / org email):

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

3. Optional but helpful: default editor, `pull.rebase` policy (agree with your team).

## Daily workflow (memorize this)

```bash
# Start from an up-to-date main
git checkout main
git pull origin main

# Feature branch — name after the Jira Deficiency Report (program standard)
git checkout -b DR-42
# optional suffix if your team allows: DR-42-double-checkin

# Work… then see what changed
git status
git diff

# Stage and commit (include DR key in the message)
git add path/to/file.java
git commit -m "DR-42 Reject double check-in when already checked in (FR-CI-02)"

# Share to remote (Bitbucket at work; GitLab for CISS lab)
git push -u origin DR-42
```

### Commit message habits

| Prefer | Avoid |
|--------|--------|
| Imperative, specific: “Add null guard on export path” | “fixes”, “wip”, “asdf” |
| Cite FR / issue when relevant | Giant mixed commits (“UI + DB + renames”) |
| One logical change per commit when practical | Secrets, credentials, huge binaries |

## Branching (program team model)

```text
main       — always deployable / demoable (protected)
DR-###     — your work for that Jira Deficiency Report (short-lived)
```

Rules of thumb:

1. Branch from latest `main`.  
2. **Branch name = DR key** (`DR-42`), matching Jira.  
3. Keep branches short; open a review early (**Bitbucket PR** at work, **GitLab MR** in CISS lab).  
4. Prefer small PRs/MRs over week-long monsters.  
5. Never force-push `main` (and rarely force-push shared branches).

## Commands you will use constantly

| Command | Purpose |
|---------|---------|
| `git status` | What’s dirty / staged? |
| `git diff` / `git diff --staged` | Unstaged / staged changes |
| `git log --oneline -15` | Recent history |
| `git pull` | Update current branch from remote |
| `git fetch` | Download remote refs without merging |
| `git stash` / `git stash pop` | Park WIP temporarily |
| `git restore <file>` | Discard unstaged edits (careful) |
| `git restore --staged <file>` | Unstage |

## Common mistakes (and fixes)

| Mistake | Safer recovery |
|---------|----------------|
| Committed to `main` by accident | `git branch feature/x` then reset main carefully (ask a peer if unsure) |
| Too much in one commit | Soft reset / split next time; avoid rewriting shared history |
| Pushed secrets | Rotate secrets immediately; remove from history only with instructor guidance |
| “Detached HEAD” | `git checkout main` or checkout a named branch |
| Merge conflicts | Edit files → `git add` → complete merge/rebase; **read both sides** |

## Offline drill (20 min)

In a throwaway folder:

1. `git init` a tiny project (one `README.md`).  
2. Make two commits on `main`.  
3. Create `feature/demo`, add a file, commit, show `git log --oneline --graph --all`.  
4. Change a file, run `git diff`, then discard with `git restore`.  

Bring screenshot or paste of `git log --oneline --graph --all` to Thursday.

## Integrity

- Do not commit another person’s work as your own.  
- Do not push secrets, private keys, or classified material.  
- Cite AI if it wrote non-trivial code; you own the design and review.

## Further reading

| Topic | Source |
|-------|--------|
| Official book | [Pro Git (free)](https://git-scm.com/book/en/v2) — Ch. 1–3 first |
| Everyday commands | [GitHub Git Cheat Sheet (PDF)](https://education.github.com/git-cheat-sheet-education.pdf) (CLI is the same on any host) |
| Commit hygiene | Include `DR-###` in messages; optional Conventional Commits style |

## Next

**Team workflow** — program **Jira + Bitbucket + Nexus**, practiced on **CISS GitLab** (MR ≈ PR).
