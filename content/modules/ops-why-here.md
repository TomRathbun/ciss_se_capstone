# Why You Are Here

> **Audience:** every intern, every track. Week 1 Monday, first **60 minutes**, **one room**.  
> **Then** you split into SE / SW / NET / ADMIN for the rest of the day.  
> **Classification:** unclassified / open source. No live sensors, no real tracks, no basing.

## Learning outcomes

After 60 minutes you can:

- Say in one sentence **why CISS exists** (a picture that is true)  
- Recite a **dated** public snapshot of the **28 February 2026** raids — without treating it as a scoreboard  
- Name **how the UAE defended itself** (layered AD) and **Lockheed Martin’s public role** (THAAD / AN/TPY-2), without claiming a vendor “did the intercepts”  
- Place **EADGE-T** as the named ground C2 / SA environment this pathway sits next to — and **PRSAS** as the classroom shape, not the system  
- Name the **four rooms plus integrators and SMEs** that keep the same pixels honest  
- Point to **weeks 10–11** (military, everyone) and **weeks 14–18** (PRSAS, everyone)  
- Repeat the integrity line: **this lab is not live C2**

## The sentence

A country stays up because someone is watching a **picture**, and that picture is **true**.

Not because a slide said “situational awareness.” Because a radar plot became a **track**, the track was **fused** with a second sensor, an operator **said what they saw**, and a commander trusted the glass enough to act.

You were hired into four rooms. The rooms are not four internships. They are four ways of keeping **the same pixels honest**.

| Room | What “honest” means here |
|------|--------------------------|
| **SE** | The picture has a CONOPS, needs, ICDs, and tests — not a hope |
| **SW** | The simulator, fusion daemon, and glass do what the ICD said |
| **NET** | The path the picture rides is the path you designed, not a spare VLAN |
| **ADMIN** | The hosts, certs, and clocks are the ones the glass believes |
| **MIL** (weeks 10–11, then 15) | The voice on the floor does not over-claim |

## Recap — 28 February 2026 (open source)

From **28 February 2026**, Iran launched ballistic missiles, cruise missiles, and drones at the UAE. The Ministry of Defence, via **WAM** and on-the-record briefings, said UAE air force and air defence **detected and intercepted** the large majority of those raids.

Interns do **not** memorize a scoreboard. Numbers in official updates **moved by the day**. You will use **one dated snapshot** so you can talk in public language, then you will stop counting.

### Snapshot the instructor cites (do not quiz this)

**Source:** UAE MoD government media briefing, **3 March 2026**, carried by **WAM**. Spokesperson: Maj. Gen. Abdulnasser Al Humaidi. Figures are **since the attacks began on 28 February**, as of that briefing.

| Class | Detected | Intercepted / destroyed | Other (as stated) |
|-------|----------|-------------------------|-------------------|
| Ballistic missiles | 186 | 172 | 13 fell into the sea; **1** impacted UAE territory |
| UAVs / drones | 812 | 755 | **57** fell within the country |
| Cruise missiles | 8 | 8 | — |

**Casualties in that same briefing:** 3 fatalities and 68 injuries, plus minor-to-moderate damage to civilian facilities. MoD said sounds heard across the country were **interceptions** (air defence and fighter aircraft), and that some harm was from **defensive operations**, not only from weapons that got through. Defence is not a video game. This module will not pretend otherwise.

### Figures moved — that is the teaching point

A later **MoD** statement (**29 March 2026**) said that since 28 February, UAE air defences had **engaged 414 ballistic missiles, 15 cruise missiles, and 1,914 UAVs**. Open-source cumulatives in May were higher still. You will **not** be asked which number is “the” number. You will be asked what had to exist **before** any of those engagements:

1. **Sensors and a picture** — overlapping coverage, not a single heroic radar.  
2. **A ground environment** that fused those sensors into something a commander could trust.  
3. **People** — operators, maintainers, engineers, integrators, SMEs — who kept the picture honest under load.

If a slide in this course ever shows a percentage with no date and no source, it is a fail. Same rule as inventing a basing map.

## How the UAE defended itself

Public, layered air and missile defence. High, medium, and short. Soft-kill as well as hard-kill. Fighters as well as batteries. **Not** one system.

| Layer (open-source vocabulary) | Public family | What it is for in this room |
|--------------------------------|---------------|-----------------------------|
| Upper-tier BMD | **THAAD** (Lockheed Martin) | High-altitude / terminal ballistic intercept theme |
| Long / medium SAM | **Patriot** PAC-2 / PAC-3 themes (Raytheon) | Mid-tier atmospheric layer |
| SHORAD / point | **Pantsir** family and other short-range systems (see **ops-uae-military** in week 10) | Low-altitude, UAV, cruise, aircraft |
| Soft-kill / EW | UAE industry, including **EDGE** public claims (May 2026: locally developed jammers / EW against a large share of drones) | Industry statement, **not** an MoD scoreboard. Date-stamp it if you repeat it. |
| Air | UAE fighters (MoD: jets engaged drones and cruise) | The picture is also for aircrew, not only for a battery |

**Do not** assign a raid to a battery. **Do not** invent intercept rates. **Do not** draw a real site. Week 10 will give you the platform vocabulary. Today you only need: **layered**, **fused**, **people**.

## Lockheed Martin’s public role

Lockheed Martin is a **50-year** UAE partner. Public, on-the-record facts you may put on a slide:

| Public fact | What it means here |
|-------------|--------------------|
| UAE was **THAAD’s first FMS** customer. First hardware delivered **October 2015**. | A long integration, not a weekend install |
| A THAAD battery includes launchers, interceptors, an **AN/TPY-2** radar, and fire control | Sensors + C2 + effectors. A picture is **not** a missile |
| THAAD’s **first operational intercepts** were publicly reported in the UAE in **January 2022** | The architecture was exercised before 2026 |
| LM continues FMS sustainment / launcher work on the UAE THAAD case (public MDA contract actions into 2026) | Industry **provides and sustains**. UAE Armed Forces **operate** |

**The line you will not cross:** Lockheed Martin did not “do the intercepts.” UAE air force and air defence engaged the raids. Patriot, SHORAD, fighters, EDGE EW, maintainers, and a ground C2 were in the same architecture. One OEM does not get the war.

## EADGE-T — the named ground environment

**EADGE-T** (Emirates Air Defence Ground Environment — Tactical) is the **named UAE Air Force Air Defence ground C2 / situational-awareness environment** — the picture-fusion layer this intern pathway sits next to.

The name sits in the same **unclassified** family as NATO’s publicly documented **NADGE** (NATO Air Defence Ground Environment): radars in, a ground environment that fuses them, a picture a commander can act on.

| This course says | This course does **not** say |
|------------------|------------------------------|
| EADGE-T is the named ground C2 / SA environment | FOC dates, site names, Link-16 employment, message catalogues |
| A fused picture needs **overlapping** sensor coverage and a dual-feed rule | Battery maps, ROE, live tracks |
| **PRSAS** is the **classroom shape** of that idea | “We are building EADGE-T” / “we built the UAE missile shield” |

You will not configure EADGE-T. You will not see its internals. You will build **PRSAS**: two simulated radars, a path, a daemon, a glass — so that overlapping coverage, dual-feed correlation, and an honest **COAST** call are muscle memory **before** you stand next to a real ground environment.

## It was a collective effort

The 2026 defence was not a vendor demo and not a single trade. It was **network engineers, systems engineers, software engineers, integrators, and subject-matter experts**, plus the operators and maintainers on the floor.

| Who | What they kept honest | CISS room |
|-----|----------------------|-----------|
| **Network engineers** | The path the picture rides (routing, encryption, allow-lists) | **NET** |
| **Systems engineers** | CONOPS, needs, ICDs, integration, test | **SE** |
| **Software engineers** | Fusion, correlation, glass, simulators, C2 software | **SW** |
| **Integrators** | The seams between sensors, weapons, and the ground environment | SE + vendors + AFAD — you will practice this in weeks 14–18 |
| **Administrators / hosts** | Clocks, certs, VMs, the machine the glass believes | **ADMIN** |
| **Subject-matter experts** | The operator voice; what the picture is **for** | **MIL** (weeks 10–11, then 15) |

If any one of those trades is sloppy, the glass still lights up. That is how people die with a green screen.

## How the 18 weeks are built

```text
Week 1 Monday     ALL-HANDS opener (this module, 60 min)
                  then four rooms for the rest of the term

Weeks 1–9         Your track’s craft (parallel rooms)

Weeks 10–11       MILITARY — common. UAE context, CONOPS/AOC, ATO, A5.
                  Every intern. Not an SE add-on.

Weeks 12–13       Leftover craft + SE living case / SA framing

Weeks 14–18       PRSAS — joint capstone. You will watch the teaching
                  picture on week-14 Monday, then build your piece.
```

Military stays **together**. We do not sprinkle ATO into week 4. ATO planning and ATO execution are a chain; A5 is one card. You will be ready for that language after nine weeks of craft.

## What you are *not* doing today

| Today | Later |
|-------|--------|
| Hear why the picture matters, with one dated recap | Weeks 10–11: learn AOC / ATO vocabulary and public platform families |
| See a **teaching** air picture (projector) with **overlapping** radar coverage | Week 14: **ops-prsas-intro** — why PRSAS, after you have the ops words |
| Split into your room | Weeks 14–18: put your craft on the same three-site lab |

Do **not** research classified order-of-battle, basing, ROE, or real unit tracks. The course already has an open-source UAE context module for week 10.

## Projector (instructor)

Play the **teaching picture** (stylized gulf, two overlapping coverage volumes, fused track). Say out loud:

1. Remote A and Remote B are **sensors**. Their coverage disks **overlap on purpose**. The gold lens is **dual-feed** — the only place fusion can be honest.  
2. Central is **fusion + glass** — the classroom stand-in for a ground environment like **EADGE-T**, not EADGE-T itself.  
3. The lines between them are **a path that can lie** if NET or ADMIN is sloppy.  
4. The operator’s job is to **say COAST when the plot died**, not to decorate the screen.  
5. After the film: the **3 March 2026** snapshot, Lockheed Martin’s public THAAD role, the collective-effort table. **Do not quiz the numbers.**

<video class="prsas-film" autoplay muted loop playsinline controls poster="/static/images/prsas/teaching-picture.jpg">
  <source src="/static/images/prsas/picture.mp4" type="video/mp4">
</video>
<p class="prsas-caption">Projector film · overlapping coverage · dual-feed lens · CISS-TEACH · fictional theater</p>

<object class="prsas-live" type="image/svg+xml" data="/static/images/prsas/live-picture.svg" aria-label="Live teaching picture — two overlapping radars, dual-feed fusion">
  <img src="/static/images/prsas/teaching-picture.jpg" alt="PRSAS teaching picture — overlapping RSA/RSB coverage, dual-feed lens, unclassified classroom architecture">
</object>
<p class="prsas-caption">Live teaching picture · RSA ∩ RSB = dual-feed · not a basing map</p>

## 10-minute floor exercise

Each intern writes **one line** in the notebook, then reads it if called:

> “My track keeps this picture honest by ________.”

Wrong answers sound like “I will configure stuff” or “I like Java.”  
Right answers name a **failure mode**: bad ICD, unsigned cert, wrong VLAN, silent dual-feed conflict, operator who calls a squawk a hostile.

## Integrity (non-negotiable from minute one)

| Allowed | Not allowed |
|---------|-------------|
| Classroom picture, simulated feeds, **overlapping** teaching coverage | Live AD sensors, real tracks, real IFF Mode 4/5 |
| Public MoD / WAM language with a **date** (3 Mar 2026 snapshot; later cumulatives as “figures moved”) | Inventing intercept rates, battery maps, ROE, or a final scoreboard |
| Lockheed Martin as **THAAD OEM + 50-year partner**; UAE Armed Forces as **operator** | “LM shot down the missiles” / “we built the UAE missile shield” |
| **EADGE-T** as the named ground C2 this pathway sits next to | EADGE-T internals, FOC, data-link employment, site names |
| “We will build the *shape* of a picture” (**PRSAS**) | “We are building EADGE-T” |
| Casualties, including interception debris, as civic memory | Treating defence as a highlight reel |

## Next

You split. Learn your craft like it will be on the glass in week 14 — because it will.

| When | What |
|------|------|
| Rest of today | Track welcome + first lab |
| Weeks 10–11 | **ops-uae-military** → **ops-00** → ATO → A5. Everyone. |
| Week 14 Monday | **ops-prsas-intro** (motivation + picture) then **se-12** (contracts) |
