"""CLI entry point for the automatic article-planning decision flow."""
import argparse
import json
from pathlib import Path

from planner import build_recommendation

ROOT = Path(__file__).parent
DATA = ROOT / 'data.json'


def load_records():
    if not DATA.exists():
        return []
    return json.loads(DATA.read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser(description='TBS Content Intelligence article planner')
    parser.add_argument('request', nargs='+', help='Natural-language request, e.g. We need an article for tomorrow')
    parser.add_argument('--date', dest='target_date', help='Target date in YYYY-MM-DD format')
    args = parser.parse_args()

    request = ' '.join(args.request)
    plan = build_recommendation(load_records(), request, args.target_date)

    print('TBS CONTENT INTELLIGENCE RECOMMENDATION')
    print('=======================================')
    print(f"Target date: {plan['target_date']}")
    print(f"Calendar slot: {plan['calendar_slot']}")
    print(f"Question diagnosed: {plan['question']}")
    print(f"Search intent: {plan['search_intent']}")
    print(f"Existing candidates found: {plan['candidate_count']}")
    if plan['candidate']:
        c = plan['candidate']
        print(f"Existing asset: {c.get('title', '')}")
        print(f"Existing asset status: {c.get('lifecycle_status', '')}")
    print(f"Reuse decision: {plan['reuse_decision']}")
    print(f"Gap: {plan['gap']}")
    print(f"Recommended direction: {plan['recommended_direction']}")
    print(f"Demand validation: {plan['demand_validation']}")
    print(f"Status: {plan['status']}")


if __name__ == '__main__':
    main()
