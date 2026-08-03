# What Is Systems Engineering?

## Learning outcomes

After this module you can:

- Explain SE in one paragraph to a non-engineer
- Separate **need**, **requirement**, and **design**
- Name why projects fail without SE discipline

## The one-paragraph definition

**Systems engineering** is the discipline of making sure we understand the real-world problem, capture what the system must do (and not do), design a solution that can be built and tested, integrate the pieces, and prove we met the need — across hardware, software, people, and process.

It is *not* only drawing diagrams. Diagrams are tools. The product of SE is **decisions under evidence**.

## Need → Requirements → Design

| Layer | Question | Example (time tracker) |
|-------|----------|-------------------------|
| **Need** | What problem exists in the world? | FOSC staff must record auditable attendance matching contract rules |
| **Requirement** | What shall the system do? | The system shall reject double check-in for the same day |
| **Design** | How will we implement it? | `time_state.can_check_in` returns an error if status is `checked_in` |

**Common intern mistake:** writing design as requirements (“The system shall use SQLite”). Prefer *what* unless the customer constrained the *how*.

## Why SE matters here

On CISS-type work you will touch:

- Multiple users and roles
- External systems (feeds, exports, other apps)
- Rules that must be defensible in review
- People who fly / plan / defend — not only code

SE gives a shared language so software, ops, and leadership do not talk past each other.

## Classic failure modes (watch for these in your work)

1. **Unstated assumptions** — “obvious” to you, invisible to the tester
2. **Gold plating** — features nobody needed
3. **Interface surprises** — two teams meet at a boundary with different formats
4. **Untestable “requirements”** — “the UI shall be intuitive”
5. **No validation** — built the wrong thing correctly

## Offline exercise (30 min)

Pick any app you use daily (banking, maps, chat). Write:

1. One sentence **need**
2. Three **shall** requirements
3. One **design** choice that is *not* a requirement

Bring to Thursday if unsure.

## Next

**Stakeholders, Context & Boundaries** — drawing the box around the system.
