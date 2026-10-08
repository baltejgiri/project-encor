#!/usr/bin/env python3
"""Sync encor-session-schedule.csv with the Project ENCOR board (GitHub Projects).

Needs the GitHub CLI logged in with the 'project' scope:
    gh auth login --scopes project

Commands:
  setup         create the custom fields and views (safe to re-run)
  archive-old   archive board items that don't belong to this schedule (reversible in the UI)
  create        create one issue per session (chapter issues as parents), add to the board,
                set fields, link sub-issues. Skips anything already created. --limit N for a trial.
  pull          closed issues -> "Done (date)" column in the CSV
  push          CSV dates -> Start/Target Date and Week on the board (run after a replan)
  status        quick done-vs-planned summary from the board
"""
import argparse, csv, datetime as dt, json, os, re, subprocess, sys, time

OWNER, NUMBER, REPO = "baltejgiri", 3, "baltejgiri/project-encor"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(HERE, "encor-session-schedule.csv")
WEEK1 = dt.date(2026, 10, 19)          # Monday of week 1
N_WEEKS = 45
MARK = re.compile(r"<!-- unit: ([A-Za-z0-9.\-]+) -->")

SESSION_TYPES = [("Chapter", "GRAY"), ("Kickoff", "PURPLE"), ("Read", "BLUE"), ("Lab", "GREEN"),
                 ("Block review", "YELLOW"), ("Block lab", "ORANGE"), ("Block test", "RED"),
                 ("Phase 3", "PINK")]
BLOCKS = [("B1 Layer 2", "BLUE"), ("B2 Routing and OSPF", "GREEN"), ("B3 BGP and IP services", "YELLOW"),
          ("B4 QoS, tunnels, architecture", "ORANGE"), ("B5 Assurance and security", "RED"),
          ("B6 Programmability and automation", "PURPLE"), ("Phase 3", "PINK")]
SLOTS = [("Weekday 5:00-6:00", "BLUE"), ("Weekend 5:00-8:00", "GREEN"), ("Both", "GRAY")]
LABELS = {"read": "1d76db", "lab": "0e8a16", "review": "fbca04", "block-lab": "d93f0b",
          "block-test": "b60205", "chapter": "c5def5", "kickoff": "5319e7", "phase-3": "e99695"}


# ---------------------------------------------------------------- gh helpers
def gh(*args, input=None):
    r = subprocess.run(["gh", *args], input=input, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args[:3])}: {r.stderr.strip()[:500]}")
    return r.stdout


def gql(query, **variables):
    out = gh("api", "graphql", "--input", "-", input=json.dumps({"query": query, "variables": variables}))
    data = json.loads(out)
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"])[:800])
    return data["data"]


def project():
    q = """query($o:String!,$n:Int!){user(login:$o){projectV2(number:$n){id title
      fields(first:50){nodes{
        ... on ProjectV2FieldCommon{id name dataType}
        ... on ProjectV2SingleSelectField{options{id name}}
        ... on ProjectV2IterationField{configuration{iterations{id startDate duration title}
                                                     completedIterations{id startDate duration title}}}}}
      views(first:20){nodes{id name layout}}}}}"""
    p = gql(q, o=OWNER, n=NUMBER)["user"]["projectV2"]
    p["f"] = {f["name"]: f for f in p["fields"]["nodes"] if f}
    return p


def items(p, include_archived=False):
    """All board items with the fields this script cares about."""
    q = """query($id:ID!,$after:String){node(id:$id){... on ProjectV2{items(first:100,after:$after){
      pageInfo{hasNextPage endCursor}
      nodes{id isArchived
        content{__typename ... on Issue{id number title state closedAt body}
                           ... on DraftIssue{title}}
        fieldValues(first:30){nodes{
          ... on ProjectV2ItemFieldTextValue{text field{... on ProjectV2FieldCommon{name}}}
          ... on ProjectV2ItemFieldDateValue{date field{... on ProjectV2FieldCommon{name}}}
          ... on ProjectV2ItemFieldIterationValue{iterationId field{... on ProjectV2FieldCommon{name}}}
          ... on ProjectV2ItemFieldSingleSelectValue{name field{... on ProjectV2FieldCommon{name}}}}}}}}}}"""
    out, after = [], None
    while True:
        d = gql(q, id=p["id"], after=after)["node"]["items"]
        for n in d["nodes"]:
            if n["isArchived"] and not include_archived:
                continue
            vals = {}
            for v in n["fieldValues"]["nodes"]:
                if not v or "field" not in v:
                    continue
                vals[v["field"]["name"]] = v.get("text") or v.get("date") or v.get("iterationId") or v.get("name")
            n["vals"] = vals
            out.append(n)
        if not d["pageInfo"]["hasNextPage"]:
            return out
        after = d["pageInfo"]["endCursor"]


def set_fields(p, item_id, values):
    """values: {field name: python value}. One GraphQL request with aliases."""
    parts, i = [], 0
    for name, val in values.items():
        f = p["f"][name]
        if val in (None, ""):
            v = None
        elif f["dataType"] == "SINGLE_SELECT":
            opt = next(o["id"] for o in f["options"] if o["name"] == val)
            v = f'{{singleSelectOptionId:"{opt}"}}'
        elif f["dataType"] == "DATE":
            v = f'{{date:"{val}"}}'
        elif f["dataType"] == "ITERATION":
            v = f'{{iterationId:"{val}"}}'
        else:
            v = "{text:%s}" % json.dumps(val)
        if v is None:
            parts.append(f'c{i}:clearProjectV2ItemFieldValue(input:{{projectId:"{p["id"]}",itemId:"{item_id}",'
                         f'fieldId:"{f["id"]}"}}){{clientMutationId}}')
        else:
            parts.append(f'u{i}:updateProjectV2ItemFieldValue(input:{{projectId:"{p["id"]}",itemId:"{item_id}",'
                         f'fieldId:"{f["id"]}",value:{v}}}){{clientMutationId}}')
        i += 1
    if parts:
        gql("mutation{" + " ".join(parts) + "}")


def iteration_for(p, date):
    cfg = p["f"]["Week"]["configuration"]
    for it in cfg["iterations"] + cfg["completedIterations"]:
        s = dt.date.fromisoformat(it["startDate"])
        if s <= date < s + dt.timedelta(days=it["duration"]):
            return it["id"]
    return None


# ---------------------------------------------------------------- schedule model
def load_rows():
    with open(CSV) as f:
        return list(csv.DictReader(f))


def parent_key(r):
    uid = r["Unit ID"]
    if uid in ("KICKOFF", "PHASE3"):
        return None
    if uid.startswith(("V-", "BL-", "BT-")):
        return "P-" + uid.split("-")[1]                       # P-B1
    return "P-" + uid.split("-", 1)[1].rsplit("-", 1)[0]      # P-5, P-GAP-4.5


def parent_title(r):
    if r["Unit ID"].startswith(("V-", "BL-", "BT-")):
        return f"{r['Block']}: block review"
    return r["Chapter"]


def session_title(r):
    t, ch = r["Type"], r["Chapter"]
    if t == "Read":
        return f"{ch} · {r['Book pages']}" if r["Book pages"] != "-" else ch
    if t == "Lab":
        return f"Lab · {ch.split(' ', 2)[-1] if ch.startswith('Ch ') else ch}: {r['Plan'].split(';')[0]}"
    if t == "Block review":
        names = {x["Unit ID"].split("-", 1)[1].rsplit("-", 1)[0]: x["Chapter"]
                 for x in load_rows() if x["Unit ID"].startswith("R-")}
        ids = ch.replace("Review: ch ", "").split("+")
        return f"{r['Block'].split()[0]} review · " + " + ".join(names.get(i, i) for i in ids)
    return ch


CHECK = {
    "Read": ["Anki reviews", "Sprint 1 (25 min): read + own-words notes", "Explain-back to camera (5 min)",
             "Sprint 2 (15 min)", "60-second recap", "Close this issue"],
    "Kickoff": ["Show schedule, tracker, blueprint map", "Show CML and Anki deck", "Close this issue"],
    "Lab": ["Anki reviews", "Build (configure + verify)", "Break: chat picks the fault",
            "Fix: symptom → show command → cause → fix → verify", "Anki cards from what broke",
            "Topology + configs saved to labs/", "Close this issue"],
    "Block review": ["Blank-page recall (before opening anything)", "Re-read own notes",
                     "DIKTA quiz again (score: __ / first score: __)",
                     "Book: Review All Key Topics + Define Key Terms", "Close this issue"],
    "Block lab": ["One topology mixing the whole block", "Faults from 2+ chapters, no book",
                  "Topology saved to labs/", "Close this issue"],
    "Block test": ["Pearson Test Prep custom exam: this block + ~20% earlier blocks, timed",
                   "Score: __%", "Review every missed question", "Lower confidence in encor-tracker.csv for weak topics",
                   "Close this issue"],
    "Phase 3": ["Boson ExSim in exam conditions", "Review every miss", "Check readiness gates (README)"],
}


def session_body(r):
    lines = [f"**Block:** {r['Block'] or '-'}  ", f"**Slot:** {r['Slot']}  "]
    if r["Book pages"] != "-":
        lines.append(f"**Book pages:** {r['Book pages']}  ")
    if r["Blueprint"]:
        lines.append(f"**Blueprint:** {r['Blueprint']}  ")
    lines += ["", "### Plan", r["Plan"], "", "### Checklist"]
    lines += [f"- [ ] {c}" for c in CHECK.get(r["Type"], ["Close this issue"])]
    lines += ["", "Stream replay: _(paste link in a comment)_", "",
              "_Dates live on the board and move when the schedule is replanned._",
              f"<!-- unit: {r['Unit ID']} -->"]
    return "\n".join(lines)


def parent_body(key, rows):
    kids = [r for r in rows if parent_key(r) == key]
    bp = sorted({r["Blueprint"] for r in kids if r["Blueprint"]})
    lines = [f"**Block:** {kids[0]['Block']}  ", f"**Sessions:** {len(kids)}  "]
    if bp:
        lines.append(f"**Blueprint:** {', '.join(bp)}  ")
    lines += ["", "Sessions are the sub-issues below. Close each one at the end of its stream.", "",
              f"<!-- unit: {key} -->"]
    return "\n".join(lines)


def existing_issues():
    out = gh("issue", "list", "-R", REPO, "--state", "all", "--limit", "1000",
             "--json", "number,id,title,body,state")
    m = {}
    for i in json.loads(out):
        g = MARK.search(i["body"] or "")
        if g:
            m[g.group(1)] = i
    return m


def create_issue(title, body, labels):
    args = ["api", f"repos/{REPO}/issues", "-f", f"title={title}", "-f", f"body={body}"]
    for l in labels:
        args += ["-f", f"labels[]={l}"]
    i = json.loads(gh(*args))
    return {"number": i["number"], "id": i["node_id"], "title": i["title"]}


def add_to_board(p, content_id):
    q = 'mutation($p:ID!,$c:ID!){addProjectV2ItemById(input:{projectId:$p,contentId:$c}){item{id}}}'
    return gql(q, p=p["id"], c=content_id)["addProjectV2ItemById"]["item"]["id"]


def label_for(t):
    return {"Read": "read", "Lab": "lab", "Block review": "review", "Block lab": "block-lab",
            "Block test": "block-test", "Kickoff": "kickoff", "Phase 3": "phase-3"}[t]


def block_label(b):
    return b.split()[0].lower() if b else None


# ---------------------------------------------------------------- commands
def cmd_setup(a):
    p = project()
    def mk(name, dtype, opts=None, iteration=None):
        if name in p["f"]:
            print(f"field exists: {name}"); return
        inp = {"projectId": p["id"], "dataType": dtype, "name": name}
        if opts:
            inp["singleSelectOptions"] = [{"name": n, "color": c, "description": ""} for n, c in opts]
        if iteration:
            inp["iterationConfiguration"] = iteration
        gql("mutation($i:CreateProjectV2FieldInput!){createProjectV2Field(input:$i){clientMutationId}}", i=inp)
        print(f"field created: {name}")
    mk("Session type", "SINGLE_SELECT", SESSION_TYPES)
    mk("Block", "SINGLE_SELECT", BLOCKS)
    mk("Slot", "SINGLE_SELECT", SLOTS)
    mk("Book pages", "TEXT")
    mk("Blueprint", "TEXT")
    mk("Unit ID", "TEXT")
    mk("Week", "ITERATION", iteration={
        "startDate": WEEK1.isoformat(), "duration": 7,
        "iterations": [{"startDate": (WEEK1 + dt.timedelta(weeks=k)).isoformat(), "duration": 7,
                        "title": f"Week {k + 1}"} for k in range(N_WEEKS)]})
    p = project()
    have = {v["name"] for v in p["views"]["nodes"]}
    show = ["Title", "Status", "Session type", "Block", "Week", "Start Date", "Book pages", "Sub-issues progress"]
    vis = [p["f"][n]["id"] for n in show if n in p["f"]]
    for name, layout, flt in [("This week", "BOARD_LAYOUT", "week:@current -session-type:Chapter"),
                              ("Today and overdue", "TABLE_LAYOUT", 'start-date:<=@today -status:Done -session-type:Chapter'),
                              ("By block", "TABLE_LAYOUT", "is:issue"),
                              ("Timeline", "ROADMAP_LAYOUT", "session-type:Chapter")]:
        if name in have:
            print(f"view exists: {name}"); continue
        v = gql("mutation($i:CreateProjectV2ViewInput!){createProjectV2View(input:$i){projectV2View{id}}}",
                i={"projectId": p["id"], "name": name, "layout": layout,
                   "configuration": {"visibleFieldIds": vis}})["createProjectV2View"]["projectV2View"]["id"]
        gql("mutation($i:UpdateProjectV2ViewInput!){updateProjectV2View(input:$i){clientMutationId}}",
            i={"viewId": v, "filter": flt})
        print(f"view created: {name}  (filter: {flt})")
    for name, color in LABELS.items():
        gh("label", "create", name, "-R", REPO, "--color", color, "--force")
    for b, _ in BLOCKS[:6]:
        gh("label", "create", block_label(b), "-R", REPO, "--color", "ededed", "--force", "--description", b)
    print("labels ok")


def cmd_archive_old(a):
    p = project()
    old = [i for i in items(p) if not i["vals"].get("Unit ID")]
    print(f"{len(old)} items without a Unit ID")
    for i in old:
        c = i["content"] or {}
        print(f"  archive: {c.get('title', '?')}")
        if a.yes:
            gql('mutation($p:ID!,$i:ID!){archiveProjectV2Item(input:{projectId:$p,itemId:$i}){clientMutationId}}',
                p=p["id"], i=i["id"])
    if not a.yes:
        print("dry run: add --yes to archive")


def cmd_create(a):
    p, rows = project(), [r for r in load_rows() if r["Unit ID"] not in ("BUF", "")]
    have = existing_issues()
    board = {i["content"]["id"]: i["id"] for i in items(p) if i["content"] and i["content"].get("id")}
    made = 0
    parents = {}
    for r in rows:
        if a.limit and made >= a.limit:
            break
        pk = parent_key(r)
        if pk and pk not in parents:
            if pk in have:
                parents[pk] = have[pk]
            else:
                kids = [x for x in rows if parent_key(x) == pk]
                iss = create_issue(parent_title(r), parent_body(pk, rows),
                                   ["chapter"] + ([block_label(r["Block"])] if r["Block"] else []))
                item = add_to_board(p, iss["id"])
                set_fields(p, item, {"Session type": "Chapter", "Block": r["Block"], "Unit ID": pk,
                                     "Start Date": min(k["Date"] for k in kids),
                                     "Target Date": max(k["Date"] for k in kids),
                                     "Blueprint": ", ".join(sorted({k["Blueprint"] for k in kids if k["Blueprint"]}))})
                parents[pk] = iss; have[pk] = iss; made += 1
                print(f"#{iss['number']} {iss['title']}"); time.sleep(1.2)
        if r["Unit ID"] in have:
            continue
        labels = [label_for(r["Type"])] + ([block_label(r["Block"])] if r["Block"] else [])
        iss = create_issue(session_title(r), session_body(r), labels)
        item = add_to_board(p, iss["id"])
        d = dt.date.fromisoformat(r["Date"]) if r["Date"][:1].isdigit() else None
        set_fields(p, item, {"Session type": r["Type"], "Block": r["Block"] or ("Phase 3" if r["Type"] == "Phase 3" else None),
                             "Slot": r["Slot"], "Book pages": "" if r["Book pages"] == "-" else r["Book pages"],
                             "Blueprint": r["Blueprint"], "Unit ID": r["Unit ID"],
                             "Start Date": d and d.isoformat(), "Target Date": d and d.isoformat(),
                             "Week": d and iteration_for(p, d), "Status": "Todo"})
        if pk:
            gql('mutation($a:ID!,$b:ID!){addSubIssue(input:{issueId:$a,subIssueId:$b}){clientMutationId}}',
                a=parents[pk]["id"], b=iss["id"])
        have[r["Unit ID"]] = iss; made += 1
        print(f"#{iss['number']} {iss['title']}"); time.sleep(1.2)
    print(f"created {made} issues")


def cmd_pull(a):
    p, rows = project(), load_rows()
    closed = {}
    for i in items(p):
        c, uid = i["content"] or {}, i["vals"].get("Unit ID")
        if uid and c.get("state") == "CLOSED" and c.get("closedAt"):
            closed[uid] = c["closedAt"][:10]
    n = 0
    for r in rows:
        if r["Unit ID"] in closed and not r["Done (date)"].strip():
            r["Done (date)"] = closed[r["Unit ID"]]; n += 1
    with open(CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    print(f"marked {n} rows done from closed issues")


def cmd_push(a):
    p, rows = project(), load_rows()
    by_uid = {i["vals"].get("Unit ID"): i for i in items(p) if i["vals"].get("Unit ID")}
    n = 0
    for r in rows:
        it = by_uid.get(r["Unit ID"])
        if not it or not r["Date"][:1].isdigit() or r["Done (date)"].strip():
            continue
        d = dt.date.fromisoformat(r["Date"])
        want = {"Start Date": d.isoformat(), "Target Date": d.isoformat(), "Week": iteration_for(p, d)}
        if any(it["vals"].get(k) != v for k, v in want.items()):
            set_fields(p, it["id"], want); n += 1
    for key, it in by_uid.items():
        if not key.startswith("P-"):
            continue
        kids = [r for r in rows if r["Unit ID"] not in ("BUF", "") and parent_key(r) == key]
        if kids:
            want = {"Start Date": min(k["Date"] for k in kids), "Target Date": max(k["Date"] for k in kids)}
            if any(it["vals"].get(k) != v for k, v in want.items()):
                set_fields(p, it["id"], want); n += 1
    print(f"updated dates on {n} board items")


def cmd_status(a):
    p = project()
    today = dt.date.today().isoformat()
    sess = [i for i in items(p) if i["vals"].get("Unit ID") and i["vals"].get("Session type") != "Chapter"]
    due = [i for i in sess if (i["vals"].get("Start Date") or "9999") <= today]
    done = [i for i in sess if (i["content"] or {}).get("state") == "CLOSED"]
    late = [i for i in due if (i["content"] or {}).get("state") != "CLOSED"]
    print(f"sessions: {len(sess)}  due by today: {len(due)}  done: {len(done)}  overdue: {len(late)}")
    for i in sorted(late, key=lambda x: x["vals"].get("Start Date", ""))[:15]:
        print(f"  overdue {i['vals'].get('Start Date')}  #{i['content'].get('number')} {i['content'].get('title')}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("setup")
    x = sp.add_parser("archive-old"); x.add_argument("--yes", action="store_true")
    x = sp.add_parser("create"); x.add_argument("--limit", type=int, default=0)
    sp.add_parser("pull"); sp.add_parser("push"); sp.add_parser("status")
    a = ap.parse_args()
    {"setup": cmd_setup, "archive-old": cmd_archive_old, "create": cmd_create,
     "pull": cmd_pull, "push": cmd_push, "status": cmd_status}[a.cmd](a)


if __name__ == "__main__":
    main()
