# Day 22 Lab Day: Fix the 2-Tier Campus

**Session:** moved from Sunday 2026-11-08 (day off); new date to come, 5:00 to 8:00 AM (live)
**Network:** the same lab as Day 21. See [the Day 21 sheet](../day21/lab-campus-design.md) for the design, cabling and addressing.
**Blueprint:** 3.1.a trunking, 3.1.b EtherChannel, 3.1.c spanning tree, 3.3.c first hop redundancy
**Book:** Chapter 1 (VLANs, SVIs), Chapter 2 (STP and RSTP), Chapter 5 (trunks and EtherChannel)

## The situation

Saturday's network was built and working. Overnight, someone made changes, and six tickets came in by morning.
The tickets describe what people see, not what's wrong. Nobody knows what was changed.

## How to work each ticket

1. Read the symptom and confirm it yourself.
2. Pick the show command that proves or rules out your first guess.
3. Find the cause, then predict what your fix will change.
4. Fix it and check the symptom is gone.
5. Write down the command that found it.

Work the tickets in any order. Some faults hide each other.

---

## INC-2201 · PC3 can't reach anything
PC3 (10.21.20.13, on ASW2) can't reach its gateway or any other host. PC1 is in the same subnet on the other access switch and works fine.

## INC-2202 · ASW2 can't be managed
The NOC can't reach ASW2's management address, 10.21.99.12. ASW1 at 10.21.99.11 answers from the same place.

## INC-2203 · Messages on two consoles
The ASW1 and DSW2 consoles keep logging messages about the link between them. Users haven't reported anything.

## INC-2204 · The bundle is half its size
Interface monitoring shows the DSW1-DSW2 bundle running at half its capacity. Both cables are connected and both ports are up.

## INC-2205 · The gateway moved
The design says DSW1 is the active gateway for every user VLAN. Monitoring shows DSW1 has lost that role for one VLAN. Nothing was down.

## INC-2206 · The design audit failed
A design audit found one VLAN where spanning tree no longer follows Figure 57's rule: the root and the active gateway on the same distribution switch. Traffic in that VLAN still flows.

---

## When every ticket is closed

- Every PC reaches every other PC and both gateways' virtual addresses.
- Both access switches answer on their management addresses.
- Re-run one failure test from Day 21 and confirm the design still recovers.
- Which ticket was hardest to find, and why?

Save the configs with `write memory` on all four switches before you stop the lab.
