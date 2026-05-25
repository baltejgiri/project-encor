# Project ENCOR

Preparation for the **350-401 ENCOR** exam — target: December 15, 2026.

## Exam

| Exam | Code | Target |
|------|------|--------|
| Implementing Cisco Enterprise Network Core Technologies | 350-401 ENCOR | December 15, 2026 |

## Resources

- **Official Guide**: *CCNP and CCIE Enterprise Core (ENCOR 350-401) 2nd Edition*
- **Exam Blueprint**: 350-401 ENCOR v1.2 (`350-401-ENCORE-v1.2.pdf`)
- **Video**: INE — *Enterprise CORE Exam: 350-401 ENCOR v1.2*
- **Labs**: Cisco Modeling Labs (CML) — personal license, 20 nodes, hosted on home server
- **Practice**: Boson NetSim (introduced after month 3)

## Repo Structure

```
project-encor/
├── README.md
├── project_overview.md          # Goals and full 29-week schedule
├── project_instructions.md      # Resources and study workflow
├── project_chapters_list.md     # Chapter map with exam scope notes
└── labs/
    └── <lab-name>/
        ├── topology.yaml        # CML-importable topology
        ├── README.md            # What the lab covers
        └── SOLUTION.md          # Exam-style questions (no answers)
```

## ENCOR Study Schedule (29 weeks)

### Phase 1 — Content Reading (Weeks 1–24, May 25 – Nov 8)

| Week | Dates | Content |
|------|-------|---------|
| 1 | May 25 – May 31 | Ch 1 Packet Forwarding |
| 2 | Jun 1 – Jun 7 | Ch 2 Spanning Tree Protocol |
| 3 | Jun 8 – Jun 14 | Ch 3 Advanced STP Tuning |
| 4 | Jun 15 – Jun 21 | Ch 4 MSTP + Ch 5 VLANs/EtherChannel |
| 5 | Jun 22 – Jun 28 | Ch 6 IP Routing Essentials + Ch 7 EIGRP |
| 6 | Jun 29 – Jul 5 | Vacation (Jul 1–5) — light review only |
| 7 | Jul 6 – Jul 12 | Ch 8 OSPF |
| 8 | Jul 13 – Jul 19 | Ch 9 Advanced OSPF |
| 9 | Jul 20 – Jul 26 | Ch 10 OSPFv3 |
| 10 | Jul 27 – Aug 2 | Ch 11 BGP |
| 11 | Aug 3 – Aug 9 | Ch 12 Advanced BGP |
| 12 | Aug 10 – Aug 16 | Ch 13 Multicast |
| 13 | Aug 17 – Aug 23 | Ch 14 QoS (first half) |
| 14 | Aug 24 – Aug 30 | Ch 14 QoS (finish) + Ch 15 IP Services (start) |
| 15 | Aug 31 – Sep 6 | Ch 15 IP Services (finish) |
| 16 | Sep 7 – Sep 13 | Ch 16 Overlay Tunnels |
| 17 | Sep 14 – Sep 20 | Ch 22 Enterprise Network Architecture |
| 18 | Sep 21 – Sep 27 | Ch 23 Fabric Technologies |
| 19 | Sep 28 – Oct 4 | Ch 24 Network Assurance (first half) |
| 20 | Oct 5 – Oct 11 | Ch 24 Network Assurance (finish) |
| 21 | Oct 12 – Oct 18 | Ch 25 Secure Network Access Control |
| 22 | Oct 19 – Oct 25 | Ch 26 Network Device Access Control |
| 23 | Oct 26 – Nov 1 | Ch 27 Virtualization + Ch 28 Programmability (start) |
| 24 | Nov 2 – Nov 8 | Ch 28 Programmability (finish) + Ch 29 Automation Tools |

> Part VI (Ch 17–21 Wireless) is skipped — no longer on the ENCOR exam blueprint.

### Phase 2 — Review and Practice Tests (Weeks 25–29, Nov 9 – Dec 14)

| Week | Dates | Activity |
|------|-------|----------|
| 25 | Nov 9 – Nov 15 | Comprehensive section reviews (Part VII, VIII, IX) |
| 26 | Nov 16 – Nov 22 | Boson Practice Test 1 + review wrong answers |
| 27 | Nov 23 – Nov 29 | Boson Practice Test 2 + targeted chapter re-reads |
| 28 | Nov 30 – Dec 6 | Boson Practice Test 3 + weak area focus |
| 29 | Dec 7 – Dec 13 | Boson Practice Test 4 + final cramming |
| Exam | Dec 15 | **350-401 ENCOR** |

## Study Workflow

- **Daily**: Read one chapter + 10–15 flashcard-style review questions
- **Weekly**: Mock test covering the past week's topics
- **Per Part**: Comprehensive section review upon completion
- **Labs**: Created for blueprint topics tagged with *Configure*, *Verify*, *Troubleshoot*, *Diagnose*, *Construct*, *Interpret*, or *Compare*

## Progress Tracking

Tracked via the [Project ENCOR](https://github.com/users/baltejgiri/projects/3) board on GitHub Projects.
