# Day 26 Lab · Chapter 4: MST Region Boundary

**Session:** Friday 2026-11-13, 20-minute lab after the DIKTA catch-up (live)
**CML lab:** import [`lab-ch04-mst-boundary.yaml`](lab-ch04-mst-boundary.yaml). It boots where Day 25 finished: one MST region, two instances, both of SW4's uplinks in use.
**Blueprint:** 3.1.c Configure and verify common Spanning Tree Protocols (RSTP, MST) and Spanning Tree enhancements such as root guard and BPDU guard
**Book:** Chapter 4, pp 90-91: MST Region Boundary

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
- SW5 has an SVI in VLAN 40 (10.40.0.5). SW2 is 10.40.0.2.
- IOSvL2 quirk: a port that spanning tree marks as blocked can still pass a ping in this lab. Judge by the switches' STP state and logs, not by ping alone.
- Predict each result first, then answer each question in your notes.

---

## WO-2601 · SW5 swap

1. **The swap (4 min):** SW5 is being replaced by a switch that only runs Rapid PVST+, not MST. Make SW5 match the
   new switch. Which ports in the MST region are now region boundary ports, and which output proves it?

> **INC-2602 comes in right after task 1. Work it before task 2.**

## INC-2602 · Ticket from the NOC

About 8 minutes.

> **Reported:** 05:50 by monitoring, priority 2
> **Symptom:** Right after the SW5 change, SW3 and SW4 started raising critical (level 2) spanning-tree alarms for
> their ports toward SW5. The change record says "SW5 swap, no other changes".

2. Find the root cause and fix it. Then answer: what has to stay true about the PVST+ side so this can't happen?

## WO-2601 (continued)

3. **Keep the region in charge (5 min):** The architect wants the MST region to stay the root for every VLAN on SW5,
   even if someone adds a new switch at default priority later. Do it without touching SW5.
   Why does SW5 show the same root bridge for every VLAN?

Run `write memory` only if you want to keep today's changes for the next lab.
