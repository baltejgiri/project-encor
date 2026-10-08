# Project Overview

CCNP Enterprise Exam Prep 2026 to 2027 covers two Cisco exams: **350-401 ENCOR** (core) and **300-410 ENARSI** (concentration). Passing both earns CCNP Enterprise, the next step after CCNA.

- `project_instructions.md`: resources, lab workflow, spaced repetition and security rules
- `project_chapters_list.md`: chapter map of the Official Cert Guide
- `encor-v1.2-blueprint-map.md`: which chapters to read, skim or skip for v1.2, plus the gaps the book doesn't cover
- `encor-session-schedule.csv`: day-by-day schedule; `encor-tracker.csv`: blueprint topic confidence

## ENCOR: no fixed exam date

The first plan (May 2026) targeted 15 December 2026 and stalled after week 1. The restart, from 19 October 2026, is built for consistency instead of a deadline:

- **Daily live stream at 5:00:** weekdays are 1 hour of reading, weekends are 3 hours of labs
- **6 blocks**, each closed by a review week, a mixed lab and a block test
- **Buffer built in**, and a replan script (`tools/build_schedule.py --replan`) when I fall behind
- **The exam is booked only when the readiness gates in the README are met:** the book is covered, every blueprint topic is at confidence 4 or higher, Anki is under control, practice tests are consistently at target, and the blueprint hasn't changed

## ENARSI

ENARSI follows once ENCOR is passed. The ENCOR routing labs (OSPF, BGP) go a little deeper than ENCOR needs, so that groundwork carries over.
