from datetime import date, timedelta
import re


def tokenize(text):
    return [t for t in re.findall(r"[a-z0-9]+", (text or '').lower()) if len(t) > 2]


def infer_question(request):
    text = (request or '').strip().rstrip('?')
    lower = text.lower()
    if 'article' in lower or 'post' in lower:
        topic = re.sub(r'\b(we need|i want|let us|let’s|an|a|the|article|post|for tomorrow|for today)\b', ' ', text, flags=re.I)
        topic = re.sub(r'\s+', ' ', topic).strip(' .')
    else:
        topic = text
    if not topic:
        return 'What question should the next piece answer?'
    return f'What does the audience need to understand about {topic}?'


def infer_intent(question, records):
    q = question.lower()
    if any(x in q for x in ['how', 'use', 'should', 'what is', 'why']):
        return 'Informational / educational'
    if any(x in q for x in ['buy', 'service', 'agency', 'hire', 'solution']):
        return 'Commercial investigation'
    return 'Informational / exploratory'


def candidate_records(records, request):
    terms = set(tokenize(request))
    scored = []
    for r in records:
        if r.get('scheduled_date') or r.get('lifecycle_status') in {'Published', 'Scheduled'}:
            continue
        hay = ' '.join(str(r.get(k, '')) for k in ['title', 'raw_input', 'observation', 'interpretation', 'audience_relevance']).lower()
        score = sum(1 for term in terms if term in hay)
        if score:
            scored.append((score, r))
    return [r for _, r in sorted(scored, key=lambda x: (-x[0], x[1].get('title', '')))]


def calendar_context(records, target_date=None):
    target = target_date or (date.today() + timedelta(days=1)).isoformat()
    same_day = [r for r in records if r.get('scheduled_date') == target]
    recent = sorted([r for r in records if r.get('scheduled_date') and r.get('scheduled_date') < target], key=lambda r: r.get('scheduled_date'), reverse=True)[:10]
    return target, same_day, recent


def build_recommendation(records, request, target_date=None):
    target, same_day, recent = calendar_context(records, target_date)
    candidates = candidate_records(records, request)
    question = infer_question(request)
    intent = infer_intent(question, candidates)

    if candidates:
        primary = candidates[0]
        reuse = 'Reuse/refine existing asset'
        gap = 'Validate whether the existing question and angle match current audience/search demand.'
        direction = primary.get('title', 'Existing TBS asset')
    else:
        primary = None
        reuse = 'Net-new creation only if research confirms a genuine gap'
        gap = 'No sufficiently relevant available TBS asset was found in the local inventory.'
        direction = 'Research the audience question before creating a new asset.'

    return {
        'target_date': target,
        'calendar_slot': same_day[0].get('scheduled_slot', '') if same_day else 'No explicit slot found in local calendar',
        'calendar_conflict': bool(same_day),
        'recent_publishing': [{'title': r.get('title', ''), 'date': r.get('scheduled_date', '')} for r in recent],
        'question': question,
        'search_intent': intent,
        'candidate_count': len(candidates),
        'candidate': primary,
        'reuse_decision': reuse,
        'gap': gap,
        'recommended_direction': direction,
        'demand_validation': 'Required before approval: validate current search questions/results around the diagnosed question.',
        'status': 'Awaiting Trepti Approval',
    }
