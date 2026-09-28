# TBS Content Intelligence Hub — MVP Architecture Proposal

**Status:** Proposed, architecture-first
**Date:** 28 Sep 2026

## 1. Business objective

Reduce the amount of TBS content intelligence that Trepti has to hold in her head.

The system must make this possible:

> "I want to post about X."

The system should first retrieve what TBS already knows, identify gaps, research only those gaps, and recommend one content direction. It must stop at the Trepti approval gate before drafting.

## 2. What we are NOT building

- Not a replacement for Notion.
- Not a social media scheduler.
- Not a CRM.
- Not a large content-management suite.
- Not an autonomous publishing agent.
- Not a second copy of all TBS business knowledge.

## 3. Source-of-truth architecture

Notion remains the source of truth for business knowledge, decisions, SOPs and client records.

GitHub becomes the source of truth for the executable content-intelligence workflow:
- data model
- application logic
- search/retrieval logic
- workflow states
- QA rules
- experiments
- version history

This preserves the existing repository rule and avoids creating a second business knowledge base.

## 4. User experience

The home screen should expose three actions only:

### CAPTURE
One input box.

Trepti can paste or type anything worth retaining. Classification can happen after capture.

### DEVELOP AN IDEA
One input:

> What do you want to explore?

The system then shows:
1. Existing TBS knowledge
2. Related evidence
3. Previous content
4. Similar/repeated ideas
5. Missing information
6. Research needed
7. One recommended direction

### CONTENT PIPELINE
Shows only ideas that have passed the approval gate and are being prepared, published or learned from.

## 5. Minimal internal model

Every intelligence record has a stable ID and these core fields:
- title
- record_type
- raw_input
- source
- observation
- interpretation
- audience/buyer relevance
- evidence status
- related records
- lifecycle status
- created_at
- updated_at

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

Do not force every field to be completed for every record.

## 6. Content Opportunity model

An opportunity becomes more structured only when it enters the Develop flow:
- buyer/problem
- key observation
- TBS interpretation
- what most people miss
- primary content job
- evidence/source basis
- repetition check
- research gaps
- recommended format/mechanism
- approval status

## 7. Retrieval priority

When developing an idea:
1. Existing approved TBS thinking
2. Existing real-world evidence
3. Existing market intelligence
4. Existing competitor mechanisms
5. New research only for unresolved gaps

The application should explicitly distinguish:

**Known**
**Related**
**Missing**
**Needs research**

This is the mechanism that prevents duplicate research.

## 8. Approval state

The system must enforce:

Captured → Developed → Recommended → Awaiting Trepti Approval → Approved / Rejected / Redirected

Drafting is unavailable until Approved.

The approval gate is a business control, not merely a UI label.

## 9. Technical shape

Use a lightweight full-stack web application.

Recommended separation:
- UI layer: simple three-action workspace
- application layer: capture/develop/pipeline workflows
- data layer: structured intelligence records
- retrieval layer: keyword + semantic search over the intelligence store
- audit layer: status/history and source traceability

Keep the storage implementation replaceable so the MVP can start lightweight and scale later.

Do not introduce external infrastructure unless the MVP demonstrates that it is needed.

## 10. First build

Build only enough to prove:

Capture → Search → Develop → Approval

The first acceptance test is a real TBS topic.

Example:

> "I want to post about why more content is not necessarily the answer for a B2B founder."

The system should find existing TBS thinking and evidence before suggesting new research.

## 11. Business value

If this works, TBS gains:
- less repeated research
- less dependence on Trepti's memory
- faster editorial planning
- better reuse of client/buyer observations
- stronger evidence continuity
- visible repetition risks
- cleaner separation between intelligence and content
- a growing institutional memory for TBS

The goal is not more content.

The goal is **better decisions about what deserves to become content.**

## 12. Build discipline

Before adding features, test the MVP against real TBS workflows.

Every feature must answer:

> Does this reduce Trepti's cognitive load or improve the quality of the content decision?

If not, do not add it.
