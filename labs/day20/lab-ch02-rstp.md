# Day 20 Lab · Chapter 2: RSTP

**Session:** Friday 2026-11-06, 20-minute lab after the reading (live)
**CML lab:** same five switches as Day 18: import [`../day18/lab-ch02-stp-topology.yaml`](../day18/lab-ch02-stp-topology.yaml)
**Blueprint:** 3.1.c Configure and verify common Spanning Tree Protocols (RSTP, MST) and Spanning Tree enhancements
**Book:** Chapter 2, pp 54-57 (RSTP Port States, Roles and Types, Building the RSTP Topology, RSTP Convergence)

## The job

Operations has the Day 19 numbers and doesn't like them: about 30 seconds for a direct failure and about 50 for an
indirect one. The architect wants the same five switches moved to Rapid PVST+ and the same failures measured again.

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

| Link | From | To |
|---|---|---|
| 1 | SW1 Gi0/1 | SW2 Gi0/1 |
| 2 | SW1 Gi0/2 | SW3 Gi0/1 |
| 3 | SW2 Gi0/2 | SW3 Gi0/2 |
| 4 | SW2 Gi1/0 | SW4 Gi0/1 |
| 5 | SW2 Gi0/3 | SW4 Gi0/2 |
| 6 | SW3 Gi0/3 | SW5 Gi0/1 |
| 7 | SW4 Gi1/0 | SW5 Gi1/0 |

| Switch | System MAC |
|---|---|
| SW1 | 5254.0011.0011 |
| SW2 | 5254.0013.0013 |
| SW3 | 5254.0012.0012 |
| SW4 | 5254.0015.0015 |
| SW5 | 5254.0014.0014 |

## Notes before you start

- Every priority, cost and timer stays at its default.
- In CML, shutting a port on one switch does **not** bring the link down on the switch at the other end. That end
  stays up and simply stops hearing BPDUs.
- Restore each failure and let the tree settle before you start the next one.
- Predict each result first, then answer each task's question in your notes.

---

## WO-2001 · What does Rapid PVST+ save?

About 18 minutes, with 2 spare. Keep to the time on each task.

1. **Migrate (3 min):** Move all five switches to Rapid PVST+. Where does the switch confirm the protocol it's running?
2. **Compare (2 min):** Did the root, the root ports or the blocked ports change? The book says RSTP has a discarding
   state. What does the switch show on SW2's and SW4's non-forwarding ports?
3. **Direct failure (3 min):** Take SW2's root port down on SW2. Time how long until SW2 forwards toward the root
   again. Compare with Day 19's failure B. Which part of the RSTP process made the difference? Restore.
4. **Indirect failure (3 min):** Shut SW1's port toward SW2, on SW1 only. Time how long until SW2 forwards toward the
   root again. Compare with Day 19's failure C and with the book's number for RSTP. Restore.
5. **A classic neighbor (5 min):** Move SW5 back to classic PVST+ and time how long until its root port forwards. What
   does SW3 show on its port toward SW5? Which note in the book explains this? Then move SW5 back to Rapid PVST+.
6. **Clean up (2 min):** Confirm all five switches run Rapid PVST+ and every root port and blocked port matches the
   Day 18 tree. Leave it this way for Day 21.
