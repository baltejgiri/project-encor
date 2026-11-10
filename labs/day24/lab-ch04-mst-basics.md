# Day 24 Lab · Chapter 4: One Tree for Many VLANs

**Session:** Wednesday 2026-11-11, 20-minute lab after the reading (live)
**CML lab:** import [`lab-ch04-mst-basics.yaml`](lab-ch04-mst-basics.yaml). It boots where Day 23 finished (SW1 root and SW2 backup for VLAN 1, classic PVST+) and adds VLANs 20, 30 and 40.
**Blueprint:** 3.1.c Configure and verify common Spanning Tree Protocols (RSTP, MST) and Spanning Tree enhancements such as root guard and BPDU guard
**Book:** Chapter 4, pp 80-85: Multiple Spanning Tree Protocol, MST configuration

## The job

The switches carry five VLANs now, and every VLAN runs its own spanning tree. The architect wants fewer trees:
VLANs 10 and 20 share one tree, VLANs 30 and 40 share another, and each tree has its own root so both
uplinks from the core get used.

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

- VLANs 10, 20, 30 and 40 exist on every switch, and every link is a trunk.
- Predict each result first, then answer each task's question in your notes.

---

## WO-2401 · Fewer trees, two roots

About 18 minutes, with 2 spare. Keep to the time on each task.

1. **Starting point (2 min):** How many spanning-tree instances is SW3 running right now? Who is the root for VLAN 1
   and for VLAN 30, and why?
2. **One region (8 min):** Put all five switches in one MST region named ENCOR, revision 1. VLANs 10 and 20 go in
   instance 1, VLANs 30 and 40 in instance 2. Which command shows the region settings? How many instances does SW3
   run now? Which instance is VLAN 1 in?
3. **Two roots (6 min):** SW1 must be the root for instance 1 and SW2 the root for instance 2, each one the backup for
   the other. Which ports block in instance 1, and which in instance 2? Is it the same port for both?
4. **Look back (2 min):** Compare with task 1. How many spanning trees does each switch run now, and how many sets
   of BPDUs does each switch send for them?

Run `write memory` only if you want to keep MST for the next lab.
