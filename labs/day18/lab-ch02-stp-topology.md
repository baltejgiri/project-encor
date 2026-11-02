# Day 18 Lab · Chapter 2: Building the STP Topology

**Session:** Monday 2026-11-02, 20-minute lab after the reading (live)
**CML lab:** "Day 18 - Lab: Ch 2 building the STP topology" (loaded and booted)
**Blueprint:** 3.1.c Configure and verify common Spanning Tree Protocols (RSTP, MST) and Spanning Tree enhancements
**Book:** Chapter 2, pp 41-47 (Root Bridge Election, Locating Root Ports, Locating Blocked Designated Switch Ports)

## The job

Five switches, cabled like the book's Figure 2-1 but with different MAC addresses. The trunks are already built
and carry VLANs 1 and 10. Nothing has been changed for spanning tree: every priority, cost and timer is at its default.

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

All links are 1 Gbps. Note links 4 and 5: they cross.

| Switch | System MAC |
|---|---|
| SW1 | 5254.0011.0011 |
| SW2 | 5254.0013.0013 |
| SW3 | 5254.0012.0012 |
| SW4 | 5254.0015.0015 |
| SW5 | 5254.0014.0014 |

## Notes before you start

- These switches run PVST+ (`spanning-tree enabled protocol ieee`), not the RSTP shown in the book's examples.
  Root bridge, root port and blocked port logic is the same.
- Ports without a cable are shut, so `show spanning-tree` lists only the cabled ports.
- The MACs are fixed in this lab, so the result is the same on every boot.
- Answer each task's question in your notes before you move on.

---

## WO-1801 · Read the tree before you touch it

1. **Predict first (no CLI):** From the topology and the MAC table only, write down: the root bridge, the root port and
   root path cost of every other switch, and the port that blocks on each link between two non-root switches.
2. **Root bridge:** Check your prediction with `show spanning-tree root` on all five switches. Why does VLAN 1 show
   priority 32769 and VLAN 10 show 32778?
3. **Root ports:** SW4 has two equal-cost links to SW2. Which one is its root port? Which tie-breaker from p 44
   decided it, and whose port number counted, SW4's or SW2's?
4. **Blocked ports:** For the SW2-SW3 link and the SW4-SW5 link, which port is Altn BLK? Which rule from p 45
   decided each one? Prove it with `show spanning-tree vlan 1` on both ends.
5. **Move the root port:** Make SW4 use Gi0/1 as its root port. Don't change any port cost and don't shut any port.
   Try it on SW4 first and record what happens. Where did the change have to go, and why?
6. **Clean up:** Put the switches back the way you found them and confirm the original root ports and blocked ports.
