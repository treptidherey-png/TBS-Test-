# EXP-001 — Weekly Operations Exception Report

**Run:** 24 Sep 2026 · **Status:** Run once. It becomes a repeatable workflow only after Trepti validates the accuracy.

## Before the run

**What we tested:** can Claude Code rebuild TBS's operating state from the systems TBS already uses, then list only the exceptions: stalled work, missing approvals, stale records and the decisions only Trepti can make?

**Why it matters:** Trepti is the only integration layer across meetings, email, trackers and Notion. Every day she reconciles those systems in her head. If an agent can do that reconciliation reliably, the daily stand-up becomes a decision meeting instead of a status meeting, and it gets easier to hand operations to someone else.

**What happens during the run:**
1. Read 20 Fireflies meeting summaries (8–23 Sep).
2. Read the TBS Daily Tracker.
3. Search Gmail for approval, proposal and client threads.
4. Read the Notion Decision Library and the Top Gear Outbound Strategy page.
5. Read the next 14 days of Calendar.
6. Cross-reference all five sources and output only the exceptions, each with an evidence label.

**What it produces:** one internal report, with items ranked by commercial consequence and a closing condition for each.

**Permissions used:** read-only on Fireflies, Gmail, Drive, Notion and Calendar. Nothing was sent, edited or deleted. The report holds client detail, so it was delivered to Trepti and kept out of Git (`outputs/` is git-ignored).

## Experiment record

| Field | Result |
|---|---|
| Objective | Cross-source exception detection for operations |
| Inputs | 20 meeting summaries, the Daily Tracker, about 30 Gmail threads (previews), 2 Notion pages, 14 days of calendar |
| Tools used | Fireflies, Gmail, Google Drive, Notion, Google Calendar (all read-only) |
| Work performed | Retrieved the sources, extracted actions, checked each action's status against the other sources, detected stale records, grouped recurring patterns, ranked by commercial consequence |
| Output | `outputs/2026-09-24_Ops_Exception_Report.md`: 8 Trepti-only items, 4 stale or conflicting records, 4 recurring patterns, a 2-week watch list |
| Time saved | **Estimate, not measured.** Doing this by hand means re-reading about 20 meeting recaps plus the trackers, email and calendar, which is roughly 1.5–2.5 hours a week. Trepti should time her normal Monday reconciliation once to confirm. |
| Quality improvement | **Demonstrated:** it caught a stale Notion record (Top Gear approval) and measured an approval cycle of about 27 days. Neither was written down anywhere. **Likely:** fewer prospect follow-ups dropped. |
| Limitations | No visibility into WhatsApp or LinkedIn. Gmail search returns previews, not full threads. The Top Gear tracker's contents were not read. The summaries are Fireflies' own, and some are in Hindi or Marathi, so detail may be lost. |
| Risks | False "open" items for anything resolved off-system, which is why those are labelled U. Client data could leak into Git, which the ignore rule prevents. |
| Automate next | A weekly Routine, Monday 07:30 IST, that produces this report as a draft in a Notion "Ops Reports" page. It needs Trepti's approval for the write location. |
| Repeat? | **Yes, if** Trepti confirms at least 80% of items are accurate and useful, and fewer than 2 items are noise. |

## After the run

**What worked**
- Every source Claude needed was already connected. No setup was required.
- Cross-referencing found things that no single source shows:
  - The Notion page still says "pending approval" after the approval arrived.
  - Approval latency, measured end to end.
  - Hold items that were never closed.
- Multilingual meeting summaries (Hindi, Marathi) were usable.
- The Decision Library gave judgement standards to apply, for example "stale record is more dangerous" and "closing conditions, not statuses", so Claude did not invent new rules.

**What did not work**
- Prospect threads that continue on WhatsApp can't be closed. Three of the eight top items are U for this reason alone.
- Gmail previews show only the oldest messages in a thread. The report avoids claiming there was "no reply" and only says "no reply found".
- Fireflies summaries are lossy. A full-transcript pass would be more accurate and costs more.

**What needed a human**
- Nothing during the run. After the run, Trepti needs to confirm the U items and decide on items 1–8.

**What should be automated**
- The weekly run.
- Stale-record detection between trackers and Notion.
- Approval-age tracking: days since each client approval was requested.

**What should stay human**
- Ranking what matters commercially (the report proposes a ranking; Trepti decides).
- Every follow-up that is sent.
- Every change to a Notion record.
- Deciding which Notion OS is current.

**What to add to the TBS Operating System**
1. `CLAUDE.md`, the operating rules for every session. **Added.**
2. The workflow spec at `workflows/ops-exception-report.md` (v0.1). **Added**, pending validation.
3. A proposal for the Decision Library: *"Client approvals carry a requested date and a chase date."* This is drafted in the report as pattern C1. It is not written to Notion until Trepti approves it.

**Estimated business leverage**
- **Demonstrated:** operating state rebuilt across 5 systems in one run, with 12 actionable exceptions and evidence for each.
- **Likely:** 1.5–2.5 hours a week of Trepti's reconciliation time saved. The report can be handed to a team member as the daily stand-up agenda. Fewer prospect threads go cold.
- **Untested assumption:** that the team will act on the report without Trepti relaying it. Test this by sharing section B with Archana directly next week.
