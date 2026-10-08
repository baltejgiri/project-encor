# Project ENCOR: CCNP ENCOR 350-401 (v1.2)

My day-by-day plan for CCNP ENCOR v1.2, studied live on YouTube ([@baltejgiri](https://www.youtube.com/@baltejgiri)) every morning at 5:00. It uses the same method I used to pass CCNA: read the Official Cert Guide, take notes in my own words, lab every chapter, and review with spaced repetition.

I'm not booking the exam on a date. I book it when the material is covered and the practice tests say I'm ready (see [Readiness gates](#readiness-gates)).

## Resources

- **Book:** *CCNP and CCIE Enterprise Core ENCOR 350-401 Official Cert Guide*, 2nd edition (Cisco Press). Not included here; it's copyrighted.
- **Video:** INE, *Enterprise CORE Exam: 350-401 ENCOR v1.2*
- **Labs:** Cisco Modeling Labs (personal license, 20 nodes) on a home server; topologies in [`labs/`](labs/)
- **Practice tests:** Pearson Test Prep (included with the book) for block tests; Boson ExSim for final readiness
- **Progress board:** [Project ENCOR on GitHub Projects](https://github.com/users/baltejgiri/projects/3)

## What's in here

| File | What it is |
|---|---|
| [`encor-session-schedule.csv`](encor-session-schedule.csv) | Every study session in order: date, chapter, exact book pages or lab, and a `Done (date)` column |
| [`encor-tracker.csv`](encor-tracker.csv) | All 47 v1.2 blueprint topics mapped to book chapters, with columns for lab done, Anki cards and confidence (1 to 5) |
| [`encor-v1.2-blueprint-map.md`](encor-v1.2-blueprint-map.md) | Which book chapters to read, skim or skip for v1.2 (no wireless), plus the topics the book doesn't cover |
| [`tools/build_schedule.py`](tools/build_schedule.py) | Generates the schedule, and replans it when I fall behind |
| [`tools/github_project.py`](tools/github_project.py) | Syncs the schedule with the GitHub Projects board (one issue per session) |
| [`labs/`](labs/) | CML topologies: each lab has `topology.yaml`, `README.md` and `SOLUTION.md` (exam-style questions, no answers) |
| [`notes/`](notes/) | Chapter notes and flashcards in my own words |
| [`cml-mcp/`](cml-mcp/) | MCP server for creating and managing labs on CML (credentials go in a local `.env`, never committed) |

## The weekly rhythm

| When | Time | What |
|---|---|---|
| Monday to Friday | 5:00 to 6:00 | **Reading:** Anki reviews, a 25-minute sprint, a 5-minute explain-back, a 15-minute sprint (about 12 pages) |
| Saturday and Sunday | 5:00 to 8:00 | **Labs:** Anki, whiteboard recap of the week, two Build, Break, Fix labs, new Anki cards, weekly check |

The first day of a chapter starts with a pre-scan and the "Do I Know This Already?" quiz. The last day ends with an own-words summary and 5 to 6 Anki cards. Labs only come from chapters already finished.

## Blocks: so earlier chapters don't fade

The book is split into 6 blocks of 3 to 5 chapters. No new chapter starts until a block is reviewed:

1. **Review week (weekdays):** one chapter per day. A blank-page recall first, then my notes, the DIKTA quiz again, and the book's "Review All Key Topics" and "Define Key Terms".
2. **Block lab (Saturday):** one topology mixing the whole block, troubleshot without the book.
3. **Block test (Sunday):** a timed Pearson Test Prep exam on the block's chapters, plus about 20% from earlier blocks.

| Block | Chapters |
|---|---|
| B1 Layer 2 | 1, 5, 2, 3, 4 |
| B2 Routing and OSPF | 6, 7, 8, 9, 10 |
| B3 BGP and IP services | 11, 12, 15, 13 |
| B4 QoS, tunnels, architecture | 14, 16, 22, 27, 23 |
| B5 Assurance and security | 24, Catalyst Center AI workflows, 26, 25 |
| B6 Programmability and automation | 28, REST API security, 29 |

Chapters 17 to 21 (wireless) are skipped: wireless isn't on the v1.2 blueprint.

## Tracking on the board

Every session is an issue under its chapter (as a sub-issue), on the [Project ENCOR board](https://github.com/users/baltejgiri/projects/3). Each one has a target date, a week, a block and a session type. **Closing the issue at the end of the stream is the log.** The board's "This week" view is what I show at the start of each stream. Stream replay links go in the issue comments.

## Falling behind (replanning)

Buffer sessions are built into the schedule. If I fall further behind than the buffer covers:

```bash
python3 tools/github_project.py pull           # closed issues -> "Done (date)" in the CSV
python3 tools/build_schedule.py --replan        # reschedule everything not done, from tomorrow
python3 tools/github_project.py push            # new dates and weeks -> the board
```
Finished sessions stay as they are. Everything else moves to new dates with the same rules, so nothing is dropped, only pushed back.

To build a fresh schedule from a different start date:
```bash
python3 tools/build_schedule.py --start 2026-10-19
```
The reading pace (`DAY_PAGES`, default 12 pages per weekday) is set at the top of the script.

## Readiness gates

I book the exam only when all of these are true:

1. Every row in the schedule is done, including all 6 block tests.
2. All 47 tracker topics are at confidence 4 or higher, with notes, Anki cards and (for lab topics) a finished lab.
3. No Anki backlog for at least a week.
4. Boson ExSim practice exams, taken in exam conditions, are consistently at my target score on exams I haven't seen before.
5. Cisco hasn't announced a newer ENCOR version ([certification roadmap](https://cisco.com/go/certroadmap)).

## Using this yourself

Download the CSVs into any spreadsheet app, or fork the repo and change the start date and `DAY_PAGES` to fit your own pace. Page numbers refer to the *CCNP and CCIE Enterprise Core ENCOR 350-401 Official Cert Guide*, 2nd edition (Cisco Press). The book isn't included here; it's copyrighted.

## Sources

- [Cisco 350-401 ENCOR v1.2 exam topics](https://learningcontent.cisco.com/documents/marketing/exam-topics/350-401-ENCORE-v1.2.pdf)
- *CCNP and CCIE Enterprise Core ENCOR 350-401 Official Cert Guide*, 2nd edition, Cisco Press (ISBN 9780138216764)
