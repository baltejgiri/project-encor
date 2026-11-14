# Labs

One folder per lab day of the live study series. Each lab is built for that session from what was read that week:
build labs come as a request plus questions to answer, troubleshooting labs come as NOC tickets, and none of them
include step-by-step instructions. Every day folder has its own YAML that boots into that day's starting point, even when the same CML lab is reused. Import it into Cisco Modeling Labs to follow along.

| Day | Date | Folder | Topics | Replay |
|---|---|---|---|---|
| 6 | Sat 17 Oct 2026 | [day06-tickets](day06-tickets) | 802.1Q trunking (build + tickets), Layer 3 interfaces | [YouTube](https://youtu.be/Bd2diUR5CgY) |
| 12 | Sat 24 Oct 2026 | [day12](day12) | CEF and forwarding (work order), VTP, DTP and EtherChannel (tickets). PCs are Alpine Linux | [YouTube](https://youtu.be/L2l1jKdUJVk) |
| 15 | Thu 29 Oct 2026 | [day15](day15) | STP root bridge election (3 switches) | [YouTube](https://youtu.be/tdohTC45bxU) |
| 16 | Fri 30 Oct 2026 | [day16](day16) | STP port roles and parallel links | [YouTube](https://youtu.be/g6UfIAzCLU4) |
| 17 | Sat 31 Oct 2026 | [day17](day17) | Collapsed core from factory defaults: DTP, trunk mismatches, LACP/PAgP/static EtherChannel | [YouTube](https://youtu.be/ph9Poy6Y3C4) |
| 18 | Mon 2 Nov 2026 | [day18](day18) | Building the STP topology: root bridge, root ports, blocked ports (5 switches, fixed MACs) | [YouTube](https://youtu.be/HvlvtjYHgmA) |
| 19 | Thu 5 Nov 2026 | [day19](day19) | STP topology changes: TCNs, direct vs indirect link failures (Day 18 switches) | [YouTube](https://youtu.be/zKOWaFwahzI) |
| 20 | Fri 6 Nov 2026 | [day20](day20) | RSTP: migrate to Rapid PVST+, measure the same failures again, a classic neighbor (Day 18 switches) | [YouTube](https://youtu.be/x7bebLvcMPo) |
| 21 | Sat 7 Nov 2026 | [day21](day21) | 2-tier campus from Cisco's design guide (Figure 57): VLANs, trunks, LACP EtherChannel, Rapid PVST+, SVIs, VRRP, failure tests. Sheet: [lab-campus-design.md](day21/lab-campus-design.md) | [YouTube](https://youtu.be/adt9stIzF8c) |
| 22 | Mon 9 Nov 2026 | [day22](day22) | Ch 3 root bridge placement: primary/secondary root, a rogue switch, path cost (Day 18 switches). Sheet: [lab-ch03-root-placement.md](day22/lab-ch03-root-placement.md) | [YouTube](https://youtu.be/bQ3-0vdwKoA) |
| 23 | Tue 10 Nov 2026 | [day23](day23) | Ch 3 protection: root guard against a rogue switch, PortFast and BPDU guard on a user port, err-disable recovery (Day 18 switches, starts where Day 22 ended). Sheet: [lab-ch03-root-bpdu-guard.md](day23/lab-ch03-root-bpdu-guard.md) | [replay](https://youtu.be/PeUfTUHnoPg) |
| 24 | Wed 11 Nov 2026 | [day24](day24) | Ch 4 MST basics: one region, two instances, a root for each (Day 18 switches with VLANs 10-40, starts where Day 23 ended). Sheet: [lab-ch04-mst-basics.md](day24/lab-ch04-mst-basics.md) | [replay](https://youtu.be/0rkIOIqwH8U) |
| 25 | Thu 12 Nov 2026 | [day25](day25) | Ch 4 MST tuning: per-instance cost and port priority, plus a NOC ticket (starts where Day 24 ended). Sheet: [lab-ch04-mst-tuning.md](day25/lab-ch04-mst-tuning.md) | [replay](https://youtu.be/sQQulVKkxvY) |
| 26 | Sat 14 Nov 2026 | [day26](day26) | Spanning tree done right (Cisco HA campus design, Figure 57): VLANs, trunks, LACP, Rapid PVST+ roots per VLAN, PortFast, BPDU guard, root guard, loop guard, UDLD, a contractor's rogue switch. Sheet: [lab-ch03-stp-best-practice.md](day26/lab-ch03-stp-best-practice.md) | _after the stream_ |
| 28 | Mon 16 Nov 2026 | [day28](day28) | Ch 4 MST region boundary: a work order plus a NOC ticket (moved from Fri 13 Nov). Sheet: [lab-ch04-mst-boundary.md](day28/lab-ch04-mst-boundary.md) | _after the stream_ |
| later | date to come | [day22](day22) | Fix the Day 21 campus: six symptom-only tickets (VLANs, trunks, EtherChannel, spanning tree root, VRRP, management). Uses the Day 21 YAML. Moved from Sun 8 Nov. Sheet: [lab-campus-tickets.md](day22/lab-campus-tickets.md) | _after the stream_ |
