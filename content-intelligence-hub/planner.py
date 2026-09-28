from datetime import date, timedelta
import re


AVAILABLE = {"Captured", "Developed", "Recommended", "Awaiting Trepti Approval", "Approved"}


def tokenize(text):
    return {t for t in re.findall(r"[a-z0-9]+", (text or "").lower()) if len(t) > 2}


def infer_question(request):
    text = (request or "").strip().rstrip("?")
    lower = text.lower()
    if "article" in lower or "post" in lower:
        topic = re.sub(
            r"\b(we need|i want|let us|let’s|an|a|the|article|post|for tomorrow|for today)\b",
            " ",
            text,
            flags=re.I,
        )
        topic = re.sub(r"\s+", " ", topic).strip(" .")
    else:
        topic = text
    if not topic:
        return "What question should the next piece answer?"
    return f"What does the audience need to understand about {topic}?"


def infer_intent(question, records=None):
    q = question.lower()
    if any(x in q for x in ["how", "use", "should", "what is", "why"]):
        return "Informational / educational"
    if any(x in q for x in ["buy", "service", "agency", "hire", "solution"]):
        return "Commercial investigation"
    return "Informational / exploratory"


def candidate_records(records, request):
    terms = tokenize(request)
    scored = []
    for r in records:
        if r.get("scheduled_date") or r.get("lifecycle_status") in {"Published", "Scheduled"}:
            continue
        if r.get("lifecycle_status", "Captured") not in AVAILABLE:
            continue
        hay = " ".join(
            str(r.get(k, ""))
            for k in [
                "title",
                "raw_input",
                "observation",
                "interpretation",
                "audience_relevance",
                "buyer_problem",
                "what_most_people_miss",
            ]
        ).lower()
        score = sum(1 for term in terms if term in hay)
        if score:
            scored.append((score, r))
    return [r for _, r in sorted(scored, key=lambda x: (-x[0], x[1].get("title", "")))]


def diagnose_asset(record):
    if not record:
        return None
    title = (record.get("title") or "").strip()
    raw = (record.get("raw_input") or "").strip()
    first_sentence = re.split(r"[.!?]", raw)[0].strip()
    return {
        "title": title,
        "question_it_currently_answers": (
            f"What does the reader need to understand about {title}?"
            if title
            else f"What does the reader need to understand about {first_sentence}?"
        ),
        "status": record.get("lifecycle_status", "Captured"),
        "evidence_status": record.get("evidence_status", "Unverified"),
        "source": record.get("source", ""),
    }


def calendar_context(records, target_date=None):
    target = target_date or (date.today() + timedelta(days=1)).isoformat()
    same_day = [r for r in records if r.get("scheduled_date") == target]
    recent = sorted(
        [r for r in records if r.get("scheduled_date") and r.get("scheduled_date") < target],
        key=lambda r: r.get("scheduled_date"),
        reverse=True,
    )[:10]
    return target, same_day, recent


def build_recommendation(records, request, target_date=None, demand_evidence=None):
    target, same_day, recent = calendar_context(records, target_date)
    candidates = candidate_records(records, request)
    question = infer_question(request)
    intent = infer_intent(question, candidates)
    demand_evidence = demand_evidence or []

    if candidates:
        primary = candidates[0]
        reuse = "Reuse/refine existing asset"
        gap = (
            "Validate whether the existing question, angle and title match current "
            "audience/search demand before drafting."
        )
        direction = primary.get("title", "Existing TBS asset")
        decision = "reuse_or_refine"
    else:
        primary = None
        reuse = "Net-new creation only if research confirms a genuine gap"
        gap = "No sufficiently relevant available TBS asset was found in the local inventory."
        direction = "Research the audience question before creating a new asset."
        decision = "research_gap"

    return {
        "target_date": target,
        "calendar_slot": (
            same_day[0].get("scheduled_slot", "")
            if same_day
            else "No explicit slot found in local calendar"
        ),
        "calendar_conflict": bool(same_day),
        "recent_publishing": [
            {"title": r.get("title", ""), "date": r.get("scheduled_date", "")}
            for r in recent
        ],
        "question": question,
        "search_intent": intent,
        "candidate_count": len(candidates),
        "candidate": diagnose_asset(primary),
        "reuse_decision": reuse,
        "gap": gap,
        "demand_evidence": demand_evidence[:8],
        "recommended_direction": direction,
        "recommendation_basis": [
            "Check existing TBS work before net-new creation.",
            "Diagnose the question the existing asset actually answers.",
            "Validate search intent/demand where the article job requires it.",
            "Change title/angle/structure before discarding useful existing work.",
        ],
        "status": "Awaiting Trepti Approval",
        "drafting_allowed": False,
        "publishing_allowed": False,
        "decision": decision,
    }
