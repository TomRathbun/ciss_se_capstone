# Git as daily craft

> **When:** Week 1 · Wednesday afternoon · Masdar
> **Who:** All interns (weeks 1–4)
> **Tomorrow morning:** [sw-fa01-git — Git daily-loop evidence](/assignments/sw-fa01-git) (~2 hours), due **Week 1 Thursday morning**.

## Learning outcomes

After this afternoon you can:

- Clone, branch, commit, push without folklore
- Name a branch after a ticket
- Recover from a mistake without destroying history you share
- Write a commit message a reviewer can use

## Why this afternoon exists

Every discipline will touch Git. Network configs, admin scripts, SE markdown, and Java all live in history. If you cannot branch safely, you cannot work on a team.

## Teach

**Daily loop**

```text
ticket  →  branch  →  edit  →  commit  →  push  →  review  →  merge
```

CISS lab: **GitLab**. Program work: Bitbucket + Jira. Same habits, different buttons.

| Habit | Rule |
|-------|------|
| Branch | `DR-123-short-name` or lab equivalent |
| Commit | Imperative, scoped, true (`Add gateway to VLAN 20 plan`) |
| Push | Your branch, not `main` |
| Recovery | Prefer *new commits* that undo; ask before rewrite of shared history |

Commands you will actually use: `status`, `diff`, `log`, `switch -c`, `commit`, `push`, `pull --rebase` only when you know what rebase is.

Do not commit secrets, PCAP with keys, or classified diagrams.

## In-class exercise (30–40 min)

In the course repo (or a sandbox): create a branch, add a one-line file, commit, show `log -1`. Instructor watches for `main` commits.

## Additional lesson

The long-form original is archived as **[sw-01-git](/modules/sw-01-git)**. Read it after class if you will keep this discipline.

## Tomorrow morning

Do **sw-fa01-git** before the next afternoon lecture. Time-box **two hours**. Stop and turn in what you have. Do not start tomorrow’s discipline homework until this one is in.

## Integrity

Unclassified work only. No production credentials, no classified topologies, no secrets in Git. Cite public sources.
