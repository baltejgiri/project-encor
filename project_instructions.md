# Project Instructions

## Resources

- Primary source of learning: Cisco's official certification guide "CCNP and CCIE Enterprise Core (ENCOR 350-401) 2nd Edition"
- Cisco Whitepapers on various exam topics to understand concepts at a deeper level while remaining on track
- The cert guide PDF is kept locally for reference only. It's copyrighted and git-ignored, so it's never committed.

## Exam Blueprint

The ENCOR exam blueprint provides a detailed list of topics tested on this exam. Official PDF: [350-401 ENCOR v1.2 exam topics](https://learningcontent.cisco.com/documents/marketing/exam-topics/350-401-ENCORE-v1.2.pdf). Book-to-blueprint mapping: [`encor-v1.2-blueprint-map.md`](encor-v1.2-blueprint-map.md).

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
- Labs can be created as YAML files for CML import, or directly via the CML MCP server (host set in `cml-mcp/.env`, never committed)
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

## Study Method and Schedule

Live on YouTube every day at 5:00: weekdays 5:00 to 6:00 are for reading, weekends 5:00 to 8:00 are for labs. Full details are in the [README](README.md) and [`encor-session-schedule.csv`](encor-session-schedule.csv). Progress is tracked on the [Project ENCOR board](https://github.com/users/baltejgiri/projects/3).

## Spaced Repetition

- **Daily:** Anki reviews at the start of every session (automation cards included from day 1)
- **Per chapter:** 5 to 6 new cards from my own notes, plus cards from whatever broke in the labs
- **Per block (3 to 5 chapters):** a review week (blank-page recall, notes, DIKTA quiz, Key Topics), a mixed lab, and a Pearson Test Prep block test with about 20% from earlier blocks

## Security

- Never commit the cert guide, `.env` files, credentials or the CML hostname. The pre-commit hook in `tools/hooks/` blocks these. Install it once:
  ```bash
  cp tools/hooks/pre-commit .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
  ```
