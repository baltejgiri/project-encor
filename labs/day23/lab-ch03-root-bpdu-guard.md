# Day 23 Lab · Chapter 3: Protecting the Root and the Edge

**Session:** Tuesday 2026-11-10, 20-minute lab after the reading (live)
**CML lab:** same five switches as Day 22: import [`lab-ch03-root-bpdu-guard.yaml`](lab-ch03-root-bpdu-guard.yaml), which boots where Day 22 finished (SW1 primary root, SW2 secondary, classic PVST+)
**Blueprint:** 3.1.c Configure and verify common Spanning Tree Protocols (RSTP, MST) and Spanning Tree enhancements such as root guard and BPDU guard
**Book:** Chapter 3, from p 67: Additional STP Protection Mechanisms

## The job

Yesterday a switch set to priority 4096 took over as root, and nothing stopped it. The architect wants two things:
the root must stay in the core no matter what someone does to an outer switch, and user ports must come up fast
but never accept a switch.

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

SW5 is the outer switch. SW3 and SW4 are the switches it plugs into.

## Notes before you start

- Work on VLAN 1 unless a task says otherwise.
- Predict each result first, then answer each task's question in your notes.

---

## WO-2301 · Keep the root in the core, keep switches off user ports

About 18 minutes, with 2 spare. Keep to the time on each task.

1. **Starting point (2 min):** Who is the root for VLAN 1 and VLAN 10, and what priority do SW1 and SW2 have? Which
   ports on SW3 and SW4 face SW5?
2. **Keep the root in the core (5 min):** Make sure no switch behind SW3 and SW4 can ever become the root. Do it on
   SW3 and SW4, on the ports facing SW5, not on SW5. Then set SW5's VLAN 1 priority to 4096. What role and state do
   those two ports show now? Which command lists them? Is SW1 still the root?
3. **The rogue leaves (2 min):** Remove SW5's priority. Do the ports recover on their own? How long did it take, and
   what did the log say?
4. **A desk port (5 min):** SW4 Gi1/0 is now a user port in VLAN 10. It must forward as soon as a PC plugs in, and it
   must shut itself if a switch is ever connected to it. SW5 is still on the other end. What happens, and why? What
   did the switch warn you about while you configured it? Which command shows the reason the port is down?
5. **Let it come back by itself (4 min):** Ports shut by that protection should come back after 30 seconds without
   anyone touching them. When does Gi1/0 retry? Did it use your 30 seconds? What happens each time it comes back?
6. **Clean up (2 min):** Put SW4 Gi1/0 back as a trunk to SW5 with no edge settings, bring it up, and confirm every
   port is in the role it had at the start of task 1.

Run `write memory` only if you want to keep the protections for the next lab.
