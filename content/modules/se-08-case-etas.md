# Case Study — SDC Time Tracker (ETAS)

## Purpose

Connect classroom SE to a **running system** used on FOSC-related timekeeping.

## Before class

1. Open the time tracker app (instructor provides URL; default local `http://localhost:8888`).  
2. Open **Systems Engineering** (`/systems-engineering`).  
3. Optionally log a check-in / leave flow on a demo account.

## Walkthrough agenda (≈ 2 hours)

### 1. Need & stakeholders (15 min)

Read the operational need on the SE page. Identify which stakeholder you would be if you joined CISS as an engineer supporting tools vs ops.

### 2. Requirements & ACs (25 min)

Find `FR-BEOD-01` and `AC-BEOD-01`. Discuss as a group:

- Why is the 6.0 hour minimum a requirement, not “just code”?  
- How would you test the boundary 5.99 vs 6.0?

### 3. State machine (20 min)

Open punch states. Role-play illegal actions:

- Checkout without check-in  
- Double check-in  

### 4. Sequence — leave approval (20 min)

Trace: request → pending reserve → approve → daily summary leave hours = target.

### 5. Interface — FOSC export (25 min)

Discuss TEMPO shortfalls only. Why base hours **above** TEMPO are zeroed for discrepancy.

### 6. Reflection (15 min)

Each intern writes 5 bullets: “What SE practice would I steal for a radar SA project?”

## Deliverable (in-class)

Submit reflection bullets under **A6 professionalism** notes or bring paper to instructor.

## Instructor notes

- Prefer demo over slides.  
- If network fails, use screenshots / SE page alone.  
- Score engagement under A6.
