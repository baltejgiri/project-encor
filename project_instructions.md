# Project Instructions

## Resources

- Primary source of learning: Cisco's official certification guide "CCNP and CCIE Enterprise Core (ENCOR 350-401) 2nd Edition"
- Cisco Whitepapers on various exam topics to understand concepts at a deeper level while remaining on track
- The official cert guide PDF is stored in this project for reference

## Exam Blueprint

The ENCOR exam blueprint provides a detailed list of topics tested on this exam. See the attached blueprint file: `350-401-ENCORE-v1.2.pdf`

### Exam Description

Implementing Cisco Enterprise Network Core Technologies v1.2 (ENCOR 350-401) is a 120-minute exam associated with the CCNP and CCIE Enterprise Certifications. This exam tests a candidate's knowledge of implementing core enterprise network technologies, including dual stack (IPv4 and IPv6) architecture, virtualization, infrastructure, network assurance, security, and automation.

## Reading

- All active chapters from Cisco's official certification guide "CCNP and CCIE Enterprise Core (ENCOR 350-401) 2nd Edition"
- Cisco Whitepapers on various exam topics for deeper understanding

## Videos

- [INE Video Library](https://ine.com/) — course: "Enterprise CORE Exam: 350-401 ENCOR v1.2"

## Labs

- All labs are completed using CML (personal license, 20 nodes) hosted on home server
- Labs are created for exam blueprint topics with action verbs: *Interpret*, *Configure*, *Verify*, *Troubleshoot*, *Compare*, *Diagnose*, *Construct*
- Labs can be created as YAML files for CML import, or directly via the CML MCP server at `cml.example.com`
- Boson NetSim will be used for guided lab practice starting around month 3

## Lab Directory Structure

Each lab lives under the `labs/` root:

```
labs/<lab-name>/
├── topology.yaml  # CML-importable topology
├── README.md      # what the lab covers and its topology
└── SOLUTION.md    # exam-style questions — no answers or commands
```

Labs are graded against `SOLUTION.md` once completed.

## Version Control

- Each CML lab has its own directory under `labs/`
- Each lab includes a `README.md` describing what it covers
- Each lab includes a `SOLUTION.md` with exam-style questions (no answers or commands)
- Labs are graded against `SOLUTION.md` upon completion

## Spaced Repetition

- Generate 10–15 flashcard-style review questions each study day
- Generate a weekly mock test covering the past week's topics
- Generate a comprehensive section review at the end of each Part
