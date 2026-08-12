# ADMIN-A04 — TLS Certificate Inspection Lab

**Weight:** 10% · **Due:** After admin-04-tls-certs · **Module:** admin-04-tls-certs

## Prompt

Inspect real or lab TLS endpoints/certs and explain trust failures in admin language.

## Deliverables

1. **Certificate report** for one endpoint or PEM: subject, issuer, SAN, notBefore/notAfter (OpenSSL commands shown).
2. **Chain check:** whether intermediate/root validation succeeds; what trust store you used.
3. **Three failure scenarios** (table): symptom, likely cause, first command to run — cover expiry, name mismatch, incomplete chain (at least).
4. **Ops impact note:** what breaks for HTTPS, DB SSL, or broker TLS when trust fails.
5. Redacted outputs only (no private keys ever).

## Quality bar

- Private keys are never pasted.
- Dates and hostnames are interpreted correctly.
- Advice is actionable for a ticket.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| inspection | 15 | Correct OpenSSL evidence |
| diagnosis | 10 | Failure scenarios accurate |
| communication | 5 | Ticket-ready notes |
