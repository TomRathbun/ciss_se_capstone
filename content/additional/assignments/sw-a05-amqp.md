# SW-A05 — ActiveMQ Publish / Consume Lab

**Weight:** 15% · **Due:** After sw-05-java-amqp · **Module:** sw-05-java-amqp

## Prompt

Build a minimal **JMS/ActiveMQ** demo on the lab broker (or approved host): one producer, one consumer, ICD-style payload.

## Deliverables

1. **Payload ICD table:** field name, type, required?, example (JSON or map) — ≥ 4 fields.
2. **Producer** that sends ≥ 3 messages with distinct keys/ids.
3. **Consumer** that receives and logs/persists them (stdout OK if structured).
4. **Ack / session note:** which acknowledge mode you used and why (one short paragraph).
5. **Failure mode:** what happens if the consumer is down while producing (observed or reasoned with evidence).
6. Runbook: broker URL, queue/topic name, start order (broker → consumer → producer).

## Quality bar

- Payload is versionable (think ICD, not random strings only).
- Consumer is safe to re-run (idempotency note if you redeliver).
- No hard-coded production secrets.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| messaging | 15 | Produce + consume works end-to-end |
| interface_thinking | 10 | ICD-style payload + ack note |
| communication | 5 | Runbook peer-usable |
