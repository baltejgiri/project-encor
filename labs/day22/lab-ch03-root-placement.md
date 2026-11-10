# Day 22 Lab · Chapter 3: Root Bridge Placement

**Session:** Monday 2026-11-09, 20-minute lab after the reading (live)
**CML lab:** same five switches as Day 18: import [`lab-ch03-root-placement.yaml`](lab-ch03-root-placement.yaml), all five boot on classic PVST+ (the YAML's default)
**Blueprint:** 3.1.c Configure and verify common Spanning Tree Protocols (RSTP, MST) and Spanning Tree enhancements
**Book:** Chapter 3, pp 58-63 (Placing the Root Bridge, start of Modifying STP Root Port and Blocked Switch Port Locations)

## The job

SW1 is the root today, but nobody chose it. The architect wants the root and its backup set on purpose, and wants to
know how exposed VLAN 1 is if someone adds a switch with a low priority.

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

- Work on VLAN 1 only and leave VLAN 10 at its defaults.
- Predict each result first, then answer each task's question in your notes.

---

## WO-2201 · Put the root where it belongs

About 18 minutes, with 2 spare. Keep to the time on each task.

1. **Why SW1? (2 min):** Record the bridge priority on SW1, SW2 and SW3. Why is SW1 the root right now?
2. **Primary and secondary (4 min):** Make SW1 the primary root and SW2 the secondary root for VLAN 1, using the
   commands that pick the values for you. What priority did each switch get, and what does the running config show?
   Did any blocked port move? Why?
3. **A bad value (1 min):** On SW5, try to set VLAN 1's priority to 1000. What does the switch say?
4. **A rogue switch (4 min):** Set SW5's VLAN 1 priority to 4096. Who is the root for VLAN 1 now, and for VLAN 10? What
   is SW1's root port and root cost?
5. **Take it back (3 min):** Run the primary root command on SW1 again. What priority does it choose, and who wins?
   How does that compare with the book's note about the script?
6. **Path cost (2 min):** Read the root cost on all five switches. Using SW3 and SW5, what does SW3 advertise, and what
   does SW5 add?
7. **Clean up (2 min):** Remove the rogue priority from SW5. Set SW1 and SW2 to the values the book recommends for
   the primary and secondary root, then confirm who the root is.
