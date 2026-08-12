# A3c — System Description → Hierarchical State Chart

**Weight:** 5% · **Due:** Week 5 Thursday · **Module:** se-06 Behavior

## Prompt

From the **system description** below, build a **hierarchical (composite)** state machine. Then show that you still understand the flat semantics by listing the important transitions.

### System description — Field radio session (unclassified teaching scenario)

A portable radio session works as follows:

- The radio powers up into **Off**.  
- Operator action **power_on** enters **Powered**. While powered, the radio is always in exactly one of: **Idle**, **Receiving**, or **Transmitting**.  
- From **Idle**, **squelch_break** (signal detected) moves to **Receiving**.  
- From **Receiving**, **signal_lost** returns to **Idle**.  
- From **Idle**, **ptt_press** moves to **Transmitting**.  
- From **Transmitting**, **ptt_release** returns to **Idle**.  
- **ptt_press** while **Receiving** shall be **rejected** (operator must not transmit over a receive path in this simple policy).  
- **power_off** from any powered mode returns to **Off** and drops any receive/transmit activity.  
- While **Off**, **ptt_press** and **squelch_break** have **no effect** (optional: show as reject/ignore self-transitions on Off).  
- Entry to **Transmitting** starts **key_transmitter**; exit stops it.  
- Entry to **Receiving** starts **audio_path**; exit stops it.

## Deliverables

1. **Hierarchical state chart** with composite state `Powered` and substates `Idle`, `Receiving`, `Transmitting`.  
   - Label transitions with triggers, guards if any, and activities (`entry`/`exit` or `/ effect`).  
   - Show `power_off` from the **composite** (or equivalent clear notation).  
   - Show reject for `ptt_press` in `Receiving`.
2. **Transition list (flat view)** — table of all external-visible transitions:

| Trigger | Guard | From (full path) | To | Activity |
|---------|-------|------------------|----|----------|
| power_on | | Off | Powered::Idle | |
| … | | | | |

3. **FR-style shalls (you write 4)** in EARS that your chart satisfies (e.g. WHEN ptt_press WHILE Idle …). Number them FR-RAD-01 … FR-RAD-04 and mark them on the chart or table.
4. **One paragraph:** what hierarchical modeling saved you versus drawing only a flat chart.

## Rubric

| Dimension | Max | Description |
|-----------|-----|-------------|
| hierarchy | 10 | Composite used correctly; initial substate clear; power_off behavior correct |
| completeness | 10 | Receive/transmit/idle rules + reject path present |
| communication | 5 | Chart + flat table + EARS readable |

## Notes

- SysML tool, PlantUML, Mermaid, or draw.io all OK if hierarchy is visible.  
- If Mermaid nesting is awkward, PlantUML or draw.io nested boxes are preferred — clarity beats tool purity.  
- Cite AI if used; policy choices in your four EARS must match the description.
