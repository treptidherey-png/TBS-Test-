from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import json
import re
from html import escape
from urllib.parse import quote

ROOT = Path(__file__).parent
DATA = ROOT / "data.json"

RECORD_TYPES = [
    "Buyer Insight", "Founder Observation", "Market Signal", "Research",
    "Competitor Reference", "Proof / Evidence", "Content Opportunity",
    "Published Content", "Content Learning"
]

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
    return f"{base}-{int(datetime.now().timestamp())}"

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

def page(title, body):
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>{escape(title)} | TBS Content Intelligence Hub</title>
<style>
body{{font-family:Inter,system-ui,sans-serif;max-width:980px;margin:40px auto;padding:0 20px;background:#111;color:#f5f5f5}}
a{{color:#f5d84a;text-decoration:none}} .nav{{display:flex;gap:18px;margin-bottom:36px}}
.card{{background:#1b1b1b;border:1px solid #333;border-radius:12px;padding:18px;margin:12px 0}}
input,textarea,select{{width:100%;box-sizing:border-box;background:#101010;color:#fff;border:1px solid #444;border-radius:8px;padding:11px;margin:6px 0 14px}}
button{{background:#f5d84a;color:#111;border:0;border-radius:8px;padding:11px 16px;font-weight:700;cursor:pointer}}
.tag{{display:inline-block;border:1px solid #555;border-radius:999px;padding:4px 8px;font-size:12px;margin-right:6px}}
small{{color:#aaa}} h1{{margin-bottom:8px}} h2{{margin-top:0}}
</style></head><body>
<div class="nav"><a href="/">Home</a><a href="/capture">Capture</a><a href="/develop">Develop an Idea</a></div>
{body}</body></html>"""

def home():
    body = """<h1>TBS Content Intelligence Hub</h1>
<p>Capture what happens. Search what we already know. Develop only the gaps.</p>
<div class="card"><h2>Capture</h2><p>Save a buyer insight, founder observation, market signal, research item, proof, competitor mechanism, or learning.</p><a href="/capture">Capture intelligence →</a></div>
<div class="card"><h2>Develop an Idea</h2><p>Start with a topic. The hub searches existing intelligence before new research is considered.</p><a href="/develop">Develop an idea →</a></div>
<div class="card"><h2>Content Pipeline</h2><p>Coming after the decision workflow is proven: approved direction → creation → publication → measurement → learning.</p></div>"""
    return page("Home", body)

def capture():
    body = """<h1>Capture</h1><p>Do not over-classify. Record the useful thing.</p>
<form method="post">
<label>Title</label><input name="title" required>
<label>Type</label><select name="record_type">""" + "".join(f'<option>{escape(t)}</option>' for t in RECORD_TYPES) + """</select>
<label>What happened / what did you find?</label><textarea name="raw_input" rows="6" required></textarea>
<label>Source</label><input name="source" placeholder="Fireflies, client call, research URL, own observation, etc.">
<label>Evidence status</label><select name="evidence_status"><option>Verified</option><option>Inferred</option><option selected>Unverified</option></select>
<button>Save intelligence</button></form>"""
    return page("Capture", body)

def develop(records, q="", notice=""):
    results = search(records, q) if q else []
    cards = ""
    for r in results[:12]:
        cards += f"""<div class="card"><span class="tag">{escape(r.get('record_type',''))}</span>
<h3>{escape(r.get('title',''))}</h3><p>{escape(r.get('raw_input',''))}</p>
<small>Source: {escape(r.get('source','') or 'Not recorded')} · Evidence: {escape(r.get('evidence_status',''))}</small></div>"""
    body = f"""<h1>Develop an Idea</h1>
<p>Search first. Research only what is genuinely missing.</p>
<form method="get"><label>What do you want to post about?</label>
<input name="q" value="{escape(q)}" placeholder="e.g. founders with strong businesses but weak LinkedIn presence">
<button>Search existing intelligence</button></form>
{f'<div class="card"><strong>{escape(notice)}</strong></div>' if notice else ''}
<h2>Known / related intelligence</h2>{cards or '<p><small>No matching intelligence yet. This is a gap, not a reason to invent evidence.</small></p>'}
<div class="card"><h2>Next decision</h2>
<p>The MVP intentionally stops before drafting. Once the evidence and interpretation are developed, create one recommended direction and send it to the Trepti approval gate.</p></div>"""
    return page("Develop an Idea", body)

def handle_post(form):
    records = load_records()
    t = form.get("title","").strip()
    r = Record(
        id=make_id(t), title=t, record_type=form.get("record_type","Research"),
        raw_input=form.get("raw_input","").strip(), source=form.get("source","").strip(),
        evidence_status=form.get("evidence_status","Unverified"), created_at=now(), updated_at=now()
    )
    records.append(asdict(r)); save_records(records)
    return develop(records, notice=f"Captured: {t}")

def main():
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from urllib.parse import urlparse, parse_qs
    from urllib.parse import unquote
    import html

    class Handler(BaseHTTPRequestHandler):
        def send_html(self, content, status=200):
            data = content.encode()
            self.send_response(status); self.send_header("Content-Type","text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)

        def do_GET(self):
            u = urlparse(self.path)
            if u.path == "/": self.send_html(home()); return
            if u.path == "/capture": self.send_html(capture()); return
            if u.path == "/develop":
                q = parse_qs(u.query).get("q", [""])[0]
                self.send_html(develop(load_records(), q=q)); return
            self.send_html(page("Not found","<h1>404</h1>"),404)

        def do_POST(self):
            if self.path != "/capture": self.send_html(page("Not found","<h1>404</h1>"),404); return
            length = int(self.headers.get("Content-Length","0"))
            from urllib.parse import parse_qs
            raw = self.rfile.read(length).decode()
            form = {k:v[0] for k,v in parse_qs(raw).items()}
            records = load_records()
            t = form.get("title","").strip()
            r = Record(id=make_id(t), title=t, record_type=form.get("record_type","Research"),
                       raw_input=form.get("raw_input","").strip(), source=form.get("source","").strip(),
                       evidence_status=form.get("evidence_status","Unverified"), created_at=now(), updated_at=now())
            records.append(asdict(r)); save_records(records)
            self.send_html(develop(records, notice=f"Captured: {t}"))

    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()

if __name__ == "__main__":
    main()
