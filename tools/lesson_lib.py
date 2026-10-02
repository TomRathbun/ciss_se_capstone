"""Shared lesson/assignment markdown builders for the Masdar path."""

from __future__ import annotations


def lesson(
    *,
    title: str,
    when: str,
    who: str,
    assignment_id: str,
    assignment_title: str,
    due: str,
    outcomes: list[str],
    why: str,
    teach: str,
    exercise: str,
    additional_of: str | None = None,
    hold: str | None = None,
    integrity: str | None = None,
) -> str:
    extra = ""
    if additional_of:
        extra += (
            f"\n## Additional lesson\n\n"
            f"The long-form original is archived as **[{additional_of}](/modules/{additional_of})**. "
            f"Read it after class if you will keep this discipline.\n"
        )
    if hold:
        extra += f"\n## Hold for later\n\n{hold}\n"
    integ = integrity or (
        "Unclassified work only. No production credentials, no classified topologies, "
        "no secrets in Git. Cite public sources."
    )
    bullets = "\n".join(f"- {o}" for o in outcomes)
    return f"""# {title}

> **When:** {when}
> **Who:** {who}
> **Tomorrow morning:** [{assignment_id} — {assignment_title}](/assignments/{assignment_id}) (~2 hours), due **{due}**.

## Learning outcomes

After this afternoon you can:

{bullets}

## Why this afternoon exists

{why}

## Teach

{teach}

## In-class exercise (30–40 min)

{exercise}
{extra}
## Tomorrow morning

Do **{assignment_id}** before the next afternoon lecture. Time-box **two hours**. Stop and turn in what you have. Do not start tomorrow’s discipline homework until this one is in.

## Integrity

{integ}
"""


def assignment(
    *,
    code: str,
    title: str,
    time: str,
    due: str,
    module: str,
    weight: str,
    prompt: str,
    deliverables: str,
    quality: str,
) -> str:
    return f"""# {code} — {title}

**Time box:** 2 hours. Stop at 2 hours and turn in what you have.
**Due:** {due}
**Module:** {module}
**Weight:** {weight} of this track’s intern-selection score.

## Prompt

{prompt}

## Deliverables

{deliverables}

## Quality bar

{quality}

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| completeness | 10 | All required artifacts present |
| accuracy | 10 | Technically right at intern level |
| communication | 5 | A peer can grade it in five minutes |
"""
