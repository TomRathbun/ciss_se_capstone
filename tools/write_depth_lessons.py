"""Write week 6+ depth lessons and 2-hour morning assignments."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lesson_lib import assignment, lesson

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "content" / "modules"
ASG = ROOT / "content" / "assignments"

SE_WHO = "All interns (SE is mandatory for the full program)"
EL_NET = "Networking elective + anyone still attending"
EL_SW = "Software elective + anyone still attending"
EL_AD = "Admin elective + anyone still attending"


def w(kind: str, id_: str, body: str) -> None:
    folder = MOD if kind == "modules" else ASG
    (folder / f"{id_}.md").write_text(body.rstrip() + "\n", encoding="utf-8")
    print("wrote", kind, id_)


def depth_pair(
    *,
    mod_id: str,
    asg_id: str,
    title: str,
    when: str,
    who: str,
    code: str,
    asg_title: str,
    due: str,
    weight: str,
    additional_of: str,
    outcomes: list[str],
    why: str,
    teach: str,
    exercise: str,
    prompt: str,
    deliverables: str,
    hold: str | None = None,
) -> None:
    w("modules", mod_id, lesson(
        title=title, when=when, who=who,
        assignment_id=asg_id, assignment_title=asg_title, due=due,
        outcomes=outcomes, why=why, teach=teach, exercise=exercise,
        additional_of=additional_of, hold=hold,
    ))
    w("assignments", asg_id, assignment(
        code=code, title=asg_title, time="2 hours", due=due,
        module=mod_id, weight=weight, prompt=prompt,
        deliverables=deliverables,
        quality="Tied to PRSAS where possible. Unclassified. Two-hour time box respected.",
    ))


def main() -> None:
    depth_pair(
        mod_id="se-d01-architecture", asg_id="se-da01-architecture",
        title="Architecture views & allocation",
        when="Week 6 · Monday afternoon · Masdar", who=SE_WHO,
        code="SE-DA01", asg_title="Architecture views pack",
        due="Week 6 Tuesday morning", weight="8%",
        additional_of="se-05-architecture",
        outcomes=["Keep context, structure, and deployment as three views",
                  "Allocate FRs to real elements", "Record one design decision"],
        why="PRSAS now has a problem statement. Allocation is how Software, Network, and Admin receive work.",
        teach="""Context = boundary. Structure = pieces and responsibilities. Deployment = VMs/processes/networks.

FRs are **allocated_to** structure elements, not to 'the cloud.' A design decision records *what we chose, what we rejected, why*.

PRSAS structure you should expect to see: simulators, broker, daemon, DB, client, firewall/encryptor, identity/CA.""",
        exercise="On the board: three views of PRSAS. Allocate FR 'WHEN a Cat062-like message arrives the daemon shall persist a track' to an element.",
        prompt="Produce views for PRSAS, not a generic web app.",
        deliverables="""1. Context diagram. 2. Structure diagram. 3. Deployment (VMs). 4. Allocation table for five FRs (write them if SE-KA has none yet). 5. One decision record (chosen / rejected / why).""",
    )
    depth_pair(
        mod_id="se-d02-behavior", asg_id="se-da02-behavior",
        title="Behavior — states & sequences",
        when="Week 7 · Monday afternoon · Masdar", who=SE_WHO,
        code="SE-DA02", asg_title="State + sequence",
        due="Week 7 Tuesday morning", weight="8%",
        additional_of="se-06-behavior",
        outcomes=["Separate state from status", "Write trigger/guard/activity",
                  "Draw one sequence that matches the state machine"],
        why="Track lifecycle (init / live / coast / drop / conflict) is a state machine whether anyone draws it or not.",
        teach="""**State** is a mode with legal transitions. **Status** is a field.

Transitions: trigger [guard] / activity.

PRSAS track lifecycle (teaching): no-track → live (on first plot) → coast (missed updates) → drop; conflict when two feeds disagree on Mode 3/A vs kinematics.

Sequence: plot in → daemon → DB write → output topic → client.""",
        exercise="Sketch hybrid state for one track. Peer names an illegal transition.",
        prompt="Use PRSAS track lifecycle, not a login screen.",
        deliverables="""1. State machine with at least four states and illegal-transition note. 2. Sequence (8–12 messages) for a dual-feed conflict. 3. FR mapping. 4. One rejected path.""",
    )
    depth_pair(
        mod_id="se-d03-interfaces", asg_id="se-da03-icd",
        title="Interfaces & ICDs",
        when="Week 8 · Monday afternoon · Masdar", who=SE_WHO,
        code="SE-DA03", asg_title="Partial messaging + API ICD",
        due="Week 8 Tuesday morning", weight="8%",
        additional_of="se-07-interfaces",
        outcomes=["Write a messaging ICD slice (content, Tx/Rx, rates)",
                  "Write an API ICD slice (ops, params, errors)",
                  "Refuse unofficial ASTERIX claims"],
        why="Parsers written without ICDs become folklore. CISS-TEACH-1 is the lab contract.",
        teach="""Messaging ICD: fields, units, who sends, who receives, rate, late/drop policy, version.

API ICD: operations, parameters, errors, auth.

PRSAS teaching payload is **JSON labeled CISS-TEACH-1**, ASTERIX-*like*, not edition-certified binary Cat 062. Read se-12 for the frozen fields.""",
        exercise="Fill six fields of radar.input (from CISS-TEACH-1). Write one API op for bulk load from Postgres.",
        prompt="Partial ICDs against PRSAS contracts.",
        deliverables="""1. Messaging ICD slice for radar.input (fields, Tx/Rx, rate, drop). 2. API ICD slice for bulk track load (one op + errors). 3. Version/owner. 4. Statement of what you are *not* claiming (official ASTERIX).""",
    )
    depth_pair(
        mod_id="se-d04-mbse", asg_id="se-da04-mbse",
        title="MBSE & architecture frameworks",
        when="Week 9 · Monday afternoon · Masdar", who=SE_WHO,
        code="SE-DA04", asg_title="MBSE literacy brief",
        due="Week 9 Tuesday morning", weight="8%",
        additional_of="se-11-mbse-frameworks",
        outcomes=["Contrast MBSE vs document piles", "UML vs SysML at intern level",
                  "Map our artifacts to OV/SV-style products without over-claiming"],
        why="You will hear DoDAF/NAF in the building. Literacy is required; a full UAF model is not this course.",
        teach="""MBSE: the model is the system of record, documents are views. We are **document-plus-diagram** honest: Mermaid/PlantUML in Git is not a SysML tool.

Map: context ~ OV-1/OV-2 flavour; sequences ~ OV-6c flavour; deployment ~ SV-1 flavour. Say 'flavour' — do not claim a completed DoDAF pack.""",
        exercise="Take three artifacts you already have. Map each to a framework product name and write the non-claim.",
        prompt="Literacy brief using your real artifacts.",
        deliverables="""1. MBSE vs documents in six lines. 2. UML vs SysML in six lines. 3. Mapping table of your artifacts. 4. Integrity: what you will not claim.""",
    )
    depth_pair(
        mod_id="se-d05-vv-trace", asg_id="se-da05-vv",
        title="Verification, validation & trace",
        when="Week 10 · Monday afternoon · Masdar", who=SE_WHO,
        code="SE-DA05", asg_title="Mini RTM",
        due="Week 10 Tuesday morning", weight="8%",
        additional_of="se-08-vv-trace",
        outcomes=["Build a small RTM", "Pick a verify method per FR", "Keep validate separate"],
        why="A demo is not a V&V program. PRSAS needs a matrix someone else could test.",
        teach="""RTM columns that work here: FR-ID, shall, design element, verify method, validate activity, status.

Verify methods: inspection, analysis, demonstration, test. 'We'll see in the GUI' is not a method until you say *what* you will see.

Validate: operator/supervisor can use the picture for the teaching scenario.""",
        exercise="Five FRs on the board. Class assigns a verify method. Argue about one.",
        prompt="RTM for PRSAS FRs you actually have.",
        deliverables="""1. RTM (≥5 FRs). 2. One paragraph validate approach. 3. One FR with no test yet — marked as a hole, not hidden.""",
    )
    depth_pair(
        mod_id="se-d06-etas", asg_id="se-da06-etas",
        title="Case study — SDC Time Tracker (ETAS)",
        when="Week 11 · Monday afternoon · Masdar", who=SE_WHO,
        code="SE-DA06", asg_title="ETAS artifact hunt",
        due="Week 11 Tuesday morning", weight="8%",
        additional_of="se-09-case-etas",
        outcomes=["Find real artifacts on a living system", "Steal habits for PRSAS"],
        why="PRSAS is still being built. ETAS already has requirements, states, and exports. Walk it.",
        teach="""Use the course case-study link (SDC Time Tracker /systems-engineering). Hunt FR-IDs, states, and an export/interface. Note BEOD-style boundary thinking.

Steal-list: what we will copy (IDs, traces, ACs) and what we will not (timekeeping domain).""",
        exercise="In the lab: open ETAS SE page. Each pair captures one FR and where it lands in the running app.",
        prompt="Hunt live artifacts; unclassified.",
        deliverables="""1. Three artifacts quoted (id + one sentence). 2. Boundary test you noticed. 3. Steal-list for PRSAS (≥5 items).""",
    )

    # NET depth
    net = [
        ("net-d01-junos", "net-da01-junos", "Junos CLI and the commit model", "Week 6", "NET-DA01",
         "Commit-model lab sheet", "net-02-junos-cli",
         "RE vs PFE; candidate vs active; `commit check`, `commit confirmed`, rollback. Older EX/SRX names. Never commit blind on a shared box.",
         "On paper: the steps from `configure` to `commit confirmed 5` and what happens if you walk away."),
        ("net-d02-switching", "net-da02-switching", "EX switching — VLANs, trunks, VC", "Week 7", "NET-DA02",
         "VLAN/trunk design", "net-03-switching",
         "Access vs trunk (port-mode vs ELS notes). RSTP. EX4200 Virtual Chassis as an idea. Handoff to the SRX.",
         "Design VLANs 10/20/99 on an EX closet. Mark trunks. Note VC split as a failure."),
        ("net-d03-srx", "net-da03-srx", "SRX firewalls — zones, policy, NAT", "Week 8", "NET-DA03",
         "Zone and policy sketch", "net-04-srx-firewall",
         "Zones, host-inbound-traffic, first-match policy, source NAT, `show security flow session`. Least privilege.",
         "Three zones (trust, untrust, vpn). One allow-list for 61617. What you `show` to prove it."),
        ("net-d04-ospf", "net-da04-ospf", "Interior routing — static and OSPF", "Week 9", "NET-DA04",
         "OSPF neighbor plan", "net-05-igp-ospf",
         "`show route` and preference. Statics. OSPF area 0, lo0 as router-id habit, neighbors. IGP as a gate for BGP/MPLS.",
         "Two SRX + one EX L3. Area 0. Expected neighbor state. What you will not do with a default-originate yet."),
        ("net-d05-bgp", "net-da05-bgp", "BGP — external and internal", "Week 10", "NET-DA05",
         "eBGP/iBGP map", "net-06-bgp",
         "eBGP vs iBGP. Neighbor states. Junos policy-statement export. local-pref, AS-path, next-hop-self.",
         "Tiny eBGP + iBGP sketch. One tight export. next-hop-self note."),
        ("net-d06-mpls", "net-da06-mpls", "MPLS tunnels — LDP, RSVP-TE, L3VPN", "Week 11", "NET-DA06",
         "LSP vs PE honesty sheet", "net-07-mpls",
         "LSPs as tunnels. LDP vs RSVP-TE. inet.3. VRF/RD/RT. Branch SRX is CE, not PE. Worksheet if the bench has only SRX210/240.",
         "Write the honesty sentence about your actual bench."),
        ("net-d07-ipsec", "net-da07-ipsec", "Encryptors and IPsec", "Week 12", "NET-DA07",
         "IPsec overlay sketch", "net-08-encryptors",
         "Route-based st0 on older SRX. Proxy-IDs. Red/black. Dedicated inline encryptor as a black box. PSK never in Git.",
         "Two tunnels onto Central. Overlay /30s. Redaction rule."),
        ("net-d08-ha-change", "net-da08-ha-change", "HA and change control", "Week 13", "NET-DA08",
         "Change window card", "net-09-ha-change",
         "commit confirmed, rescue, rollback. SRX cluster vocabulary. EX VC split. Change tickets.",
         "Write a 15-minute change card for adding one firewall rule."),
        ("net-d09-troubleshoot", "net-da09-troubleshoot", "Network troubleshooting on Junos", "Week 14", "NET-DA09",
         "Junos evidence pack", "net-10-troubleshoot",
         "Layered method on Junos `show`/`monitor`. Avoid traceoptions and blast-radius clears on old boxes.",
         "Symptom: 61617 dead, ping lives. Ordered Junos shows."),
    ]
    dues = {
        "Week 6": "Week 6 Wednesday morning",
        "Week 7": "Week 7 Wednesday morning",
        "Week 8": "Week 8 Wednesday morning",
        "Week 9": "Week 9 Wednesday morning",
        "Week 10": "Week 10 Wednesday morning",
        "Week 11": "Week 11 Wednesday morning",
        "Week 12": "Week 12 Wednesday morning",
        "Week 13": "Week 13 Wednesday morning",
        "Week 14": "Week 14 Wednesday morning",
    }
    for mid, aid, title, week, code, atitle, addl, teach, ex in net:
        depth_pair(
            mod_id=mid, asg_id=aid, title=title,
            when=f"{week} · Tuesday afternoon · Masdar", who=EL_NET,
            code=code, asg_title=atitle, due=dues[week], weight="7%",
            additional_of=addl,
            outcomes=[f"Apply {title.split('—')[0].strip()} at intern level on older Junos",
                      "Leave evidence, not folklore", "Keep PRSAS path in view"],
            why="Foundation taught packets. This afternoon is the vendor craft on the gear this program still runs.",
            teach=teach + "\n\nTie every example back to the three-site PRSAS fabric when you can. If the bench cannot do it, worksheet + instructor captures.",
            exercise=ex,
            prompt=f"Two-hour packet for {title}. Unclassified. No production keys.",
            deliverables="1. Design/procedure table. 2. Evidence or labeled worksheet. 3. PRSAS relevance (5–8 lines). 4. Safety: what you will not do on old boxes.",
            hold="Do not paste production configs. Redact PSKs.",
        )

    sw = [
        ("sw-d01-python-java", "sw-da01-python-java", "From Python to Java", "Week 6", "SW-DA01",
         "Python → Java translation", "sw-03-python-java",
         "Types, `equals` vs `==`, packages, Maven vs pip. Graded work is Java from here.",
         "Translate a 10-line Python function on the board to Java. Compile it if the lab is up."),
        ("sw-d02-java-tooling", "sw-da02-java-tooling", "VS Code for Java", "Week 7", "SW-DA02",
         "Runnable Maven mini-app", "sw-03-vscode-java",
         "JDK vs JRE, LTS, Java 8 baseline + upgrade path, Maven, run/debug in VS Code.",
         "Run a hello Maven app. Set a breakpoint. Screenshot or notes."),
        ("sw-d03-jdbc", "sw-da03-jdbc", "PostgreSQL with Java (JDBC)", "Week 8", "SW-DA03",
         "JDBC repository slice", "sw-04-java-postgresql",
         "PreparedStatement, transactions, pools (Hikari). Secrets not in source. JBoss datasource as awareness.",
         "Sketch schema + one insert/select with PreparedStatement. Rollback story."),
        ("sw-d04-amqp", "sw-da04-amqp", "AMQP messaging with Java", "Week 9", "SW-DA04",
         "Publish / consume lab", "sw-05-java-amqp",
         "JMS publish/consume on ActiveMQ. Ack modes. ICD-style payload. TLS 61617 on PRSAS.",
         "Producer and consumer roles on paper. Payload fields from CISS-TEACH-1."),
        ("sw-d05-daemons", "sw-da05-daemons", "Java daemons and background services", "Week 10", "SW-DA05",
         "Worker lifecycle sheet", "sw-06-java-daemons",
         "Long-running process, shutdown hooks, systemd unit, consumers that must not die silently.",
         "Write a systemd unit sketch and a shutdown sequence."),
        ("sw-d06-javafx", "sw-da06-javafx", "JavaFX for desktop GUIs", "Week 11", "SW-DA06",
         "Thin UI sketch", "sw-07-javafx-gui",
         "Stage/scene/layouts. UI-thread safety. Thin UI over services — no JDBC on the FX thread.",
         "Sketch the SA client: map, labels, conflict color. Mark the thread boundary."),
        ("sw-d07-cicd", "sw-da07-cicd", "CI/CD and Jenkins", "Week 12", "SW-DA07",
         "Pipeline map", "sw-08-jenkins-cicd",
         "Build-test-publish. Jenkins jobs/pipelines. Nexus. Map the same steps to GitLab CI for CISS.",
         "Draw program vs lab pipeline side by side."),
    ]
    sw_due = {f"Week {n}": f"Week {n} Thursday morning" for n in range(6, 13)}
    for mid, aid, title, week, code, atitle, addl, teach, ex in sw:
        depth_pair(
            mod_id=mid, asg_id=aid, title=title,
            when=f"{week} · Wednesday afternoon · Masdar", who=EL_SW,
            code=code, asg_title=atitle, due=sw_due[week], weight="8%",
            additional_of=addl,
            outcomes=[f"Perform {title} at intern level", "Keep VM-first runtime",
                      "Implement shalls, do not invent them"],
            why="Foundation taught Git and the shape of services. This is the Java craft PRSAS needs.",
            teach=teach,
            exercise=ex,
            prompt=f"Two-hour lab or worksheet for {title}.",
            deliverables="1. Working evidence or honest blocker. 2. Mapping to a PRSAS job. 3. Secret/integrity note.",
        )

    admin = [
        ("admin-d01-bash", "admin-da01-bash", "Bash programming for admins", "Week 6", "ADMIN-DA01",
         "Safe admin script", "admin-02-bash",
         "Quoting, args, `set -euo pipefail`, no `rm -rf` folklore. Scripts are change-controlled.",
         "Write a 20-line script that lists a unit and greps a pattern. Peer reviews quoting."),
        ("admin-d02-tls", "admin-da02-tls", "TLS certificate management", "Week 7", "ADMIN-DA02",
         "Inspect a cert chain", "admin-04-tls-certs",
         "CSR, leaf, chain, `openssl` inspect/verify, SAN, expiry, trust stores, AMQ TLS on PRSAS.",
         "Inspect a lab cert (or a public https cert) and fill name/expiry/SAN/issuer."),
        ("admin-d03-idm", "admin-da03-idm", "Identity — AD and FreeIPA", "Week 8", "ADMIN-DA03",
         "Identity design sketch", "admin-05-idm-ad-ipa",
         "Central identity. AD vs FreeIPA. SSSD, Kerberos, groups, HBAC, sudo. Login troubleshooting order.",
         "Principals for daemon, client user, admin. Where sudo lives."),
        ("admin-d04-nfs", "admin-da04-nfs", "NFS setup and configuration", "Week 9", "ADMIN-DA04",
         "Export/mount design", "admin-06-nfs",
         "Exports, mounts, NFSv3/v4, UID mapping, firewall, Kerberos-aware shares.",
         "One export line for a /24. UID risk. How you verify with `showmount`/`exportfs`."),
        ("admin-d05-vsphere", "admin-da05-vsphere", "vSphere, vSAN, VDI, and ESXi", "Week 10", "ADMIN-DA05",
         "VM lifecycle card", "admin-07-vsphere-vsan-vdi",
         "ESXi/vCenter vocabulary. VM lifecycle. Datastores/vSAN awareness. Port groups. Snapshot discipline.",
         "Lifecycle: create, clone, snapshot, delete — when each is allowed on PRSAS hosts."),
        ("admin-d06-postgres", "admin-da06-postgres", "PostgreSQL for admins", "Week 11", "ADMIN-DA06",
         "Admin SQL sheet", "admin-08-postgres-admin",
         "Roles vs databases. Activity, size, locks. Grants. Vacuum/backup awareness. Do not become the app developer.",
         "Queries you would run to see who is connected and whether the disk is filling."),
        ("admin-d07-troubleshoot", "admin-da07-troubleshoot", "Troubleshooting methodology", "Week 12", "ADMIN-DA07",
         "Host evidence pack", "admin-09-troubleshooting",
         "Deep `grep`/`tail`/`journalctl`/`ps`/`ss`. Evidence packs. Still one hypothesis at a time.",
         "Symptom: daemon up, nothing in DB. Host-level ordered tests."),
        ("admin-d08-tickets", "admin-da08-tickets", "Documentation and trouble tickets", "Week 13", "ADMIN-DA08",
         "Ticket and runbook", "admin-10-documentation-tickets",
         "Incident vs change vs request. Runbooks. Resolution notes. No classified content in the tool.",
         "Write a change ticket for issuing a replacement AMQ cert."),
    ]
    ad_due = {f"Week {n}": f"Week {n} Friday morning" for n in range(6, 14)}
    for mid, aid, title, week, code, atitle, addl, teach, ex in admin:
        depth_pair(
            mod_id=mid, asg_id=aid, title=title,
            when=f"{week} · Thursday afternoon · Masdar", who=EL_AD,
            code=code, asg_title=atitle, due=ad_due[week], weight="8%",
            additional_of=addl,
            outcomes=[f"Perform {title} at intern level on VMs",
                      "Leave rebuildable evidence", "Support PRSAS without owning Junos or Java"],
            why="Foundation taught host literacy. This is the admin craft the three-site lab needs.",
            teach=teach,
            exercise=ex,
            prompt=f"Two-hour admin packet for {title}. VM-first. Redact secrets.",
            deliverables="1. Procedure or design table. 2. Evidence excerpt or labeled dry-run. 3. PRSAS relevance. 4. Integrity note.",
        )


if __name__ == "__main__":
    main()
