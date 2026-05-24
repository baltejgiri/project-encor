# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

CCNP Enterprise exam preparation (May 2026 – May 2027). Two exams required:
- **350-401 ENCOR** — target: 6 months (by ~November 2026)
- **300-410 ENARSI** — target: months 7–12

## Key Reference Files

- `project_overview.md` — goals and timeline
- `project_instructions.md` — resources, lab workflow, version control rules, spaced repetition schedule
- `project_chapters_list.md` — chapter map for the official guide (with exam scope notes)
- `350-401-ENCORE-v1.2.pdf` — official exam blueprint (authoritative scope reference)
- `ccnp-and-ccie-enterprise-core-encor-350-401-2nd-edition.pdf` — official cert guide (stored locally for reference)

## Book Chapter Scope

Part VI (Ch 17–21, Wireless) is **no longer on the ENCOR exam blueprint — skip entirely**.

Active chapters:
- **Part I** Ch 1: Packet Forwarding
- **Part II** Ch 2–5: Layer 2 (STP, Advanced STP, MSTP, VLANs/EtherChannel)
- **Part III** Ch 6–13: Routing (IP Routing, EIGRP, OSPF, Advanced OSPF, OSPFv3, BGP, Advanced BGP, Multicast)
- **Part IV** Ch 14–15: Services (QoS, IP Services)
- **Part V** Ch 16: Overlay Tunnels
- **Part VII** Ch 22–24: Architecture, Fabric Technologies, Network Assurance
- **Part VIII** Ch 25–26: Security
- **Part IX** Ch 27–29: SDN (Virtualization, Programmability, Automation)
- **Ch 30**: Final Preparation

## Claude's Role

### Progress Tracking
Analyze study logs and flag if pace is off-track for the 6-month ENCOR deadline.

### Lab Creation
Create labs only for exam blueprint topics with these action verbs: *Interpret*, *Configure*, *Verify*, *Troubleshoot*, *Compare*, *Diagnose*, *Construct*.

**Lab format options:**
- YAML file for CML import
- Direct creation via CML MCP server at `cml.example.com`

**Lab directory structure** (under the `ccnp/` root):
```
ccnp/<lab-name>/
├── README.md      # what the lab covers and its topology
└── SOLUTION.md   # exam-style questions for this topic — NO answers or commands
```
Labs are graded against `SOLUTION.md` once completed.

### Spaced Repetition
- **Each study day**: generate 10–15 flashcard-style review questions
- **Weekly**: generate a mock test covering the past week's topics
- **End of each Part**: generate a comprehensive section review
