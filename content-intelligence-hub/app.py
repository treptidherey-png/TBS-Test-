from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import json
import re
from html import escape

ROOT = Path(__file__).parent
DATA = ROOT / "data.json"

RECORD_TYPES = [
    "Content Draft", "Content Opportunity", "Buyer Insight", "Founder Observation",
    "Market Signal", "Research", "Competitor Reference", "Proof / Evidence",
    "Published Content", "Content Learning"
]

AVAILABLE_STATUSES = {"Captured", "Developed", "Recommended", "Awaiting Trepti Approval", "Approved"}
CALENDAR_STATUSES = {"Scheduled", "Published"}

@dataclass
class Record:
    id: str
    title: str
    record_type: str
    raw_input: str
    source: str = ""
    observation: str = ""
    interpretation: str = ""
    audience_relevance: str = ""
    evidence_status: str = "Unverified"
    lifecycle_status: str = "Captured"
    scheduled_date: str = ""
    scheduled_slot: str = ""
    created_at: str = ""
    updated_at: str = ""


def load_records():
    if not DATA.exists():
        return []
    return json.loads(DATA.read_text(encoding="utf-8"))


def save_records(records):
    DATA.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")


def now():
    return datetime.now(timezone.utc).isoformat()


def make_id(title):
    base = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:40] or "record"
    return f"{base}-{int(datetime.now().timestamp() * 1000)}"


def search(records, q):
    terms = [x for x in re.findall(r"\w+", q.lower()) if len(x) > 2]
    if not terms:
        return records
    scored = []
    for r in records:
        hay = " ".join(str(r.get(k, "")) for k in r).lower()
        score = sum(hay.count(t) for t in terms)
        if score:
            scored.append((score, r))
    return [r for _, r in sorted(scored, key=lambda x: x[0], reverse=True)]


def available_records(records):
    return [r for r in records if r.get("lifecycle_status", "Captured") in AVAILABLE_STATUSES and not r.get("scheduled_date")]


def calendar_records(records):
    return sorted(
        [r for r in records if r.get("scheduled_date") or r.get("lifecycle_status") in CALENDAR_STATUSES],
        key=lambda r: (r.get("scheduled_date", "9999-12-31"), r.get("scheduled_slot", ""), r.get("title", "")),
    )


def update_record(records, record_id, **changes):
    for record in records:
        if record.get("id") == record_id:
            record.update(changes)
            record["updated_at"] = now()
            return record
    return None


def page(title, body):
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>{escape(title)} | TBS Content Intelligence Hub</title>
<style>
body{{font-family:Inter,system-ui,sans-serif;max-width:1100px;margin:40px auto;padding:0 20px;background:#111;color:#f5f5f5}}
a{{color:#f5d84a;text-decoration:none}} .nav{{display:flex;gap:18px;flex-wrap:wrap;margin-bottom:36px}}
.card{{background:#1b1b1b;border:1px solid #333;border-radius:12px;padding:18px;margin:12px 0}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px}}
input,textarea,select{{width:100%;box-sizing:border-box;background:#101010;color:#fff;border:1px solid #444;border-radius:8px;padding:11px;margin:6px 0 14px}}
button{{background:#f5d84a;color:#111;border:0;border-radius:8px;padding:10px 14px;font-weight:700;cursor:pointer}}
button.secondary{{background:#333;color:#fff}} .tag{{display:inline-block;border:1px solid #555;border-radius:999px;padding:4px 8px;font-size:12px;margin-right:6px}}
small{{color:#aaa}} h1{{margin-bottom:8px}} h2{{margin-top:0}} .muted{{color:#aaa}}
</style></head><body>
<div class="nav"><a href="/">Home</a><a href="/capture">Capture</a><a href="/inventory">Master Content Inventory</a><a href="/develop">Develop an Idea</a><a href="/calendar">Content Calendar</a></div>
{body}</body></html>"""


def home():
    body = """<h1>TBS Content Intelligence Hub</h1>
<p>One master content pool. Use existing work first. Move selected pieces into the active calendar.</p>
<div class="grid">
<div class="card"><h2>Capture</h2><p>Put useful ideas, observations, research, proof, and drafts into the master pool.</p><a href="/capture">Capture intelligence →</a></div>
<div class="card"><h2>Master Content Inventory</h2><p>Everything available to use, with its current lifecycle status.</p><a href="/inventory">Open inventory →</a></div>
<div class="card"><h2>Develop an Idea</h2><p>Search the existing pool before researching or creating something new.</p><a href="/develop">Develop an idea →</a></div>
<div class="card"><h2>Content Calendar</h2><p>Selected content leaves the available pool and becomes scheduled work.</p><a href="/calendar">Open calendar →</a></div>
</div>"""
    return page("Home", body)


def capture():
    body = """<h1>Capture</h1><p>Do not over-classify. Record the useful thing. Content can be organized later.</p>
<form method="post">
<label>Title</label><input name="title" required>
<label>Type</label><select name="record_type">""" + "".join(f'<option>{escape(t)}</option>' for t in RECORD_TYPES) + """</select>
<label>What happened / what did you find?</label><textarea name="raw_input" rows="6" required></textarea>
<label>Source</label><input name="source" placeholder="Fireflies, client call, research URL, own observation, etc.">
<label>Evidence status</label><select name="evidence_status"><option>Verified</option><option>Inferred</option><option selected>Unverified</option></select>
<button>Save to master inventory</button></form>"""
    return page("Capture", body)


def inventory(records, q="", status=""):
    pool = available_records(records)
    if q:
        pool = search(pool, q)
    if status:
        pool = [r for r in pool if r.get("lifecycle_status") == status]
    cards = ""
    for r in pool:
        cards += f"""<div class="card"><span class="tag">{escape(r.get('record_type',''))}</span><span class="tag">{escape(r.get('lifecycle_status','Captured'))}</span>
<h3>{escape(r.get('title',''))}</h3><p>{escape(r.get('raw_input',''))}</p>
<small>Source: {escape(r.get('source','') or 'Not recorded')} · Evidence: {escape(r.get('evidence_status',''))}</small>
<form method="post" action="/schedule" style="margin-top:14px"><input type="hidden" name="id" value="{escape(r.get('id',''))}">
<label>Schedule date</label><input type="date" name="scheduled_date" required>
<label>Slot</label><input name="scheduled_slot" placeholder="e.g. Tuesday, TOFU" required>
<button>Move to calendar</button></form></div>"""
    body = f"""<h1>Master Content Inventory</h1>
<p>This is the available content pool. Once a piece is moved to the calendar, it no longer appears here.</p>
<form method="get"><input name="q" value="{escape(q)}" placeholder="Search the master inventory">
<select name="status"><option value="">All available statuses</option>""" + "".join(
        f'<option value="{escape(s)}"' + (' selected' if status == s else '') + f'>{escape(s)}</option>' for s in sorted(AVAILABLE_STATUSES)
    ) + f"""</select><button>Filter inventory</button></form>
<p class="muted">{len(pool)} available item(s)</p>
{cards or '<div class="card"><p>No available content matches this view. That is a signal to identify a genuine gap, not to duplicate existing work.</p></div>'}"""
    return page("Master Content Inventory", body)


def develop(records, q="", notice=""):
    results = search(available_records(records), q) if q else []
    cards = ""
    for r in results[:12]:
        cards += f"""<div class="card"><span class="tag">{escape(r.get('record_type',''))}</span><span class="tag">{escape(r.get('lifecycle_status','Captured'))}</span>
<h3>{escape(r.get('title',''))}</h3><p>{escape(r.get('raw_input',''))}</p>
<small>Source: {escape(r.get('source','') or 'Not recorded')} · Evidence: {escape(r.get('evidence_status',''))}</small></div>"""
    body = f"""<h1>Develop an Idea</h1>
<p>Search the master inventory first. Research only what is genuinely missing.</p>
<form method="get"><label>What do you want to post about?</label>
<input name="q" value="{escape(q)}" placeholder="e.g. founders with strong businesses but weak LinkedIn presence">
<button>Search existing content</button></form>
{f'<div class="card"><strong>{escape(notice)}</strong></div>' if notice else ''}
<h2>Existing content and intelligence</h2>{cards or '<p><small>No matching available content yet. This is a potential gap, not a reason to invent evidence.</small></p>'}
<div class="card"><h2>Next decision</h2>
<p>The MVP stops before drafting. After evidence and interpretation are developed, one direction can be recommended and sent to the Trepti approval gate.</p></div>"""
    return page("Develop an Idea", body)


def calendar_view(records):
    items = calendar_records(records)
    cards = ""
    for r in items:
        cards += f"""<div class="card"><span class="tag">{escape(r.get('scheduled_date',''))}</span><span class="tag">{escape(r.get('scheduled_slot',''))}</span><span class="tag">{escape(r.get('lifecycle_status',''))}</span>
<h3>{escape(r.get('title',''))}</h3><p>{escape(r.get('raw_input',''))}</p>
<form method="post" action="/unschedule"><input type="hidden" name="id" value="{escape(r.get('id',''))}"><button class="secondary">Return to master inventory</button></form></div>"""
    body = f"""<h1>Content Calendar</h1>
<p>Only content selected for a publishing slot appears here. Moving it back returns it to the master inventory.</p>
{cards or '<div class="card"><p>No content has been scheduled yet.</p></div>'}"""
    return page("Content Calendar", body)


def create_record(form):
    records = load_records()
    title = form.get("title", "").strip()
    record = Record(
        id=make_id(title), title=title, record_type=form.get("record_type", "Research"),
        raw_input=form.get("raw_input", "").strip(), source=form.get("source", "").strip(),
        evidence_status=form.get("evidence_status", "Unverified"), created_at=now(), updated_at=now()
    )
    records.append(asdict(record))
    save_records(records)
    return records


def main():
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from urllib.parse import urlparse, parse_qs

    class Handler(BaseHTTPRequestHandler):
        def send_html(self, content, status=200):
            data = content.encode()
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def form_data(self):
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode()
            return {k: v[0] for k, v in parse_qs(raw).items()}

        def do_GET(self):
            u = urlparse(self.path)
            if u.path == "/": self.send_html(home()); return
            if u.path == "/capture": self.send_html(capture()); return
            if u.path == "/inventory":
                params = parse_qs(u.query)
                self.send_html(inventory(load_records(), params.get("q", [""])[0], params.get("status", [""])[0])); return
            if u.path == "/develop":
                q = parse_qs(u.query).get("q", [""])[0]
                self.send_html(develop(load_records(), q=q)); return
            if u.path == "/calendar": self.send_html(calendar_view(load_records())); return
            self.send_html(page("Not found", "<h1>404</h1>"), 404)

        def do_POST(self):
            if self.path == "/capture":
                records = create_record(self.form_data())
                self.send_html(inventory(records, notice="")); return
            if self.path == "/schedule":
                form = self.form_data(); records = load_records()
                record = update_record(records, form.get("id", ""), lifecycle_status="Scheduled", scheduled_date=form.get("scheduled_date", ""), scheduled_slot=form.get("scheduled_slot", ""))
                if not record: self.send_html(page("Not found", "<h1>Record not found</h1>"), 404); return
                save_records(records); self.send_html(calendar_view(records)); return
            if self.path == "/unschedule":
                form = self.form_data(); records = load_records()
                record = update_record(records, form.get("id", ""), lifecycle_status="Approved", scheduled_date="", scheduled_slot="")
                if not record: self.send_html(page("Not found", "<h1>Record not found</h1>"), 404); return
                save_records(records); self.send_html(inventory(records)); return
            self.send_html(page("Not found", "<h1>404</h1>"), 404)

    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()


if __name__ == "__main__":
    main()
