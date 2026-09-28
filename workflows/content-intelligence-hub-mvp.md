# TBS Content Intelligence Hub — MVP Architecture Proposal

**Status:** Proposed, architecture-first
**Date:** 28 Sep 2026

## 1. Business objective

Reduce the amount of TBS content intelligence that Trepti has to hold in her head.

The system must make this possible:

> "I want to post about X."

The system should first retrieve what TBS already knows, identify gaps, research only those gaps, and recommend one content direction. It must stop at the Trepti approval gate before drafting.

A second core use case is calendar planning:

> "We need content for this week. What do we already have that we can use?"

The system must inventory existing TBS content before recommending new content.

## 2. What we are NOT building

- Not a replacement for Notion.
- Not a social media scheduler.
- Not a CRM.
- Not a large content-management suite.
- Not an autonomous publishing agent.
- Not a second copy of all TBS business knowledge.

## 3. Source-of-truth architecture

Notion remains the source of truth for business knowledge, decisions, SOPs, client records and existing content.

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

## 8. Existing-content inventory and calendar reuse

When planning a new content calendar, the system must first inspect existing TBS content available in Notion, including:
- completed but unpublished content
- approved but unscheduled content
- drafts
- article drafts and completed articles
- topic-bank entries with sufficient development
- previously created content that may be repurposed
- scheduled content that should be checked for overlap
- published content that creates repetition risk

The system should classify each relevant item for calendar planning as:

**Ready to use** — can be scheduled with no substantive work

**Needs light refinement** — already valuable but needs editing, updating or formatting

**Needs approval** — developed enough to consider, but Trepti has not approved it for use

**Repurpose candidate** — existing material can support a new format or angle without pretending it is new thinking

**Hold** — useful, but not appropriate for the current calendar

**Do not use** — outdated, duplicated, strategically misaligned or otherwise unsuitable

For the current week's calendar, the system should:
1. Identify the actual publishing capacity/time available.
2. Inventory relevant existing content first.
3. Recommend the strongest usable existing pieces for the available slots.
4. Identify gaps only after existing content has been evaluated.
5. Recommend new content only for genuine gaps.
6. Show why each existing piece is being recommended.
7. Never schedule or publish automatically.

The planning principle is:

> **Use what TBS has already created before asking TBS to create more.**

This is a planning rule, not a command to force unsuitable old content into the calendar. Strategic fit and quality remain the filters.

## 9. Approval state

The system must enforce:

Captured → Developed → Recommended → Awaiting Trepti Approval → Approved / Rejected / Redirected

Drafting is unavailable until Approved.

The approval gate is a business control, not merely a UI label.

Calendar recommendations are also recommendations, not automatic scheduling actions. Trepti approves the calendar direction before scheduling or new production.

## 10. Technical shape

Use a lightweight full-stack web application.

Recommended separation:
- UI layer: simple three-action workspace
- application layer: capture/develop/pipeline workflows
- data layer: structured intelligence records
- retrieval layer: keyword + semantic search over the intelligence store
- audit layer: status/history and source traceability

Keep the storage implementation replaceable so the MVP can start lightweight and scale later.

Do not introduce external infrastructure unless the MVP demonstrates that it is needed.

## 11. First build

Build only enough to prove:

Capture → Search → Develop → Approval

The first acceptance test is a real TBS topic.

Example:

> "I want to post about why more content is not necessarily the answer for a B2B founder."

The system should find existing TBS thinking and evidence before suggesting new research.

A second acceptance test is a real weekly calendar request:

> "Find everything already created but not yet used, determine what can fill this week's available slots, and identify only the remaining gaps."

The system should use existing Notion content as the first planning pool and must not invent new content simply to fill the calendar.

## 12. Business value

If this works, TBS gains:
- less repeated research
- less dependence on Trepti's memory
- faster editorial planning
- better reuse of client/buyer observations
- stronger evidence continuity
- visible repetition risks
- cleaner separation between intelligence and content
- a growing institutional memory for TBS
- better utilization of content already created
- less unnecessary content production

The goal is not more content.

The goal is **better decisions about what deserves to become content and better use of what TBS has already created.**

## 13. Build discipline

Before adding features, test the MVP against real TBS workflows.

Every feature must answer:

> Does this reduce Trepti's cognitive load or improve the quality of the content decision?

If not, do not add it.
