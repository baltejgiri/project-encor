# Day 17 Lab Day · Chapter 5: Collapsed Core Uplinks

**Session:** Saturday 2026-10-31, 5:00 to 8:00 AM PT (live)
**CML lab:** "Day 17 - Lab: Ch 5 collapsed core" (loaded and booted)
**Blueprint:** 3.1.a Troubleshoot static and dynamic 802.1Q trunking protocols · 3.1.b Troubleshoot static and dynamic EtherChannels
**Book:** Chapter 5, pp 101-120 (DTP and EtherChannel)

## The job

A new floor is being brought online. Two closet switches, **ACC1 in Closet 2A** and **ACC2 in Closet 3B**, must be uplinked to the core pair in the MDF, **CORE1** and **CORE2**. Every closet connects to both cores, so losing one core or one uplink doesn't take the floor down. The switches came out of the box with factory settings (hostname only).

| Time | Block |
|---|---|
| 5:00-5:55 | **Session 1:** hello, the job, topology walk-through, WO-1701 tasks 1-7 |
| 5:55-6:00 | Break |
| 6:00-6:55 | **Session 2:** WO-1701 tasks 8-11, WO-1702 tasks 1-4 |
| 6:55-7:00 | Break |
| 7:00-7:55 | **Session 3:** WO-1702 tasks 5-12 |
| 7:55-8:00 | Wrap-up |

If time is left: Day 16 STP lab (WO-1602). If not, it moves to another session.

## Topology

```
 MDF          CORE1 =======3======= CORE2
               ||  \               /  ||
               2    1             1    2
               ||     \         /     ||
               ||       \     /       ||
               ||         \ /         ||
               ||         / \         ||
               ||       /     \       ||
 Closet 2A    ACC1 ---'         '--- ACC2    Closet 3B
```
(Numbers are how many cables. Each closet has two cables to one core and one cable to the other.)

| Cable | From | To | Purpose |
|---|---|---|---|
| 1-3 | CORE1 Gi0/1, Gi0/2, Gi0/3 | CORE2 Gi0/1, Gi0/2, Gi0/3 | Core interlink |
| 4-5 | CORE1 Gi1/0, Gi1/1 | ACC1 Gi0/1, Gi0/2 | Closet 2A uplink to CORE1 |
| 6 | CORE2 Gi1/0 | ACC1 Gi0/3 | Closet 2A uplink to CORE2 |
| 7 | CORE1 Gi1/2 | ACC2 Gi0/3 | Closet 3B uplink to CORE1 |
| 8-9 | CORE2 Gi1/1, Gi1/2 | ACC2 Gi0/1, Gi0/2 | Closet 3B uplink to CORE2 |

## VLAN plan (all switches)

| VLAN | Name | Notes |
|---|---|---|
| 10 | DATA | |
| 20 | VOICE | |
| 99 | MGMT | |
| 999 | NATIVE-UNUSED | Native VLAN on every trunk, carries no users |

**Trunk standard:** every switch-to-switch link is an 802.1Q trunk that carries only VLANs 10, 20 and 99, with native VLAN 999. When the job is finished, no uplink is left negotiating with DTP.

## Notes before you start

- VTP is set to transparent on all four switches (common in production). VTP is not part of today's lab: create the VLANs on every switch yourself.
- These switches also support ISL, so a port's trunk encapsulation starts as "auto". IOS refuses `switchport mode trunk` until the encapsulation is 802.1Q. (Catalyst 9000 switches only do 802.1Q, so you won't see this on them.)
- The switch MACs are fixed in this lab, so the STP root is the same on every boot.
- Answer each task's question in your notes before you move on.

---

## WO-1701 · Trunks and DTP (Session 1 and start of Session 2)

1. **VLANs:** Create the VLAN plan on all four switches.
2. **Out of the box:** Before changing any port, record the administrative and operational mode of ACC1 Gi0/3 and CORE2 Gi1/0. Is this uplink a trunk? Why not?
3. **One side negotiates:** Make the ACC1-CORE2 uplink a trunk by changing **only ACC1**, using DTP (not a static trunk). Record the Mode and Encapsulation columns of `show interfaces trunk` on both switches. Which encapsulation did they agree on, and what does the "n-" in front of it mean?
4. **802.1Q, still negotiated:** Keep DTP on this uplink, but make it run 802.1Q on both ends. Record the new Encapsulation column.
5. **Static meets default:** Make CORE1 Gi1/2 (toward ACC2) a static trunk. Leave ACC2 Gi0/3 at its default. What is ACC2's operational mode, and why?
6. **Stop DTP on one side:** Stop CORE1 Gi1/2 from sending DTP. Check ACC2 Gi0/3 once a minute for 5 minutes. Record when its mode changes and every log message you see. Why didn't it change straight away? Then make this uplink a trunk with **no DTP on either end**.
7. **Trunk standard:** Apply the trunk standard to both single uplinks (ACC1-CORE2 and CORE1-ACC2). `show interfaces trunk` has four sections. What does each one show for these ports?
8. **Native VLAN mismatch:** On CORE2 Gi1/0 only, put the native VLAN back to the default. Wait 2 minutes. Record every log message on both switches: which protocol found the problem, and what did STP do? Then fix it.
9. **Allowed VLAN mismatch:** On ACC1 Gi0/3 only, remove VLAN 20 from the allowed list. Does any protocol warn you? What would users in the voice VLAN notice? Then fix it.
10. **The replacement switch:** A replacement for ACC1 arrives from another site, still configured with that site's VTP domain. Simulate it: give ACC1 and CORE2 different VTP domain names, set both ends of their uplink to negotiate actively, and bounce the link. Does the trunk come up? Record the log message. Then put both in the same domain, confirm the trunk forms, and return the uplink to the trunk standard.
11. **Open question from Day 10 (labs-to-test):** Does `switchport nonegotiate` work on a port that is still in a dynamic mode? Test it on an unused ACC2 port (for example Gi2/0) and record exactly what IOS says. Where does it work?

---

## WO-1702 · EtherChannel (rest of Session 2 and Session 3)

**Design:** all three bundles are trunks built to the trunk standard.

| Bundle | Where | Members | Protocol | Rule |
|---|---|---|---|---|
| Po1 | CORE1-CORE2 (core interlink) | 3 | LACP | CORE1 starts the negotiation, CORE2 only answers |
| Po13 | ACC1-CORE1 (Closet 2A uplink) | 2 | PAgP | ACC1 starts, CORE1 only answers. ACC1 must not bundle a port until it hears PAgP from the core |
| Po24 | ACC2-CORE2 (Closet 3B uplink) | 2 | none (static) | no negotiation protocol at all |

1. **Build Po1, Po13 and Po24** to the design. For each, record the port-channel flags, the member flags and the bandwidth.
2. **Neighbors:** Show CORE1's LACP neighbor and PAgP neighbor. What does each tell you that `show etherchannel summary` doesn't?
3. **STP view:** Find the root bridge for VLAN 10. On each closet switch, which uplink forwards and which one blocks? How many STP ports does CORE1 now see toward CORE2, and at what cost?
4. **Both sides answering only:** Change CORE1's Po1 members so that both ends only answer. Record what happens to Po1 and its members. What did STP do with the closet uplinks while the core interlink was down? Restore the design.
5. **Member mismatch (LACP):** On CORE2, change the allowed VLAN list on **one member interface** of Po1 (not on the port channel). Record the flags and log messages on both cores. Fix it.
6. **Member mismatch (static):** Do the same on one ACC2 member of Po24. Compare both ends with task 5. Which bundle protects you, and what could happen to traffic on the other one? Fix it.
7. **Maximum links:** Allow only **two** active members in Po1, set on CORE1. Which member is left out? Record its flag on **both** cores (they differ). Why that member? Did Po1 stay up while you changed it?
8. **Choose the standby link:** Make CORE1 Gi0/3 an active member instead, without removing the maximum. Then make **CORE2** the switch that decides which members are active, and give CORE2 its own preference. Which member is in standby now, and how does that prove which switch decides? Remove the maximum when you are done.
9. **Platform check:** Try LACP fast and a minimum number of links on Po1. Record exactly what this switch image says. (Also answers the Day 13 open question.)
10. **Load balancing:** What hash is CORE1 using for non-IP, IPv4 and IPv6 traffic? Which of the book's hash options does this image offer (the book's example uses src-dst-mixed-ip-port)? Why is a MAC-based hash a bad choice on a port channel to a router? Why do 3 members balance worse than 2 or 4?
11. **Member failure:** Look at the LACP and PAgP counters. Then shut CORE2 Gi0/2 (a Po1 member). Check Po1 on **both** cores right away, then check CORE1 every 30 seconds until it changes. What happens to Po1's bandwidth, its line protocol and its STP cost? How long did CORE1 take to notice, and what told it? (In CML, shutting a port does not take the link down on the other end, the way pulling a real cable would.) Why is a bundle better for the closets than three separate links? Bring the member back.
12. **Uplink failure:** Shut ACC1's Po13 (its uplink to CORE1). Does Closet 2A stay connected? Which port takes over, and how long does it take? Bring Po13 back and record what happens.

---

## Wrap-up questions

- Which DTP mode combinations form a trunk, and which don't?
- Which EtherChannel mode combinations form a bundle, and which don't?
- Name the settings that must match on every member of a port channel.
- Why does the trunk standard turn DTP off on uplinks?
- What did this switch image not support?
