# ENCOR v1.2 Blueprint → Official Cert Guide Map

Built from Cisco's official [350-401 ENCOR v1.2 exam topics](https://learningcontent.cisco.com/documents/marketing/exam-topics/350-401-ENCORE-v1.2.pdf) and the table of contents of the *CCNP and CCIE Enterprise Core ENCOR 350-401 Official Cert Guide*, 2nd edition (Cisco Press; the book itself isn't included here). The book was written for the previous blueprint, so this map says what to read, what to skim and what to skip.

Per-topic tracking lives in [encor-tracker.csv](encor-tracker.csv).

---

## Chapter verdicts

| Ch | Title | Verdict | Blueprint | Notes |
|---|---|---|---|---|
| 1 | Packet Forwarding | Skim | (foundation) | Not a blueprint line, but CEF and forwarding come up indirectly |
| 2 | Spanning Tree Protocol | Read | 3.1.c | RSTP |
| 3 | Advanced STP Tuning | Read | 3.1.c | Root guard and BPDU guard are named in the blueprint |
| 4 | Multiple Spanning Tree Protocol | Read | 3.1.c | |
| 5 | VLAN Trunks and EtherChannel Bundles | Read | 3.1.a, 3.1.b | "Troubleshoot", so lab the faults |
| 6 | IP Routing Essentials | Read | 3.2.d, 2.2.a | PBR (p146) and VRF (p149) live here |
| 7 | EIGRP | Read for concepts | 3.2.a | Blueprint only asks you to *compare* EIGRP with OSPF |
| 8 | OSPF | Read | 3.2.b | |
| 9 | Advanced OSPF | Read | 3.2.b | Summarization and filtering |
| 10 | OSPFv3 | Read | 3.2.b | Blueprint says "OSPFv2/v3" |
| 11 | BGP | Read | 3.2.c | eBGP between directly connected neighbors |
| 12 | Advanced BGP | Partly | 3.2.c | Read the best-path selection section. Route maps, conditional matching and communities go beyond ENCOR (useful if you take ENARSI) |
| 13 | Multicast | Read for concepts | 3.3.d | "Describe" only: RPF, PIM-SM, IGMPv2/v3, SSM, bidir, MSDP |
| 14 | QoS | Read; skip one section | 1.4 | "Interpret" configs. **Skip "A Practical Example: Wireless QoS" (p393)** |
| 15 | IP Services | Read | 3.3.a to 3.3.c | NTP and PTP (interpret), NAT/PAT, HSRP/VRRP (configure) |
| 16 | Overlay Tunnels | Read | 2.2.b, 2.3 | GRE, IPsec, GRE over IPsec, VTI, LISP, VXLAN |
| 17 to 21 | Wireless (all five chapters) | **Skip** | none | Removed in v1.2 (pp. 510 to 621, about 110 pages saved) |
| 22 | Enterprise Network Architecture | Read | 1.1 | 2-tier, 3-tier, SSO/NSF, SD-Access design |
| 23 | Fabric Technologies | Read | 1.2, 1.3 | SD-Access and SD-WAN. Skip the fabric wireless controller detail |
| 24 | Network Assurance | Read | 4.1 to 4.5 | Debug, conditional debug, SNMP, syslog, Flexible NetFlow, SPAN/RSPAN/ERSPAN, IP SLA, DNA Center Assurance |
| 25 | Secure Network Access Control | Read | 5.4 | Threat defense, endpoint, NGFW, TrustSec, MACsec. 802.1X isn't named in v1.2, but TrustSec builds on it, so read it lightly |
| 26 | Network Device Access Control and Infrastructure Security | Read | 5.1, 5.2 | Lines, local users, AAA, ACLs, CoPP. Zone-Based Firewall isn't named in the blueprint, so skim it |
| 27 | Virtualization | Partly | 2.1 | Read VMs, containers, virtual switching. Skim the NFV and ENFV detail (not in the blueprint) |
| 28 | Foundational Network Programmability Concepts | Read | 4.6, 6.1 to 6.5 | REST, JSON, YANG, NETCONF, RESTCONF, Python, DNA Center/vManage APIs |
| 29 | Introduction to Automation Tools | Read | 6.6, 6.7 | EEM ("Construct", so lab it). Puppet, Chef, SaltStack and Ansible only to *compare* agent vs agentless |
| 30 | Final Preparation | Use in weeks 22 to 24 | | |
| 31 | Exam Updates | **Download the latest version** | | ciscopress.com/register, ISBN 9780138216764 |

## Gaps: blueprint topics the book doesn't fully cover

1. **4.5 Catalyst Center "AI-powered workflows".** The book covers DNA Center Assurance only. Use Cisco's Catalyst Center docs and the DevNet Catalyst Center sandbox.
2. **5.3 Describe REST API security.** There's no dedicated section in the book's table of contents. Cover authentication (basic, token, OAuth), HTTPS, and API keys vs tokens from Cisco DevNet material.
3. **Naming.** The book says DNA Center and vManage; the exam says Catalyst Center (4.5, 6.4, 6.5) and SD-WAN Manager (6.4). The same products were renamed, so learn both names.
4. **1.2 "Benefits and limitations" of Catalyst SD-WAN.** Ch 23 explains the architecture. Write your own pros and cons list; it makes good Anki material.

## Lab topics vs concept topics

**Lab (Configure / Troubleshoot / Construct):** 2.2.a VRF · 2.2.b GRE and IPsec · 3.1.a trunks · 3.1.b EtherChannel · 3.1.c RSTP/MST with root guard and BPDU guard · 3.2.b OSPFv2/v3 · 3.2.c eBGP · 3.3.b NAT/PAT · 3.3.c HSRP/VRRP · 4.2 Flexible NetFlow · 4.3 SPAN/RSPAN/ERSPAN · 4.4 IP SLA · 4.6 NETCONF/RESTCONF · 5.1 lines, local users and AAA · 5.2 ACLs and CoPP · 6.2 JSON · 6.6 EEM

**Concept (Explain / Describe / Interpret / Compare):** everything else. These go on the whiteboard and into Anki, not the lab.

**CML Free node budget (5 nodes):** every lab topic above fits in 5 nodes or fewer. NETCONF/RESTCONF needs an IOS-XE node (Catalyst 8000v), which uses more RAM than IOSv, so test that one before the week 20 stream.
