# ADMIN-A05 — Identity Lookup & Access Notes

**Weight:** 10% · **Due:** After admin-05-idm-ad-ipa · **Module:** admin-05-idm-ad-ipa

## Prompt

Practice **central identity** literacy (AD and/or FreeIPA) with safe lookup commands and a troubleshooting story.

## Deliverables

1. **Environment note:** which stack you can see in lab (AD, FreeIPA, neither — be honest) and how Linux would join it.
2. **Lookup evidence** (as available): `id`, `getent passwd|group`, and any of `realm list`, `klist`, `ipa` — paste what works; explain gaps.
3. **Access model table:** user → groups → what host/app access those groups should imply (lab-fictional OK if labeled).
4. **Incident story (½ page):** “user cannot log in / wrong groups” — timeline, hypotheses, tests, fix/escalation.
5. **HBAC/sudo awareness:** 5 bullets on least privilege.

## Quality bar

- You do not invent admin rights you do not have.
- Evidence is primary; guesses are labeled.
- Privacy: no password hashes or personal data dumps.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| evidence | 15 | Real lookups or honest constraints |
| troubleshooting | 10 | Structured incident story |
| communication | 5 | Clear access model |
