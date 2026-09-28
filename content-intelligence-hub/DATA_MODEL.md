# Data Model

## Intelligence Record

Required:

- `id`
- `title`
- `record_type`
- `raw_input`
- `source`
- `evidence_status`
- `lifecycle_status`
- `created_at`
- `updated_at`

Optional intelligence fields:

- `observation`
- `interpretation`
- `audience_relevance`
- `buyer_problem`
- `what_most_people_miss`
- `related_record_ids`
- `notes`

Record types:

- Buyer Insight
- Founder Observation
- Market Signal
- Research
- Competitor Reference
- Proof / Evidence
- Content Opportunity
- Published Content
- Content Learning

## Important distinctions

Do not collapse:

Source → Observation → Interpretation → Opportunity → Asset → Learning

A source is not automatically a TBS interpretation. An interpretation is not automatically a content opportunity. A published asset is not the same thing as the intelligence that produced it.

## Opportunity fields

A Content Opportunity should additionally capture:

- buyer/problem
- TBS interpretation
- what most people miss
- one primary content job
- evidence/source
- repetition check
- research gaps
- recommended format/mechanism
- approval status
