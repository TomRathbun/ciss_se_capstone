# Workshop A3b — EARS Pack → Flat State Chart

**Not separately graded.** Monday workshop for **se-06**. The Thursday take-home for this module is **A3**.

Use the **fixed** printer-queue pack below — do not rewrite the shalls.

## Prompt

You are given a **fixed set of EARS requirements**. Produce a **flat** (non-hierarchical) state machine that implements them, and a mapping table.

### Requirement pack (use exactly these IDs)

**Context:** Lab printer queue for a small ops cell.

| ID | Requirement |
|----|-------------|
| FR-PQ-01 | WHEN an authorized user submits a print job AND the queue is not full, the system shall accept the job and place it in state Queued. |
| FR-PQ-02 | IF the queue is full THEN the system shall reject the job and notify the user. |
| FR-PQ-03 | WHEN a Queued job reaches the head of the queue AND the printer is idle, the system shall move the job to Printing and start the device. |
| FR-PQ-04 | WHEN printing completes successfully, the system shall mark the job Complete. |
| FR-PQ-05 | IF the printer reports a fault WHILE a job is Printing THEN the system shall mark the job Faulted and hold the queue. |
| FR-PQ-06 | WHEN an operator issues clear_fault AND there is a Faulted job, the system shall move that job to Queued (re-queue) and release the hold. |
| FR-PQ-07 | WHEN a user cancels a job WHILE it is Queued, the system shall remove it from the queue and mark it Cancelled. |
| FR-PQ-08 | IF a user attempts to cancel a job WHILE it is Printing THEN the system shall reject the cancel request and notify the user. |

## Deliverables

1. **Flat state chart** covering job lifecycle (recommended states include at least: `Queued`, `Printing`, `Complete`, `Faulted`, `Cancelled` — add others only if justified).  
   - Every transition labeled `trigger [guard] / activity` as needed.  
   - Explicit reject paths for FR-PQ-02 and FR-PQ-08.
2. **Mapping table** with one row per FR:

| FR ID | Trigger | Guard / WHILE | From → To | Activity |
|-------|---------|---------------|-----------|----------|
| … | … | … | … | … |

3. **Short note (≤10 lines):** one illegal sequence your chart prevents that a careless implementer might allow.

## Rubric

| Dimension | Max | Description |
|-----------|-----|-------------|
| coverage | 10 | Every FR in mapping table and on chart |
| correctness | 10 | Triggers/guards match EARS; reject paths present |
| communication | 5 | Readable diagram and table |
