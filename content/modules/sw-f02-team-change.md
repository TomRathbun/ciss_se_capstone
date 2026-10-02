# How a team ships a change

> **When:** Week 2 · Wednesday afternoon · Masdar
> **Who:** All interns (weeks 1–4)
> **Tomorrow morning:** [sw-fa02-team-change — Ticket → MR checklist](/assignments/sw-fa02-team-change) (~2 hours), due **Week 2 Thursday morning**.

## Learning outcomes

After this afternoon you can:

- Walk ticket → branch → merge request → main
- Write a review comment that would catch a real defect
- Map program tools (Jira/Bitbucket) to CISS lab (GitLab)
- Refuse to merge your own unchecked work

## Why this afternoon exists

A brilliant patch on `main` with no ticket is how labs become folklore. The habit is the same whether you are changing Java or a markdown ICD.

## Teach

```text
PROGRAM:  Jira DR-123 → branch DR-123 → Bitbucket PR → Jenkins → main
CISS LAB: ticket DR-123 → branch DR-123 → GitLab MR → pipeline → main
```

A **merge request** (lab) / **pull request** (program) is the review surface: what changed, why, how to test, what you did not do.

Review comments that help: “This shall is now untested — where is the AC?” Comments that do not: “Looks good” on 400 lines.

You do not merge your own unchecked work. If you are alone in a lab, you still fill the checklist and wait for a peer or instructor.

## In-class exercise (30–40 min)

Draft an MR description for yesterday’s Git file. Peer writes two review comments: one useful, one useless. Discuss.

## Additional lesson

The long-form original is archived as **[sw-02-bitbucket-jira](/modules/sw-02-bitbucket-jira)**. Read it after class if you will keep this discipline.

## Tomorrow morning

Do **sw-fa02-team-change** before the next afternoon lecture. Time-box **two hours**. Stop and turn in what you have. Do not start tomorrow’s discipline homework until this one is in.

## Integrity

Unclassified work only. No production credentials, no classified topologies, no secrets in Git. Cite public sources.
