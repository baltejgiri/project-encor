# Day 19 Lab · Chapter 2: STP Topology Changes

**Session:** Tuesday 2026-11-03, 20-minute lab after the reading (live)
**CML lab:** same five switches as Day 18: import [`../day18/lab-ch02-stp-topology.yaml`](../day18/lab-ch02-stp-topology.yaml)
**Blueprint:** 3.1.c Configure and verify common Spanning Tree Protocols (RSTP, MST) and Spanning Tree enhancements
**Book:** Chapter 2, pp 48-53 (Verification of VLANs on Trunk Links, STP Topology Changes, Converging with Direct Link Failures, Indirect Failures)

## The job

The tree from Day 18 is stable. Before this design goes live, operations wants to know what each kind of link
failure costs: who notices, what gets reported, and how many seconds each switch is without a path to the root.
Nothing has been changed for spanning tree: every priority, cost and timer is at its default.

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

- These switches run PVST+ (`spanning-tree enabled protocol ieee`), the classic 802.1D timers from the book.
- In CML, shutting a port on one switch does **not** bring the link down on the switch at the other end. That end
  stays up and simply stops hearing BPDUs.
- Restore each failure and let the tree settle before you start the next one.
- Answer each task's question in your notes before you move on.

---

## WO-1901 · What does each failure cost?

1. **One interface:** On SW4, look at spanning tree for Gi0/2 only, then the detailed version. Which switch and
   which port send the BPDUs that SW4 uses on Gi0/2? Compare BPDUs sent and received on Gi0/2 and Gi0/1. Why does
   SW4 send almost none?
2. **Baseline:** On all five switches, record how many topology changes VLAN 1 has seen, how long ago the last one
   happened, and which interface it came from.
3. **Failure A, link between two non-root switches:** Take the SW2-SW3 link down from SW3's end. Did any switch
   lose its path to the root? Which switches' change counters moved, and where did SW1's last change come from?
   Bring the link back and time how long SW3's port takes to forward again.
4. **Failure B, direct:** Take SW2's root port down on SW2. Time how long until SW2 forwards toward the root again.
   Which of the book's scenarios is this, and why did SW2 not wait for max age? Restore.
5. **Failure C, direct, other side:** Take SW3's root port down on SW3. Time how long until SW3 has a forwarding
   path to the root again, and record which port changes state on which switch. Why is this slower than failure B?
   Which book scenario does it match? Restore.
6. **Failure D, indirect:** Shut SW1's port toward SW2, on SW1 only. How does SW2 find out, and how long until it
   forwards toward the root again? Compare with failure B. Restore.
7. **Clean up:** Confirm every root port and blocked port matches the Day 18 tree.
