"""Write weeks 1–4 foundation + week 5 kickoff markdown."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lesson_lib import assignment, lesson

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "content" / "modules"
ASG = ROOT / "content" / "assignments"
ALL = "All interns (weeks 1–4)"


def w(kind: str, id_: str, body: str) -> None:
    folder = MOD if kind == "modules" else ASG
    path = folder / f"{id_}.md"
    path.write_text(body.rstrip() + "\n", encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


def main() -> None:
    # ----- SE F01 -----
    w("modules", "se-f01-what-se-is", lesson(
        title="What SE is",
        when="Week 1 · Monday afternoon · Masdar",
        who=ALL,
        assignment_id="se-fa01-what-se-is",
        assignment_title="SE definition and failure map",
        due="Week 1 Tuesday morning",
        outcomes=[
            "Explain systems engineering in one paragraph a non-engineer can use",
            "Name the early chain: Vision → Needs → Use cases → Requirements",
            "Spot the intern failure mode: jumping to design",
            "Say what an artifact is (owner, version, date)",
        ],
        why="Every intern on CISS will sit in a room with software, network, and admin work. If you cannot say what problem we are solving, those rooms build the wrong thing. This afternoon is the shared language — not a specialty school.",
        teach="""**Systems engineering** is the discipline of making sure we understand the real-world problem, capture what the system must do, design something that can be built and tested, integrate the pieces, and prove we met the need — across hardware, software, people, and process.

It is not “drawing diagrams.” Diagrams are tools. The product is **decisions under evidence**, recorded as **artifacts**.

### Early chain (memorize this)

```text
VISION  →  NEEDS  →  USE CASES  →  REQUIREMENTS
 shared     who/why    how people     what the system
 picture    benefit    use it         shall do
```

| Link | From → To | Meaning |
|------|-----------|---------|
| **derives_from** | Need → Vision | The need is justified by the vision |
| **traces_to** | Need → Use case | The need is realized by a goal-oriented interaction |
| **allocated_to** | Use case → Requirement | The use case is specified by shall-statements |

**Design comes later.** Starting with a solution is the most common intern mistake. Architecture, states, and ICDs wait until the problem is clear.

### Artifacts

Every artifact has an **owner**, a **date**, a **version**, and a **classification** (for us: unclassified). A slide with no owner is not an artifact. A secret sketch in a notebook is not an artifact.

### Why programs fail (the list you will reuse)

| Failure mode | Missing artifact |
|--------------|------------------|
| Built the wrong thing | Vision / needs |
| Nobody agrees who it is for | Stakeholders |
| Happy path only | Use-case extensions |
| “It should be fast” | Testable requirement + AC |
| Two teams, two interfaces | ICD |
| “We tested it” with no mapping | RTM / V&V |

Use **public** failure stories (Therac-25, Mars Climate Orbiter units, 737 MAX MCAS as public reporting). Do not invent classified ones.""",
        exercise="In pairs: pick a daily app (maps, badge, banking). Write one sentence each for vision, need, use case, and a shall. Label one design choice *design — not a requirement*. Swap and mark mixed layers.",
        hold="Architecture views, state machines, ICDs, MBSE frameworks, and the PRSAS problem. Week 5 opens the project.",
    ))

    w("assignments", "se-fa01-what-se-is", assignment(
        code="SE-FA01", title="SE definition and failure map",
        time="2 hours", due="Week 1 Tuesday morning, before the Networking lecture",
        module="se-f01-what-se-is", weight="8%",
        prompt="Prove you can explain SE, walk the early chain, and map a **public** failure to a missing artifact. Unclassified sources only. Cite URLs.",
        deliverables="""1. **One-paragraph definition** of systems engineering (≤ 120 words).
2. **Chain walk** for a daily app you use (not PRSAS, not a design):

   | Layer | One sentence |
   |-------|----------------|
   | Vision | |
   | Need (`As … we need … so that …`) | |
   | Use case (actor + goal) | |
   | One shall | |
   | One **design** choice, labeled *design — not a requirement* | |

3. **Public failure map** (Therac-25, Climate Orbiter, or another public case from the lesson): case, URL, what went wrong (4–6 lines), missing artifact, what that artifact would have forced into the open.
4. **Trace sentence** using *derives_from / traces_to / allocated_to* on *your* daily-app example.""",
        quality="Layers are not mixed. The case cites a real public URL. Design is labeled so it cannot be mistaken for a requirement.",
    ))

    w("assignments", "se-fa00-professional", assignment(
        code="SE-FA00", title="Professionalism & participation",
        time="Ongoing", due="Ongoing — scored across the 36 weeks",
        module="se-f01-what-se-is", weight="8%",
        prompt="Show up prepared, turn morning work in on time, help peers without doing their work, and keep unclassified discipline.",
        deliverables="""No single document. Instructors score from attendance, on-time morning packets, Thursday/Friday questions, and integrity incidents.""",
        quality="Own work. Cited sources. No secrets in Git. No classified content in course tools.",
    ))

    # ----- SE F02 -----
    w("modules", "se-f02-needs-usecases", lesson(
        title="Needs → use cases",
        when="Week 2 · Monday afternoon · Masdar",
        who=ALL,
        assignment_id="se-fa02-needs-usecases",
        assignment_title="Needs and two use-case briefs",
        due="Week 2 Tuesday morning",
        outcomes=[
            "Write a need as As … we need … so that …",
            "Turn a need into a use case with actor, goal, and main success scenario",
            "Write at least one extension (failure/alternate path)",
            "Reject a use case that is really a design",
        ],
        why="Requirements written without needs become a wishlist. Use cases without extensions become happy-path fiction. This afternoon is how people actually use a system — still not how we will build it.",
        teach="""### Needs grammar

```text
As  <stakeholder>,
we need  <capability>,
so that  <outcome they care about>.
```

Bad: “As a user we need a Kubernetes cluster so that it is modern.”
Good: “As a supervisor we need one defensible air picture so that we do not brief two different tracks as truth.”

Needs **derives_from** the vision. If you cannot point at the vision sentence, it is not a need yet.

### Use cases

A **use case** is a goal-oriented interaction: an **actor** wants an **outcome**.

| Field | Put this |
|-------|----------|
| Name | Verb-noun, goal-shaped (`Correlate dual feeds`) |
| Actor | Who is trying |
| Goal | What success looks like |
| Main success scenario | Numbered steps, no UI chrome |
| Extensions | `3a` if the second feed disagrees… |

**traces_to:** need → use case. One need can fan out.

### Reject list

A use case is **not**: a screen layout, a vendor name, a protocol, a class name, “make it fast.” Those are design or NFRs. Write them down as *rejected — design* so they do not sneak back in.""",
        exercise="Take yesterday’s daily-app vision. Write two needs in grammar. Turn one into a use case with a main scenario (5–8 steps) and one extension. Reject one fake use case that is actually a design.",
    ))

    w("assignments", "se-fa02-needs-usecases", assignment(
        code="SE-FA02", title="Needs and two use-case briefs",
        time="2 hours", due="Week 2 Tuesday morning, before the Networking lecture",
        module="se-f02-needs-usecases", weight="8%",
        prompt="Stay on the **same daily app** from SE-FA01 (or switch once, and say so). Do not jump to PRSAS yet.",
        deliverables="""1. **Vision restated** in one sentence (from FA01 or improved).
2. **Three needs** in `As … we need … so that …` grammar. Mark which vision they derive_from.
3. **Use-case index** (name, actor, goal) with at least three rows.
4. **Two full briefs**: main success scenario + at least one extension each.
5. **One rejected use case** labeled *design / not a use case* and why.
6. **Trace table:** need → use case (traces_to).""",
        quality="No UI widgets in the needs. Extensions are real alternate paths, not ‘error happens.’ A peer could write a shall from your brief.",
    ))

    # ----- SE F03 -----
    w("modules", "se-f03-requirements", lesson(
        title="Requirements that can be tested",
        when="Week 3 · Monday afternoon · Masdar",
        who=ALL,
        assignment_id="se-fa03-requirements",
        assignment_title="Six testable shalls",
        due="Week 3 Tuesday morning",
        outcomes=[
            "Write a shall that can be tested without a meeting",
            "Use an EARS pattern (WHEN / WHILE / IF-THEN / ubiquitous)",
            "Write an acceptance criterion in Given/When/Then that proves a shall",
            "Keep design out of the requirement",
        ],
        why="‘The system shall be user-friendly’ cannot be failed. Interns who cannot write a testable shall cannot later write an ICD or a lab procedure. This is the last foundation SE skill before we learn to *read* architecture.",
        teach="""A **requirement** says what the system **shall** do. It stands alone. The acceptance criterion **proves** it; it does not explain it.

### EARS patterns (use the names)

| Pattern | Shape |
|---------|--------|
| Ubiquitous | The system shall … |
| Event-driven | WHEN \<event\> the system shall … |
| State-driven | WHILE \<state\> the system shall … |
| Unwanted | IF \<condition\> THEN the system shall … |

Give every FR an **ID** (`FR-FA03-01`). NFRs (latency, availability, classification of the lab) get IDs too.

### Acceptance criteria

```text
Given <precondition>
When  <action>
Then  <observable result>
```

The Then must be something a tester can see or log — not “the user is happy.”

### Design smuggling

If your shall names Java, Junos, Postgres, or a screen widget, you wrote a design. Put it in a decision record later. The shall stays about behavior.

SE-allocated_to: use case → requirement. Next week we only *read* structure. We do not allocate yet.""",
        exercise="From one use-case extension last week, write two EARS shalls (one IF/THEN) and one AC. Peer marks any shall that needs the AC to be understood.",
    ))

    w("assignments", "se-fa03-requirements", assignment(
        code="SE-FA03", title="Six testable shalls",
        time="2 hours", due="Week 3 Tuesday morning, before the Networking lecture",
        module="se-f03-requirements", weight="8%",
        prompt="Write testable requirements for the same daily-app (or a tiny unclassified lab helper). Not PRSAS yet.",
        deliverables="""1. **Six FRs** with IDs, EARS pattern tags, and shall text. Include at least one WHEN, one WHILE, and one IF/THEN.
2. **Two NFRs** with IDs (e.g. time-to-display, availability of the lab).
3. **Three ACs** in Given/When/Then, each pointing at an FR-ID.
4. **One labeled design** you refused to put in a shall, and why.
5. **Trace:** two FRs allocated_to named use cases from FA02.""",
        quality="A stranger can fail the shall without calling you. ACs do not add hidden rules. No vendor/UI smuggling.",
    ))

    # ----- SE F04 -----
    w("modules", "se-f04-reading-the-system", lesson(
        title="Reading the system",
        when="Week 4 · Monday afternoon · Masdar",
        who=ALL,
        assignment_id="se-fa04-reading-system",
        assignment_title="Context sketch and V&V note",
        due="Week 4 Tuesday morning",
        outcomes=[
            "Read a context diagram (who is outside the box)",
            "Tell structure (containers) from deployment (VMs)",
            "Read a simple sequence and a simple state",
            "Say verify vs validate in one sentence each",
            "Explain how SE will coordinate Network, Admin, and Software",
        ],
        why="Next week we open PRSAS. You must be able to look at a picture and not confuse ‘who talks to whom’ with ‘which VM it runs on’ with ‘what we will test.’",
        teach="""### Three views (do not mix them)

| View | Question it answers |
|------|---------------------|
| **Context** | Who/what is outside our system? |
| **Structure / containers** | What major pieces exist and what they owe each other? |
| **Deployment** | Where does it run? (For CISS: **VMs**, not Docker-first) |

A sequence diagram is **behavior over time**. A state machine is **legal vs illegal modes**. You do not need SysML fluency this week. You need to *read* them.

```text
Actor → Client → Daemon → Database
         │          │
         └─ messages over a broker
```

### Verify vs validate

| | Question |
|--|----------|
| **Verify** | Did we build it right? (tests against shalls) |
| **Validate** | Did we build the right thing? (operator / stakeholder) |

A passing unit test that nobody wanted is verified and not validated.

### How SE coordinates the other three

| Track | SE asks them for |
|-------|------------------|
| Software | Implementation of shalls and ICDs |
| Networking | Path, ports, protection matching NFRs |
| Admin | Runtime (VMs, identity, certs) that V&V can stand on |

SE does not write Junos or Java as the system of record. SE owns the **shared contracts** the others build against.""",
        exercise="Given a three-box sketch (client, daemon, DB): label context vs structure vs deployment. Write one sequence (login → load → live update). Write one verify activity and one validate activity for a shall from last week.",
        hold="Full architecture allocation, hierarchical states, messaging ICDs, MBSE frameworks. Depth starts week 6. PRSAS itself is next Monday.",
    ))

    w("assignments", "se-fa04-reading-system", assignment(
        code="SE-FA04", title="Context sketch and V&V note",
        time="2 hours", due="Week 4 Tuesday morning, before the Networking lecture",
        module="se-f04-reading-the-system", weight="8%",
        prompt="Show you can read and produce the cheap pictures SE will use on PRSAS — still on your daily-app or a tiny lab helper.",
        deliverables="""1. **Context diagram** (boxes + actors/external systems). One paragraph in/out of scope.
2. **Structure vs deployment:** two lists — pieces vs VMs/processes. Do not mix.
3. **One sequence** (5–8 messages) for a success path.
4. **V&V table** for three FRs from FA03: FR-ID, verify activity, validate activity.
5. **Coordination note (8–10 lines):** one thing SE will need from Network, from Admin, and from Software when a real project starts.""",
        quality="Views are distinct. Verify ≠ validate. No PRSAS invention — that is next week.",
    ))

    # ----- NET F01-F04 -----
    w("modules", "net-f01-how-built", lesson(
        title="How a network is built",
        when="Week 1 · Tuesday afternoon · Masdar",
        who=ALL,
        assignment_id="net-fa01-how-built",
        assignment_title="Path and device-roles sheet",
        due="Week 1 Wednesday morning",
        outcomes=[
            "Describe LAN vs WAN in vendor-neutral language",
            "Say what a switch, router, and firewall each do",
            "Use OSI / TCP-IP enough to name which layer is failing",
            "Draw a path from a user to a service",
        ],
        why="Software and sensors only matter if packets arrive, in order, on the allowed path. Interns who jump to Junos cannot tell a wrong mask from a dead DNS from a blocked port.",
        teach="""A **network** is nodes exchanging messages under agreed addresses and rules.

| Word | Meaning |
|------|---------|
| Host | PC, server, VM — source or destination |
| Hop | A router or L3 firewall the packet is forwarded through |
| Path | Ordered hops from source to destination |
| LAN | One site / broadcast-domain family |
| WAN | Links **between** sites |

```text
PC → Switch → Gateway/firewall → WAN → Remote gateway → Server
```

| Role | Forwards on | Job |
|------|-------------|-----|
| Switch (L2) | MAC + VLAN | Many hosts in a LAN |
| Router (L3) | IP prefix | Next hop between subnets |
| Firewall | IP + port + policy | Allow/deny (often NAT too) |

**Layers you need this week:** L2 delivery, L3 hops, L4 ports, application names (DNS, HTTPS). If you cannot draw the path, you cannot debug it.

SE link: host, port, and path are interface / NFR fields. A path sketch is a cheap context diagram.""",
        exercise="Draw the path from a laptop on a user VLAN to a database VM on a server VLAN through a firewall. Label switch, router/firewall, WAN-or-not. Name one failure that is L2 vs L3 vs L4.",
        hold="Junos commit model, OSPF, BGP, MPLS, IPsec. Depth after week 4.",
        additional_of="net-01-general",
    ))

    w("assignments", "net-fa01-how-built", assignment(
        code="NET-FA01", title="Path and device-roles sheet",
        time="2 hours", due="Week 1 Wednesday morning, before the Software lecture",
        module="net-f01-how-built", weight="7%",
        prompt="Prove you can talk about a network without a vendor CLI.",
        deliverables="""1. **Path drawing** (boxes + arrows) from a user PC to a server through at least one switch and one firewall. Caption each hop’s role.
2. **Device-roles table** (switch / router / firewall / host) with one sentence each.
3. **Two failure stories:** “cannot ping gateway” and “HTTPS times out but ping works.” Name the layer you would suspect first and why.
4. **SE sentence:** how this path would show up on a context diagram.""",
        quality="Vendor-neutral. Path is a path, not a brand list. Layers are not guessed at random.",
    ))

    w("modules", "net-f02-addressing", lesson(
        title="Addressing",
        when="Week 2 · Tuesday afternoon · Masdar",
        who=ALL,
        assignment_id="net-fa02-addressing",
        assignment_title="Readable address plan",
        due="Week 2 Wednesday morning",
        outcomes=[
            "Read an IPv4 address, mask, and default gateway",
            "Explain DHCP and DNS in operational terms",
            "Say what a subnet is *for*",
            "Write a tiny address plan a peer can implement",
        ],
        why="Most intern outages are addressing: wrong gateway, overlapping subnets, DNS that lies. You will not design OSPF this week. You will write a plan someone else can type.",
        teach="""**IPv4** `10.10.20.15/24` means host `.15` on network `10.10.20.0`, 256 addresses, typical gateway `10.10.20.1`.

| Piece | Job |
|-------|-----|
| Address | Who I am |
| Mask / prefix | Who is “local” |
| Default gateway | Who I send to when it is not local |
| DHCP | Hands out address + gateway + DNS |
| DNS | Names → addresses |

A **subnet** exists to bound a broadcast domain, apply policy, and make plans readable — not to look clever.

**Write plans as tables**, not paragraphs:

| VLAN | Subnet | Gateway | Use |
|------|--------|---------|-----|
| 10 | 10.10.10.0/24 | .1 | Users |
| 20 | 10.10.20.0/24 | .1 | Servers |

CISS labs reuse teaching blocks (management `10.255.0.0/24`, site users, site servers). Instructor may remap — **write the live values in your notebook**.""",
        exercise="Fill a three-row plan (users, servers, management) for a fictional Masdar lab closet. Pick gateways. List three hosts with names and IPs. Peer tries to find an overlap or a missing gateway.",
        additional_of="net-01-foundations",
    ))

    w("assignments", "net-fa02-addressing", assignment(
        code="NET-FA02", title="Readable address plan",
        time="2 hours", due="Week 2 Wednesday morning, before the Software lecture",
        module="net-f02-addressing", weight="7%",
        prompt="Write an address plan a sysadmin could type without calling you.",
        deliverables="""1. **Plan table:** at least users, servers, management — VLAN, subnet, gateway, use.
2. **Three hosts** with hostname, IP, mask, gateway, DNS.
3. **DHCP vs static:** which of those hosts should be static and why.
4. **One naming rule** (e.g. `pc-user-01`) and one thing you will **not** overlap.
5. **Failure:** what a host looks like if the gateway is wrong vs if DNS is wrong.""",
        quality="No overlapping subnets. Gateway sits in the subnet. A peer can read it in two minutes.",
    ))

    w("modules", "net-f03-on-the-wire", lesson(
        title="Conversations on the wire",
        when="Week 3 · Tuesday afternoon · Masdar",
        who=ALL,
        assignment_id="net-fa03-on-the-wire",
        assignment_title="Ports and allowed-path table",
        due="Week 3 Wednesday morning",
        outcomes=[
            "Choose TCP vs UDP for a given conversation",
            "Name common ports (SSH, HTTPS, DNS, AMQP)",
            "Explain VLAN and NAT as ideas, not configs",
            "State the allowed-path mindset",
        ],
        why="Firewalls and brokers fail in port language. If you cannot say ‘ActiveMQ TLS is 61617 on the allowed path,’ you cannot help Software or Admin.",
        teach="""**TCP** is a conversation with setup and acknowledgment. **UDP** is a datagram — DNS questions often live here; streaming and some tunnels too.

| Service | Typical port | Transport |
|---------|--------------|-----------|
| SSH | 22 | TCP |
| HTTPS | 443 | TCP |
| DNS | 53 | UDP (and TCP) |
| PostgreSQL | 5432 | TCP |
| ActiveMQ OpenWire TLS (PRSAS later) | **61617** | TCP |

**VLAN:** a LAN sliced into separate L2 domains. **NAT:** rewriting addresses so private hosts can talk out (or, badly, hiding too much).

**Allowed-path mindset:** the path that is *permitted* is the one we document. Everything else is deny. “It works if we disable the firewall” is not a design.

Hold Junos `set security policies` until depth. Today is the *idea*.""",
        exercise="For SSH, DNS, HTTPS, and a message broker: transport, port, and whether a user VLAN should reach it. Draw one allowed path and one path you would deny.",
    ))

    w("assignments", "net-fa03-on-the-wire", assignment(
        code="NET-FA03", title="Ports and allowed-path table",
        time="2 hours", due="Week 3 Wednesday morning, before the Software lecture",
        module="net-f03-on-the-wire", weight="7%",
        prompt="Show you can describe conversations without a vendor policy stanza.",
        deliverables="""1. **Port table** for SSH, HTTPS, DNS, PostgreSQL, and a message broker — transport, port, who initiates.
2. **TCP vs UDP:** two sentences on when you would pick each.
3. **VLAN in one paragraph** and **NAT in one paragraph** (ideas, not CLI).
4. **Allowed-path sketch** for: user PC → HTTPS client; simulator → broker. One explicit deny.
5. **SE/ICD note:** why a port belongs in an interface description.""",
        quality="Ports are right. Deny is written, not implied. No Junos yet — and that is correct.",
    ))

    w("modules", "net-f04-test-path", lesson(
        title="Test before you guess",
        when="Week 4 · Tuesday afternoon · Masdar",
        who=ALL,
        assignment_id="net-fa04-test-path",
        assignment_title="Evidence pack for a dead path",
        due="Week 4 Wednesday morning",
        outcomes=[
            "Order tests: local → gateway → name → port → application",
            "Say what ping and traceroute actually prove",
            "Write an evidence pack a peer can reuse",
            "Treat change control as part of networking",
        ],
        why="‘It doesn’t work’ is not a ticket. Guessing OSPF on a week-4 intern is how labs burn down. This afternoon is the method you will still use on Junos in week 12.",
        teach="""**Test order (default):**

1. Is *my* interface up and addressed?
2. Can I reach the **gateway**?
3. Does the **name** resolve (if we used a name)?
4. Does the **port** answer (not just ICMP)?
5. Does the **application** complete?

**Ping** proves ICMP to an address, not that 61617 works. **Traceroute** shows hops that *answer traceroute*, not the full policy.

Evidence pack: command, timestamp, excerpt, what you conclude, what you will try next. One hypothesis at a time.

**Change control:** even in a lab, write what you will change, how you will know, and how you will undo. `commit confirmed` is a depth skill; the *habit* starts now.

Hold: Junos `show` cheatsheets, traceoptions, blast-radius clears.""",
        exercise="Symptom: ‘the web page never loads, ping to the server IP works.’ Write the ordered tests. Peer adds the test you skipped.",
        hold="Junos, OSPF, BGP, MPLS, IPsec — week 6+ for those who stay in Networking.",
    ))

    w("assignments", "net-fa04-test-path", assignment(
        code="NET-FA04", title="Evidence pack for a dead path",
        time="2 hours", due="Week 4 Wednesday morning, before the Software lecture",
        module="net-f04-test-path", weight="7%",
        prompt="Symptom given: a user can ping 10.10.20.10 but cannot open HTTPS on that host, and the name `app.lab.example` sometimes fails.",
        deliverables="""1. **Ordered test list** (at least six steps) with the command you would run at intern level.
2. **What ping proved** and **what it did not**.
3. **Two hypotheses** (name vs port vs policy) and what evidence would confirm each.
4. **Change-control card** for one experimental change: intent, success signal, undo.
5. **Ticket summary** (8 lines) a peer could pick up.""",
        quality="No guessing OSPF. No ‘restart everything.’ Evidence before action.",
    ))

    # ----- SW F01-F04 -----
    w("modules", "sw-f01-git", lesson(
        title="Git as daily craft",
        when="Week 1 · Wednesday afternoon · Masdar",
        who=ALL,
        assignment_id="sw-fa01-git",
        assignment_title="Git daily-loop evidence",
        due="Week 1 Thursday morning",
        outcomes=[
            "Clone, branch, commit, push without folklore",
            "Name a branch after a ticket",
            "Recover from a mistake without destroying history you share",
            "Write a commit message a reviewer can use",
        ],
        why="Every discipline will touch Git. Network configs, admin scripts, SE markdown, and Java all live in history. If you cannot branch safely, you cannot work on a team.",
        teach="""**Daily loop**

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

Do not commit secrets, PCAP with keys, or classified diagrams.""",
        exercise="In the course repo (or a sandbox): create a branch, add a one-line file, commit, show `log -1`. Instructor watches for `main` commits.",
        additional_of="sw-01-git",
    ))

    w("assignments", "sw-fa01-git", assignment(
        code="SW-FA01", title="Git daily-loop evidence",
        time="2 hours", due="Week 1 Thursday morning, before the Admin lecture",
        module="sw-f01-git", weight="8%",
        prompt="Prove the daily loop with command evidence. Use a sandbox or the assigned GitLab project — not a secret dump of SDC repos.",
        deliverables="""1. **Command log** (copy/paste) of: clone or fetch, new branch named for a fake ticket, edit, commit, push.
2. **`git log -3 --oneline`** excerpt.
3. **Recovery note:** how you would undo the last commit *if it was not pushed* vs *if it was pushed*.
4. **One bad commit message** and the rewritten good one.
5. **Integrity:** what you will never commit.""",
        quality="Evidence is real. Branch is not `main`. Recovery does not say `force push to main`.",
    ))

    w("modules", "sw-f02-team-change", lesson(
        title="How a team ships a change",
        when="Week 2 · Wednesday afternoon · Masdar",
        who=ALL,
        assignment_id="sw-fa02-team-change",
        assignment_title="Ticket → MR checklist",
        due="Week 2 Thursday morning",
        outcomes=[
            "Walk ticket → branch → merge request → main",
            "Write a review comment that would catch a real defect",
            "Map program tools (Jira/Bitbucket) to CISS lab (GitLab)",
            "Refuse to merge your own unchecked work",
        ],
        why="A brilliant patch on `main` with no ticket is how labs become folklore. The habit is the same whether you are changing Java or a markdown ICD.",
        teach="""```text
PROGRAM:  Jira DR-123 → branch DR-123 → Bitbucket PR → Jenkins → main
CISS LAB: ticket DR-123 → branch DR-123 → GitLab MR → pipeline → main
```

A **merge request** (lab) / **pull request** (program) is the review surface: what changed, why, how to test, what you did not do.

Review comments that help: “This shall is now untested — where is the AC?” Comments that do not: “Looks good” on 400 lines.

You do not merge your own unchecked work. If you are alone in a lab, you still fill the checklist and wait for a peer or instructor.""",
        exercise="Draft an MR description for yesterday’s Git file. Peer writes two review comments: one useful, one useless. Discuss.",
        additional_of="sw-02-bitbucket-jira",
    ))

    w("assignments", "sw-fa02-team-change", assignment(
        code="SW-FA02", title="Ticket → MR checklist",
        time="2 hours", due="Week 2 Thursday morning, before the Admin lecture",
        module="sw-f02-team-change", weight="8%",
        prompt="Show the workflow, not a novel about Git internals.",
        deliverables="""1. **Fake ticket** with ID, title, acceptance in two bullets.
2. **Branch name** derived from that ID.
3. **MR/PR description** (why, how to test, out of scope).
4. **Review checklist** (8–10 boxes) that would catch a real defect in code *or* a markdown ICD.
5. **Program vs lab table:** ticket, git host, review button, CI.
6. **Rule you will follow** when you are the only intern in the room.""",
        quality="Checklist is specific. Description would let a peer press merge without Slack.",
    ))

    w("modules", "sw-f03-reading-code", lesson(
        title="Reading and writing code",
        when="Week 3 · Wednesday afternoon · Masdar",
        who=ALL,
        assignment_id="sw-fa03-reading-code",
        assignment_title="Requirement vs code vs secret",
        due="Week 3 Thursday morning",
        outcomes=[
            "Read a short function and say what requirement it implements",
            "State the hiring bar: Python may be how you think; Java is the contract language",
            "Keep secrets out of Git",
            "Refuse to invent a requirement in code",
        ],
        why="Interns ship clever code that nobody asked for. SE just taught you shalls. Software’s job is to implement them — in the language the program pays for.",
        teach="""**Python** is allowed as a scratchpad. **Java** is what JDBC, JMS/ActiveMQ, daemons, and JavaFX labs will use. After the depth bridge module, graded work is Java.

When you read code, ask:

1. What shall is this?
2. What happens on failure?
3. Where would a secret leak?
4. What would a test look like?

```text
Requirement  →  code  →  test that can fail the shall
     ↑                        |
     └── if the code invents behavior, stop and write a shall
```

Secrets: connection passwords, private keys, tokens. Environment or a secrets file that is **gitignored**, never a screenshot in a ticket.""",
        exercise="Instructor shows a 15-line function (any language). Class: shall it implements, one failure path, one secret risk.",
        hold="JDBC pools, ActiveMQ resource adapters, JavaFX, Jenkins. Depth.",
        additional_of="sw-03-python-java",
    ))

    w("assignments", "sw-fa03-reading-code", assignment(
        code="SW-FA03", title="Requirement vs code vs secret",
        time="2 hours", due="Week 3 Thursday morning, before the Admin lecture",
        module="sw-f03-reading-code", weight="8%",
        prompt="Use the sample snippet in this assignment folder or a 15-line function you write. Not a framework dump.",
        deliverables="""1. **The function** (paste or link).
2. **Shall it implements** (one EARS sentence, or ‘none — this is design-only’ and stop).
3. **Failure path** in three bullets.
4. **Secret-handling:** where a password could leak and how you would not do that.
5. **Hiring-bar note:** one thing that is different in Java (types, `equals`, packages) even if you thought in Python.
6. **Integrity:** one example of code inventing a requirement, and what you would do instead.""",
        quality="The shall could be tested. No real passwords. Honest about Java as the destination.",
    ))

    w("modules", "sw-f04-services", lesson(
        title="Services, not scripts",
        when="Week 4 · Wednesday afternoon · Masdar",
        who=ALL,
        assignment_id="sw-fa04-services",
        assignment_title="Service conversation sketch",
        due="Week 4 Thursday morning",
        outcomes=[
            "Sketch a process that talks to a database",
            "Sketch a process that publishes or consumes a message",
            "List ICD fields before anyone writes a parser",
            "Place those processes on VMs, not as Docker-first",
        ],
        why="PRSAS is not a notebook script. It is simulators, a daemon, a broker, a database, and a client. This afternoon is the shape — not JDBC.",
        teach="""A **service** is a long-running process with a clear job, a failure story, and a contract.

```text
Producer  →  broker topic  →  consumer / daemon  →  database
                                      ↓
                                   client
```

**ICD before parser:** field name, type/units, who sends, who receives, rate, what happens when it is late. SE owns the contract language; Software implements it.

CISS runtime: **VMs** (vSphere guests). Docker may appear later as a PoC, not as the default.

Hold: connection pools, JMS factories, JavaFX threads, Jenkins.""",
        exercise="Boxes: simulator, broker, daemon, DB, client. Label one ICD between simulator and daemon (five fields). Label who owns each box (SW/NET/ADMIN/SE).",
    ))

    w("assignments", "sw-fa04-services", assignment(
        code="SW-FA04", title="Service conversation sketch",
        time="2 hours", due="Week 4 Thursday morning, before the Admin lecture",
        module="sw-f04-services", weight="8%",
        prompt="Draw the shape of a small lab system. You may preview PRSAS names (radar.input) but do not invent classified fields.",
        deliverables="""1. **Diagram:** at least producer, broker, consumer, database, client.
2. **ICD table** (six fields): name, meaning, who Tx, who Rx, rate or ‘on change’, drop policy.
3. **DB sentence:** what is stored vs what is only in the live message.
4. **VM note:** which processes share a VM vs need their own (your call, with a reason).
5. **Owner map:** SE / SW / NET / ADMIN for each box.""",
        quality="ICD is a contract, not a Java class. No Docker-first default. Owners do not all say ‘software.’",
    ))

    # ----- ADMIN F01-F04 -----
    w("modules", "admin-f01-linux-vm", lesson(
        title="Linux on a VM",
        when="Week 1 · Thursday afternoon · Masdar",
        who=ALL,
        assignment_id="admin-fa01-linux-vm",
        assignment_title="Host literacy sheet",
        due="Week 1 Friday morning",
        outcomes=[
            "Treat the lab runtime as a RHEL-class VM, not a laptop container",
            "Navigate filesystem, users, processes",
            "Use systemctl to ask whether a service is up",
            "Practice least privilege",
        ],
        why="Software ‘works on my laptop’ and then dies on the guest. Admin is the runtime. Everyone needs enough Linux to not be helpless at 16:00 on a Thursday.",
        teach="""CISS labs: **virtual machines** under vSphere / ESXi, typically **RHEL 7-class** or compatible. `docker run` in an external tutorial translates to: service on the assigned VM, `systemctl status`, correct hostname.

| You must be able to | Commands (examples) |
|---------------------|---------------------|
| Where am I | `pwd`, `ls`, `cd` |
| Who am I | `id`, `whoami` |
| What is running | `ps`, `systemctl status …` |
| What just happened | `journalctl -u … -n 50` |

Least privilege: your user + limited `sudo`. Do not disable SELinux “to see if it helps” on a shared host.

SE link: the VM *is* a deployment-view element.""",
        exercise="On the assigned VM (or a documented equivalent): `id`, `hostname`, `systemctl status` for one service, `df -h`. Write the four answers in your notebook.",
        additional_of="admin-01-rhel7-linux",
    ))

    w("assignments", "admin-fa01-linux-vm", assignment(
        code="ADMIN-FA01", title="Host literacy sheet",
        time="2 hours", due="Week 1 Friday morning, before any Friday flex session",
        module="admin-f01-linux-vm", weight="7%",
        prompt="Work on a VM. If you only have a laptop, say so and use a VM the instructor named — not Docker as the default.",
        deliverables="""1. **Host sheet:** hostname, OS (`/etc/redhat-release` or equivalent), your username, `id` excerpt.
2. **Filesystem:** where you are allowed to write; where you are not.
3. **One service:** `systemctl status` excerpt (redact secrets).
4. **Least-privilege note:** one thing you needed sudo for and one thing you did not.
5. **Translation:** how you would rewrite a `docker run postgres` tutorial for this VM.""",
        quality="Evidence looks like a VM. No ‘it works on Windows.’ No disabled SELinux as a flex.",
    ))

    w("modules", "admin-f02-see-machine", lesson(
        title="See what the machine is doing",
        when="Week 2 · Thursday afternoon · Masdar",
        who=ALL,
        assignment_id="admin-fa02-see-machine",
        assignment_title="Evidence pack for a symptom",
        due="Week 2 Friday morning",
        outcomes=[
            "Read logs without drowning",
            "Run symptom → hypothesis → test",
            "Tell incident vs change vs request",
            "Build an evidence pack a peer can reuse",
        ],
        why="The difference between a useful intern and a dangerous one is whether they paste 4,000 lines of log or a hypothesis with a 20-line excerpt.",
        teach="""**Method:** symptom (observable) → hypothesis (one) → test (command) → next hypothesis.

Tools for this afternoon: `journalctl`, `tail`, `grep`, `less`, `ps`, `ss`. You do not need to be a DBA.

**Tickets**

| Kind | Use |
|------|-----|
| Incident | Something is broken |
| Change | You will alter a system |
| Request | Please give me access / a VM |

A ticket without evidence is a rumor.

Hold: deep `strace`, tcpdump on shared hosts without permission.""",
        exercise="Symptom: ‘I cannot SSH.’ Three hypotheses (service down, firewall, wrong key). What command tests each? Write a four-field ticket: symptom, last change, evidence, ask.",
        additional_of="admin-09-troubleshooting",
    ))

    w("assignments", "admin-fa02-see-machine", assignment(
        code="ADMIN-FA02", title="Evidence pack for a symptom",
        time="2 hours", due="Week 2 Friday morning, before any Friday flex session",
        module="admin-f02-see-machine", weight="7%",
        prompt="Pick one: cannot SSH, service won’t start, or disk looks full. If you cannot reproduce, write the pack against a *described* lab symptom and label it as a dry run.",
        deliverables="""1. **Symptom** in one sentence (observable).
2. **Three hypotheses** and the command that would confirm each.
3. **Evidence excerpt** (≤ 20 lines, redacted) or a labeled dry-run excerpt.
4. **Ticket** with type (incident/change/request), fields filled.
5. **What you will not do** (restart host, disable SELinux, tcpdump on a shared span).""",
        quality="One hypothesis at a time. Excerpts are short. Ticket type is correct.",
    ))

    w("modules", "admin-f03-software-host", lesson(
        title="Software on the host",
        when="Week 3 · Thursday afternoon · Masdar",
        who=ALL,
        assignment_id="admin-fa03-software-host",
        assignment_title="Install and secret-handling note",
        due="Week 3 Friday morning",
        outcomes=[
            "Explain how a package gets onto a RHEL-class VM",
            "Reject ‘works on my laptop’ as a deployment",
            "Keep secrets out of Git and screenshots",
            "Treat snapshots as a rollback idea",
        ],
        why="Software builds jars. Admin makes them run tomorrow after a reboot. If you cannot say where the bits came from, you cannot rebuild the lab.",
        teach="""**Packages:** `yum`/`rpm` on the guest; language ecosystems (Maven, pip, npm) still land *on the VM*. Nexus is the org hub when configured.

Deployment means: bits on the **assigned host**, service enabled, config outside the jar, secrets not in Git.

**Snapshots** (vSphere) are a rollback idea, not a backup strategy. Know when a snapshot is allowed; do not snapshot a full database as folklore.

Hold: writing Ansible roles, vSAN design, FreeIPA.""",
        exercise="Trace ‘install PostgreSQL’ from package source → files on disk → systemd unit → who owns the data directory. Where would a password accidentally get committed?",
        additional_of="admin-03-package-management",
    ))

    w("assignments", "admin-fa03-software-host", assignment(
        code="ADMIN-FA03", title="Install and secret-handling note",
        time="2 hours", due="Week 3 Friday morning, before any Friday flex session",
        module="admin-f03-software-host", weight="7%",
        prompt="Describe a real install path for one service (postgres, httpd, or the lab broker). VM-first.",
        deliverables="""1. **Install path:** package name, command, how you would verify files/units.
2. **Config vs bits:** what is in the package vs what you would change locally.
3. **Secret handling:** three places a password must not live; one acceptable place (idea-level).
4. **Laptop translation:** how a Docker tutorial maps to this VM.
5. **Snapshot:** one sentence on when you would ask for one before a change.""",
        quality="Rebuildable. No secrets in the write-up. No ‘I’ll just copy from my laptop.’",
    ))

    w("modules", "admin-f04-trust-identity", lesson(
        title="Trust and identity",
        when="Week 4 · Thursday afternoon · Masdar",
        who=ALL,
        assignment_id="admin-fa04-trust-identity",
        assignment_title="Certificate one-pager",
        due="Week 4 Friday morning",
        outcomes=[
            "Explain a certificate, a key, and a chain in one page",
            "Say why every box should not have its own password file",
            "Connect admin trust work to SE V&V",
            "Hold FreeIPA, vSAN, and Ansible for depth",
        ],
        why="PRSAS will use TLS on the broker and logins for the client. If ‘certificate’ is a magic word, you will block Software next month.",
        teach="""A **certificate** binds a **public key** to a name (and SANs), signed by a **CA**. The **private key** stays private. A **chain** is leaf → intermediates → trust anchor.

When TLS fails, look at: names, clocks (expiry), and whether the client **trusts** the CA — before you regenerate everything.

**Identity:** people and services should come from a **central** source (AD / FreeIPA in depth) so sudo, groups, and offboarding work. Local `root` passwords on twelve VMs is how intern labs rot.

SE V&V: “clients authenticate” is a shall. Admin produces the **evidence** (login works with the issued cert; `openssl` inspect).

Hold: issuing a lab CA, IPA replicas, HBAC design.""",
        exercise="On paper: leaf cert for `amq-c-01`. What SAN must it have? Who trusts it? What shall does that prove?",
        additional_of="admin-04-tls-certs",
        hold="FreeIPA, vSAN, Ansible, NFS Kerberos — week 6+ for those who stay in Admin.",
    ))

    w("assignments", "admin-fa04-trust-identity", assignment(
        code="ADMIN-FA04", title="Certificate one-pager",
        time="2 hours", due="Week 4 Friday morning, before any Friday flex session",
        module="admin-f04-trust-identity", weight="7%",
        prompt="Explain trust well enough that a software intern can use it. Unclassified lab CA ideas only.",
        deliverables="""1. **Diagram or numbered list:** key, cert, chain, trust store.
2. **Failure table:** expiry, name mismatch, untrusted CA — symptom vs what you inspect.
3. **Identity paragraph:** why not a local password on every VM.
4. **V&V:** one shall from SE-FA03 (or a generic ‘client shall authenticate’) and the admin evidence you would attach.
5. **Hold list:** three things you are *not* doing this week (IPA, vSAN, Ansible) and why that is correct.""",
        quality="One page-ish. No private keys pasted. Names and clocks appear in the failure table.",
    ))

    # ----- Week 5 kickoff -----
    w("modules", "se-k01-prsas-overview", lesson(
        title="PRSAS capstone overview",
        when="Week 5 · Monday afternoon · Masdar",
        who="All interns (all-hands, including those who will later drop electives)",
        assignment_id="se-ka01-overview",
        assignment_title="PRSAS one-minute brief",
        due="Week 5 Tuesday morning",
        outcomes=[
            "Restate UC-CISS_PROJECT-001 in one minute",
            "Name the three VMware stacks and what lives on each",
            "Point at shared contracts (topics, ports, teaching payload)",
            "Keep unclassified / VM-first discipline",
        ],
        why="Specialization without a shared problem produces four intern projects. This afternoon is the whole picture before anyone picks an elective.",
        teach="""**PRSAS** — Prototype Radar Situational Awareness System. Unclassified lab. Not a live C2.

Two simulated radars (Remote A, Remote B) publish ASTERIX-*like* Category 062 messages (Mode 3/A present) across a secured path to Central: ActiveMQ (`radar.input`) → track daemon → PostgreSQL → `radar.output` → authenticated client.

Read the live module [se-12-prsas-overview](/modules/se-12-prsas-overview) after class. Contracts freeze there: ports (**61617** TLS), topics, CISS-TEACH-1 JSON payload. Do not claim official ASTERIX encoding.

Electives open **next week**. SE remains mandatory. Networking, Software, and Admin continue only if you stay in those rooms.

Military lectures remain Friday-flex and **TAA-gated** — not part of this kickoff.""",
        exercise="In four mixed groups: 60-second brief of the picture with no notes. Peer group marks anything that sounded like a live air-defense system.",
        additional_of="se-12-prsas-overview",
    ))

    w("assignments", "se-ka01-overview", assignment(
        code="SE-KA01", title="PRSAS one-minute brief",
        time="2 hours", due="Week 5 Tuesday morning, before the Networking kickoff",
        module="se-k01-prsas-overview", weight="6%",
        prompt="Share Tuesday morning with SE-KA02 (about one hour each). Write the brief you would give a visiting engineer. Unclassified. No live sensors.",
        deliverables="""1. **One-minute script** (≤ 180 words).
2. **Three-site table:** Remote A, Remote B, Central — what runs where.
3. **Contracts:** topics, port 61617, payload name (CISS-TEACH-1).
4. **Owner map:** SE / SW / NET / ADMIN in one table (from the overview).
5. **Out of scope:** two things PRSAS is not.""",
        quality="Could be read aloud. No C2 over-claim. Contracts match the overview module.",
    ))

    w("modules", "se-k02-se-work", lesson(
        title="SE work on the capstone",
        when="Week 5 · Monday afternoon (second half) · Masdar",
        who="All interns; SE will live with this list for the rest of the program",
        assignment_id="se-ka02-se-work",
        assignment_title="SE accomplishment list",
        due="Week 5 Tuesday morning",
        outcomes=[
            "List what SE must produce for PRSAS",
            "Separate SE artifacts from Java and Junos",
            "Name the first week-6 SE assignment",
        ],
        why="If SE does not own CONOPS, schema, and V&V, Software will invent them in code.",
        teach="""**SE must accomplish**

- CONOPS (stakeholders, threads, unwanted paths, in/out of scope)
- MBSE artifacts: sequence, hybrid track lifecycle, logical components
- PostgreSQL track schema (Mode 3/A as correlation key)
- V&V / lessons-learned and a virtualization study vs the VM baseline

**SE does not** ship production Java or Junos commits.

Shared contracts (topics, ports, payload) are SE-facilitated and **frozen** for other tracks.

Week 6 depth starts architecture views on this problem. Capstone modules [se-13](/modules/se-13-prsas-conops) onward are the long form.""",
        exercise="Write the SE backlog on the board: artifact, first due week, who reviews it. Class votes on the one most likely to be skipped — that one gets an owner.",
        additional_of="se-13-prsas-conops",
    ))

    w("assignments", "se-ka02-se-work", assignment(
        code="SE-KA02", title="SE accomplishment list",
        time="2 hours", due="Week 5 Tuesday morning, before the Networking kickoff",
        module="se-k02-se-work", weight="6%",
        prompt="Turn the SE work statement into a backlog you could run.",
        deliverables="""1. **Backlog table:** artifact, why it exists, week you think it is due, reviewer (SE/instructor).
2. **Not-SE list:** three things you will refuse to own (Java, Junos, IPA).
3. **First week-6 output:** what you will bring to Monday architecture.
4. **Risk:** one way SE can block SW/NET/ADMIN if late.""",
        quality="Artifacts are named, not slogans. Dates are plausible. Ownership is not ‘the team.’",
    ))

    w("modules", "net-k01-net-work", lesson(
        title="Networking work on the capstone",
        when="Week 5 · Tuesday afternoon · Masdar",
        who="All interns this week; elective from week 6",
        assignment_id="net-ka01-net-work",
        assignment_title="NET accomplishment list",
        due="Week 5 Wednesday morning",
        outcomes=[
            "List what Networking must produce for PRSAS",
            "Name topology, firewall/IPsec, and validation as separate jobs",
            "Ask SE for the ports/topics freeze",
        ],
        why="Without a documented path, simulators have nowhere to send.",
        teach="""**Networking must accomplish**

- Three-site topology (VLANs, addressing, EX/SRX placement)
- Least-privilege firewalls and two site-to-site IPsec tunnels onto Central
- Path validation that **61617** works, plus negative tests
- A replayable configuration guide

**Networking does not** write app code or keep CA private keys in tickets.

Depth starts Junos next week for those who stay. Live capstone modules: [net-11](/modules/net-11-prsas-topology) onward.""",
        exercise="Sketch Remote A / B / Central as three clouds. Mark the two tunnels. Write the one port you must prove. List three questions for SE/Admin.",
        additional_of="net-11-prsas-topology",
    ))

    w("assignments", "net-ka01-net-work", assignment(
        code="NET-KA01", title="NET accomplishment list",
        time="2 hours", due="Week 5 Wednesday morning, before the Software kickoff",
        module="net-k01-net-work", weight="9%",
        prompt="Turn the networking work statement into a backlog and a question list.",
        deliverables="""1. **Backlog:** topology, firewalls/IPsec, validation, config guide — outcome and dependency.
2. **Question list** for SE (contracts) and Admin (VMs/port groups) — at least five.
3. **Prove-it:** how you will show 61617 without claiming ping is enough.
4. **Not-NET list:** app schema, IPA, JavaFX.""",
        quality="Dependencies are named. Ping is not the whole test.",
    ))

    w("modules", "sw-k01-sw-work", lesson(
        title="Software work on the capstone",
        when="Week 5 · Wednesday afternoon · Masdar",
        who="All interns this week; elective from week 6",
        assignment_id="sw-ka01-sw-work",
        assignment_title="SW accomplishment list",
        due="Week 5 Thursday morning",
        outcomes=[
            "List simulator, daemon, client, integration as four jobs",
            "Refuse to invent the schema or the ICD",
            "See containers as a later PoC, not the default runtime",
        ],
        why="Three applications, one picture. If Software starts with a GUI, the daemon and ICD lose.",
        teach="""**Software must accomplish**

- Radar-message simulators on Remote A and B (CISS-TEACH-1, TLS to `radar.input`)
- Track-processing daemon (Mode 3/A correlate, persist, `radar.output`)
- Authenticated SA client (bulk load + live)
- Integration test card; container PoC of two components for the SE virt study

**Software does not** invent the Postgres schema without SE or talk to live radars.

Depth starts the Java bridge next week for those who stay. Live modules: [sw-09](/modules/sw-09-prsas-simulator) onward.""",
        exercise="Order the four jobs. Name the SE artifact each one requires before code. Name the NET/ADMIN artifact each one requires before it can run.",
        additional_of="sw-09-prsas-simulator",
    ))

    w("assignments", "sw-ka01-sw-work", assignment(
        code="SW-KA01", title="SW accomplishment list",
        time="2 hours", due="Week 5 Thursday morning, before the Admin kickoff",
        module="sw-k01-sw-work", weight="12%",
        prompt="Four software jobs, in order, with blockers from other tracks.",
        deliverables="""1. **Four-job backlog** with order and a one-line success for each.
2. **Blockers table:** SE / NET / ADMIN thing you need before you can run it.
3. **ICD humility:** three fields you will not invent.
4. **Runtime:** VM-first sentence; when Docker is allowed.""",
        quality="GUI is not job one. Blockers are specific.",
    ))

    w("modules", "admin-k01-admin-work", lesson(
        title="Admin work on the capstone",
        when="Week 5 · Thursday afternoon · Masdar",
        who="All interns this week; elective from week 6",
        assignment_id="admin-ka01-admin-work",
        assignment_title="Admin accomplishment list",
        due="Week 5 Friday morning",
        outcomes=[
            "List VM provision, identity/certs, harden/automate as separate jobs",
            "See rebuildability as the test of admin work",
            "Keep keys out of Git",
        ],
        why="If the stack cannot be rebuilt, the demo is a snowflake.",
        teach="""**Admin must accomplish**

- VM provisioning on the correct port groups; snapshot discipline
- Identity (FreeIPA/OpenLDAP) and lab certificates for AMQ TLS and clients
- Host hardening (firewalld, SELinux, audit) aligned to the allow-list
- Enough automation (Ansible or PowerCLI) that the stack can be rebuilt

**Admin does not** treat Junos policy as the system of record.

Depth starts bash/TLS/IPA for those who stay. Live modules: [admin-11](/modules/admin-11-prsas-provision) onward.""",
        exercise="Inventory the VMs you think exist (sim-a, sim-b, amq, daemon, db, idm, client). Mark who needs a cert. Mark who needs to be on which VLAN — as questions for NET.",
        additional_of="admin-11-prsas-provision",
    ))

    w("assignments", "admin-ka01-admin-work", assignment(
        code="ADMIN-KA01", title="Admin accomplishment list",
        time="2 hours", due="Week 5 Friday morning, before any Friday flex session",
        module="admin-k01-admin-work", weight="8%",
        prompt="Turn admin work into a rebuildable backlog.",
        deliverables="""1. **Backlog:** provision, identity/certs, harden, automate — outcome and dependency on NET/SE/SW.
2. **VM inventory draft** (names, role, questions still open).
3. **Key handling rule** you will print above the desk.
4. **Rebuild test:** how you would know the automation worked.""",
        quality="Inventory is a table. Secrets policy is explicit. Rebuild is a test, not a hope.",
    ))


if __name__ == "__main__":
    main()
