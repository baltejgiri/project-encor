#!/usr/bin/env python3
"""Build (or rebuild) the ENCOR day-by-day study schedule.

Weekdays (Mon-Fri, 5:00-6:00): reading.  Weekends (Sat-Sun, 5:00-8:00): labs.
Chapters are grouped into blocks; after each block comes a review week
(weekdays: one chapter per day re-read/recall) and a block weekend
(Saturday mixed troubleshooting lab, Sunday chapter-filtered practice test).

Usage:
  python3 tools/build_schedule.py                      # fresh plan from START
  python3 tools/build_schedule.py --start 2026-10-19
  python3 tools/build_schedule.py --replan --from 2026-11-09
      keeps every row whose "Done" column is filled, and reschedules
      everything not done yet starting at --from (default: tomorrow).
"""
import argparse, csv, datetime as dt, os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "encor-session-schedule.csv")

FIRST_DAY_PAGES = 8   # pre-scan + DIKTA quiz + one 25-min sprint
DAY_PAGES = 12        # 25-min sprint + 5-min explain-back + 15-min sprint
LAST_DAY_MAX = 8      # last day of a chapter also holds the summary + Anki cards

# Block -> list of (chapter id, title, page ranges or None, note, labs, blueprint)
BLOCKS = [
 ("B1 Layer 2", [
  ("1", "Packet Forwarding", None, "Refresher: re-read notes/ch01-packet-forwarding.md and notes/ch01-lab01-flashcards.md from May; skim pp 2-35. Labs already done (labs/ch01-*)", [], "-"),
  ("5", "VLAN Trunks and EtherChannel", [(94, 123)], "", [
     "DTP trunk modes, allowed VLANs, native VLAN mismatch: Build, Break, Fix",
     "LACP/PAgP EtherChannel: mode and config mismatches: Build, Break, Fix"], "3.1.a, 3.1.b"),
  ("2", "Spanning Tree Protocol", [(36, 57)], "", [], "3.1.c"),
  ("3", "Advanced STP Tuning", [(58, 79)], "", [
     "RSTP root election, port roles, priority/cost tuning (covers ch 2 + 3)",
     "Root guard, BPDU guard, PortFast, err-disable recovery: Build, Break, Fix"], "3.1.c"),
  ("4", "Multiple Spanning Tree Protocol", [(80, 93)], "", [
     "MST region, instance-to-VLAN mapping",
     "MST region mismatch / boundary ports: Break, Fix"], "3.1.c"),
 ], ["5", "2", "3", "4"]),
 ("B2 Routing and OSPF", [
  ("6", "IP Routing Essentials", [(124, 153)], "", [
     "VRF-lite with overlapping customer subnets",
     "Policy-based routing next-hop override"], "3.2.d, 2.2.a"),
  ("7", "EIGRP", [(154, 169)], "Concepts only: compare with OSPF", [
     "EIGRP vs OSPF side by side: metrics, load balancing, path selection"], "3.2.a"),
  ("8", "OSPF", [(170, 201)], "", [
     "Single-area OSPF, DR/BDR election",
     "OSPF adjacency faults: MTU, timers, area, network type, passive-interface"], "3.2.b"),
  ("9", "Advanced OSPF", [(202, 229)], "", [
     "Multi-area OSPF with ABR/ASBR summarization",
     "OSPF route filtering"], "3.2.b"),
  ("10", "OSPFv3", [(230, 243)], "", [
     "OSPFv3 dual stack (address families): Build, Break, Fix"], "3.2.b"),
 ], ["6", "7", "8", "9", "10"]),
 ("B3 BGP and IP services", [
  ("11", "BGP", [(244, 287)], "", [
     "eBGP between directly connected neighbors, network advertisement",
     "eBGP neighbor faults: wrong AS, source address, TCP 179 blocked"], "3.2.c"),
  ("12", "Advanced BGP", [(288, 295), (318, 333)], "Skip pp 296-317 (route maps/filtering: ENARSI depth)", [
     "Best path: weight vs local preference",
     "Best path: AS path prepend and MED"], "3.2.c"),
  ("15", "IP Services", [(418, 465)], "NTP/PTP: interpret only", [
     "NAT: static, pooled, PAT: Build, Break, Fix",
     "HSRP and VRRP with object tracking",
     "Read and verify NTP/PTP configs"], "3.3.a-c"),
  ("13", "Multicast", [(334, 369)], "Describe only", [], "3.3.d"),
 ], ["11", "12", "15", "13"]),
 ("B4 QoS, tunnels, architecture", [
  ("14", "Quality of Service", [(370, 392), (394, 417)], "Skip p393 (Wireless QoS)", [
     "Read an MQC policy: classify, mark, police, queue (interpret show policy-map)"], "1.4"),
  ("16", "Overlay Tunnels", [(466, 509)], "LISP/VXLAN: describe only", [
     "GRE tunnel with routing over it",
     "GRE over IPsec and VTI"], "2.2.b, 2.3"),
  ("22", "Enterprise Network Architecture", [(622, 641)], "", [], "1.1"),
  ("27", "Virtualization", [(826, 833)], "Skim pp 833-849 (NFV/ENFV not on v1.2)", [], "2.1"),
  ("23", "Fabric Technologies", [(642, 671)], "Skip fabric WLC detail", [
     "SD-WAN and SD-Access tour (DevNet sandbox)"], "1.2, 1.3"),
 ], ["14", "16", "22+27", "23"]),
 ("B5 Assurance and security", [
  ("24", "Network Assurance", [(672, 735)], "", [
     "Conditional debug, syslog, SNMP",
     "Flexible NetFlow",
     "SPAN, RSPAN, ERSPAN",
     "IP SLA with tracking"], "4.1-4.5"),
  ("GAP-4.5", "Catalyst Center AI-powered workflows", None,
     "Not in book: Cisco Catalyst Center docs", [
     "Catalyst Center sandbox: assurance and AI workflows (DevNet)"], "4.5"),
  ("26", "Device Access Control and Infrastructure Security", [(778, 825)], "ZBFW: skim (not on v1.2)", [
     "Local users, lines, AAA with local fallback",
     "ACLs and CoPP: Build, Break, Fix"], "5.1, 5.2"),
  ("25", "Secure Network Access Control", [(736, 777)], "Describe only; 802.1X lightly", [], "5.4"),
 ], ["24", "GAP-4.5", "26", "25"]),
 ("B6 Programmability and automation", [
  ("28", "Foundational Network Programmability", [(850, 891)], "", [
     "Construct JSON, read Python, decode REST response codes (Postman)",
     "NETCONF and RESTCONF on IOS-XE (Cat8000v)",
     "Catalyst Center / SD-WAN Manager APIs (DevNet sandbox)"], "4.6, 6.1-6.5"),
  ("GAP-5.3", "REST API security", None,
     "Not in book: basic/token/OAuth auth, HTTPS, API keys vs tokens", [], "5.3"),
  ("29", "Introduction to Automation Tools", [(892, 925)], "Agent vs agentless: compare only", [
     "EEM applet triggered by syslog",
     "EEM applet for timed data collection"], "6.6, 6.7"),
 ], ["28", "GAP-5.3", "29"]),
]


def chname(cid, title):
    return f"Gap: {title}" if cid.startswith("GAP") else f"Ch {cid} {title}"


def fmt_pages(pages):
    out, s, p = [], pages[0], pages[0]
    for x in pages[1:]:
        if x != p + 1:
            out.append(f"{s}-{p}"); s = x
        p = x
    out.append(f"{s}-{p}")
    return "pp " + ", ".join(out)


def build_units():
    """Ordered units. kind: read | lab | review | blocklab | blocktest."""
    units = [dict(id="KICKOFF", kind="read", block="B1 Layer 2", ch="-", chapter="Kickoff",
                  pages="-", plan="Stream tour: schedule, tracker, blueprint map, CML, Anki deck", bp="")]
    for bname, chapters, review in BLOCKS:
        bid = bname.split()[0]
        for cid, title, ranges, note, labs, bp in chapters:
            name = chname(cid, title)
            if ranges is None:
                units.append(dict(id=f"R-{cid}-1", kind="read", block=bname, ch=cid, chapter=name, pages="-",
                                  plan=f"{note}. Own-words summary + Anki cards", bp=bp))
            else:
                pages = [p for a, b in ranges for p in range(a, b + 1)]
                chunks, i = [pages[:FIRST_DAY_PAGES]], FIRST_DAY_PAGES
                while i < len(pages):
                    rem = len(pages) - i
                    if rem <= LAST_DAY_MAX:
                        n = rem                      # final day: pages + summary + cards
                    elif rem <= DAY_PAGES + 4:
                        n = rem - 4                  # leave at least 4 pages for the final day
                    else:
                        n = DAY_PAGES
                    chunks.append(pages[i:i + n]); i += n
                for k, c in enumerate(chunks, 1):
                    if k == 1:
                        plan = "Pre-scan + DIKTA quiz (chat answers) + 1 sprint"
                        if note:
                            plan += f". Note: {note}"
                    else:
                        plan = "Sprints (25 + 15 min) with explain-back"
                    if k == len(chunks):
                        plan += "; own-words summary; write 5-6 Anki cards"
                    units.append(dict(id=f"R-{cid}-{k}", kind="read", block=bname, ch=cid, chapter=name,
                                      pages=fmt_pages(c), plan=plan, bp=bp))
            for k, lab in enumerate(labs, 1):
                units.append(dict(id=f"L-{cid}-{k}", kind="lab", block=bname, ch=cid, chapter=name, pages="-",
                                  plan=lab + "; Anki cards from what broke", bp=bp))
        for k, rc in enumerate(review, 1):
            units.append(dict(id=f"V-{bid}-{k}", kind="review", block=bname, ch=rc,
                              chapter=f"Review: ch {rc}", pages="-",
                              plan="Recall first (blank page: what do I remember?), then re-read own notes, "
                                   "redo DIKTA quiz, book's 'Review All Key Topics' + 'Define Key Terms'",
                              bp=""))
        units.append(dict(id=f"BL-{bid}", kind="blocklab", block=bname, ch="", chapter=f"{bname}: mixed lab",
                          pages="-", plan="One topology combining the block's topics; troubleshoot from scratch "
                                          "without the book (faults from 2+ chapters at once)", bp=""))
        units.append(dict(id=f"BT-{bid}", kind="blocktest", block=bname, ch="", chapter=f"{bname}: block test",
                          pages="-", plan="Pearson Test Prep (book's code), custom exam: this block's chapters "
                                          "+ ~20% from earlier blocks, timed. Review every miss, log weak "
                                          "topics in tracker", bp=""))
    return units


def schedule(units, start, done_ids):
    todo = [u for u in units if u["id"] not in done_ids]
    done = set(done_ids)
    rows, d = [], start
    review_week_ok = {}   # block -> earliest Monday its review may start

    def block_units(b, kinds):
        return [u for u in units if u["block"] == b and u["kind"] in kinds]

    def all_done(us):
        return all(u["id"] in done for u in us)

    guard = 0
    while todo and guard < 2000:
        guard += 1
        wd = d.weekday()
        if wd < 5:   # weekday: one 1-hour slot
            pick = None
            for u in todo:
                if u["kind"] == "read":
                    # a block's reading waits until the previous block's review week is done
                    prev = [b for b, *_ in BLOCKS]
                    bi = prev.index(u["block"])
                    if bi == 0 or all_done(block_units(prev[bi - 1], ["review"])):
                        pick = u
                    break
            if pick is None:
                for u in todo:
                    if u["kind"] == "review":
                        b = u["block"]
                        if all_done(block_units(b, ["read"])):
                            if b not in review_week_ok:
                                last = max(r["date"] for r in rows if r.get("block") == b and r["kind"] == "read") \
                                    if any(r.get("block") == b and r["kind"] == "read" for r in rows) else d
                                review_week_ok[b] = last + dt.timedelta(days=(7 - last.weekday()))
                            if d >= review_week_ok[b]:
                                pick = u
                        break
            if pick:
                rows.append(dict(pick, date=d, slot="Weekday 5:00-6:00")); done.add(pick["id"]); todo.remove(pick)
            else:
                rows.append(dict(id="BUF", kind="buffer", block="", ch="", chapter="Buffer", pages="-",
                                 plan="Catch up if behind; otherwise extra Anki + re-read last chapter's notes",
                                 bp="", date=d, slot="Weekday 5:00-6:00"))
        else:        # weekend: one 3-hour slot = 2 labs, or 1 block lab, or 1 block test
            taken = []
            for u in todo:
                if u["kind"] == "lab":
                    if all_done([x for x in units if x["kind"] == "read" and x["ch"] == u["ch"]]):
                        taken.append(u)
                        if len(taken) == 2:
                            break
            if not taken:
                for u in todo:
                    if u["kind"] in ("blocklab", "blocktest"):
                        b = u["block"]
                        if all_done(block_units(b, ["read", "lab", "review"])) and \
                                (u["kind"] == "blocklab" or f"BL-{b.split()[0]}" in done):
                            taken = [u]
                        break
            if taken:
                for u in taken:
                    rows.append(dict(u, date=d, slot="Weekend 5:00-8:00")); done.add(u["id"]); todo.remove(u)
            else:
                rows.append(dict(id="BUF", kind="buffer", block="", ch="", chapter="Buffer", pages="-",
                                 plan="Catch up any missed reading or labs; otherwise concept review: "
                                      "Pearson questions for chapters read so far",
                                 bp="", date=d, slot="Weekend 5:00-8:00"))
        d += dt.timedelta(days=1)
    rows.append(dict(id="PHASE3", kind="phase3", block="", ch="", chapter="Phase 3: practice exams", pages="-",
                     plan="Weekends: full Boson ExSim exam in exam conditions + review. Weekdays: Anki + review "
                          "missed questions. Continue until readiness gates are met, then book the exam.",
                     bp="all", date=d, slot="Both"))
    return rows


TYPES = {"read": "Read", "lab": "Lab", "review": "Block review", "blocklab": "Block lab",
         "blocktest": "Block test", "buffer": "Buffer", "phase3": "Phase 3"}
HEAD = ["Day", "Date", "Weekday", "Slot", "Type", "Block", "Chapter", "Book pages", "Plan",
        "Blueprint", "Unit ID", "Done (date)"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2026-10-19")
    ap.add_argument("--replan", action="store_true")
    ap.add_argument("--from", dest="frm")
    a = ap.parse_args()
    units = build_units()
    kept, done_ids = [], []
    start = dt.date.fromisoformat(a.start)
    if a.replan:
        with open(OUT) as f:
            for r in csv.DictReader(f):
                if r["Done (date)"].strip():
                    kept.append(r)
                    if r["Unit ID"] != "BUF":
                        done_ids.append(r["Unit ID"])
        start = dt.date.fromisoformat(a.frm) if a.frm else dt.date.today() + dt.timedelta(days=1)
    rows = schedule(units, start, done_ids)
    with open(OUT, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(HEAD)
        n = 0
        for r in kept:
            n += 1
            w.writerow([n] + [r[h] for h in HEAD[1:]])
        for r in rows:
            n += 1
            dd = r["date"]
            w.writerow([n, dd.isoformat(), dd.strftime("%a"), r["slot"], TYPES[r["kind"]], r["block"],
                        r["chapter"], r["pages"], r["plan"], r["bp"], r["id"], ""])
    print(f"wrote {OUT}: {n} sessions, last scheduled {rows[-1]['date']}")


if __name__ == "__main__":
    main()
