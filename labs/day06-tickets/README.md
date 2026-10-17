# Day 6 labs: VLAN trunking and Layer 3 interfaces (Chapter 1)

Live lab day, Saturday 17 October 2026, 5:00 to 8:00 AM. Three CML labs, no step-by-step instructions:
build labs come as a request plus questions to answer, and the troubleshooting lab comes as NOC tickets.

Blueprint: **3.1.a** Troubleshoot static and dynamic 802.1Q trunking (Lab 1 and the tickets).
Lab 2 (SVIs, subinterfaces, routed ports) is the Chapter 1 foundation for inter-VLAN routing in 3.2.

| File | CML lab | Type |
|---|---|---|
| `lab1-build.yaml` | Day 6 - Lab 1: VLANs and 802.1Q Trunking | Build |
| `lab1-tickets.yaml` | Day 6 - Lab 1 TICKETS: SW1-SW2 outage | Troubleshoot |
| `lab2-build.yaml` | Day 6 - Lab 2: Layer 3 Interfaces | Build |

> Spoiler warning: `lab1-tickets.yaml` contains the device configs, so it shows the faults. Work the tickets in CML first.

## Done on stream

- **When:** Saturday 17 October 2026, live 4:58 to 8:37 AM (first lab day of the series)
- **Replay:** https://youtu.be/Bd2diUR5CgY
- **Checklist and my answers:** [issue #252](https://github.com/baltejgiri/project-encor/issues/252)
- **Notes from the session:** in Lab 2, disconnecting PC2's link in CML and removing VLAN 20 from the trunk did not bring SW1's VLAN 20 interface down. A disconnected CML link can leave the IOSvL2 port up, and the virtual switch may not apply SVI autostate like a real Catalyst. Worth remembering when a lab result differs from the book.

To use them in your own CML: Import, then choose the YAML file. Each lab's Notes hold the same request, questions or tickets as below.

---

## Lab 1: VLANs and 802.1Q trunking (build)

**Request (from the network team)**
- PC1 (on SW1) and PC2 (on SW2) are both in VLAN 10. They must be able to reach each other.
- VLAN 20 must also be carried between SW1 and SW2 for future users (PC3 is the first one).
- The link between SW1 and SW2 is the only path between the buildings.

**Questions (prove each answer with device output)**
1. What does a VLAN 10 frame look like on the SW1-SW2 link, compared with on PC1's link? Which fields changed?
2. How do the switches decide where to send a frame for a MAC address they haven't learned yet?
3. What happens to traffic that has no VLAN tag on the SW1-SW2 link? Which VLAN does it belong to, and what if the two ends disagree?
4. How long does a switch remember a MAC address, and how can you watch that happen?

## Lab 1 tickets: SW1-SW2 outage (troubleshoot)

**INC-1042 (Priority 2).** Reported by the user at PC1 (10.10.10.1), building A:
"Since last night's change window I can't reach PC2 (10.10.10.2) in building B. We're both in VLAN 10. It worked before the change."
Change record: "Uplink between SW1 and SW2 reconfigured." No other details.

**INC-1043 (Priority 4).** Opened by monitoring, may only show up later:
"SW1 is logging repeated warnings about the SW1-SW2 link. Please investigate."

Rules: find the root cause from the device output before you change anything. For each ticket write down:
symptom, what you checked, root cause, fix, and how you proved it's fixed.

## Lab 2: Layer 3 interfaces (build)

**Request (from the network team)**
- R1 is the default gateway for both user VLANs: VLAN 10 uses 10.10.10.254/24, VLAN 20 uses 10.20.20.254/24. R1 has one physical link to SW1.
- VLAN 10 is also moving to a new range: 172.16.10.254/24 must work on R1 for VLAN 10 at the same time as the old one.
- SW1 needs its own address in each user VLAN: 10.10.10.1/24 and 10.20.20.1/24.
- SW1 connects to R2 over a point-to-point routed link: SW1 172.30.0.1/30, R2 172.30.0.2/30.
- Everything must be dual stack:

| Network | Prefix | Addresses |
|---|---|---|
| VLAN 10 | 2001:db8:10::/64 | R1 ::1 (also ::ff), SW1 ::2 |
| VLAN 20 | 2001:db8:20::/64 | R1 ::1, SW1 ::2 |
| SW1-R2 | 2001:db8:30::/64 | SW1 ::1, R2 ::2 |

**Questions (prove each answer with device output)**
1. How is a switch's address in a VLAN different from the address on its port to R2?
2. Under what conditions is SW1's VLAN 20 address unusable? Make it happen, then undo it.
3. When PC1 sends a packet to R2's 172.30.0.2, which devices does it pass through, and what changes in the frame at each hop?
