# NET-A01G — General Networking Brief

**Weight:** 10% · **Due:** After net-01-general · **Module:** net-01-general

## Prompt

Show **vendor-neutral** literacy: devices, layers, host services (DHCP/DNS/gateway), ports, and a test order. No Junos `set` lines required.

## Deliverables

1. **Device role table** for the welcome fabric (or your bench remap): each hostname → switch / router / firewall / PE / encryptor / host — one-line “why.”  
2. **Layer table** (5 rows): invent or reuse a symptom for Physical, Link, Internet, Transport, Application — first test for each.  
3. **Host services:** for PC `10.10.10.50/24` gateway `10.10.10.1` DNS `10.10.20.53`, explain DHCP vs static; what `169.254.x.x` would mean; what fails if DNS is wrong but the IP path is good.  
4. **Ports:** pick **five** from the module table (must include **443** and **53**) — service, protocol, and one sentence on mission/lab impact if blocked.  
5. **Test order:** user reports `https://app.ciss-lab.local` is down. Numbered list of **at least six** checks (name **and** IP, ping not last-and-only).  
6. **NAT vs firewall** — four sentences: what each does; why PAT is not a permit policy.

## Quality bar

- No vendor CLI dump as a substitute for the model.  
- Ping is not treated as application V&V.  
- Roles are not all labeled “router.”

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| literacy | 15 | Roles, layers, DHCP/DNS/gateway, NAT vs firewall |
| method | 10 | Sensible test order; ports accurate |
| communication | 5 | Tables a non-author intern can use |
