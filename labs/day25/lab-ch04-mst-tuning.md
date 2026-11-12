# Day 25 Lab · Chapter 4: MST Tuning

**Session:** Thursday 2026-11-12, 20-minute lab after the reading (live)
**CML lab:** import [`lab-ch04-mst-tuning.yaml`](lab-ch04-mst-tuning.yaml). It boots where Day 24 finished: one MST region, two instances, two roots.
**Blueprint:** 3.1.c Configure and verify common Spanning Tree Protocols (RSTP, MST) and Spanning Tree enhancements such as root guard and BPDU guard
**Book:** Chapter 4, pp 87-90: MST Tuning, Common MST Misconfigurations

## Topology

```
                  SW1
                /     \
           Gi0/1       Gi0/2
              |           |
           Gi0/1       Gi0/1
            SW2 --------- SW3
              Gi0/2   Gi0/2
          Gi1/0  Gi0/3      Gi0/3
            |      |          |
          Gi0/1  Gi0/2      Gi0/1
            SW4 ------------ SW5
              Gi1/0     Gi1/0
```

## Notes before you start

- MST region ENCOR, revision 1. Instance 1 = VLANs 10 and 20, instance 2 = VLANs 30 and 40.
- SW2 and SW3 have SVIs in VLAN 30 (10.30.0.2 and 10.30.0.3) and VLAN 40 (10.40.0.2 and 10.40.0.3).
- Predict each result first, then answer each task's question in your notes.
- If you imported the YAML and an SVI shows down, bounce it once (IOSvL2 quirk).

---

## WO-2501 · Use both of SW4's uplinks

About 10 minutes.

1. **Split by instance (5 min):** SW4 has two uplinks to SW2. The architect wants instance 2 to use SW4's Gi0/1
   while instance 1 stays on Gi0/2. Make the change on SW4 only. How do you prove instance 1 did not move?
2. **Same goal, other side (5 min):** Now instance 1 must also use SW4's Gi0/1, and this time you may not touch SW4.
   Why does this change work from the far end, when the change in task 1 had to be on SW4?

## INC-2502 · Ticket from the NOC

About 8 minutes, with 2 spare.

> **Reported:** 05:40 by monitoring, priority 3
> **Symptom:** Since last night's change window, the probe on SW3 (10.30.0.3) can't reach 10.30.0.2 on SW2.
> The VLAN 40 probe (10.40.0.3 to 10.40.0.2) is fine. The change record only says "trunk tidy-up for load balancing".

3. Find the root cause and fix it. Then answer: what rule would have stopped this change from breaking anything?

Run `write memory` only if you want to keep today's changes for the next lab.
