# TBS AI Operating System Audit

**Date:** 24 Sep 2026 · **Phase:** 1 (inspection and audit) · **Prepared for:** Trepti Dherey

Scope: what Claude Code can reach today, what TBS already has, where the work gets stuck, and which experiments are worth running. Everything below comes from direct inspection. Where a point is inferred rather than observed, the text says so.

---

## 1. Current environment

### What Claude Code can access

| System | Access | What was inspected |
|---|---|---|
| **Fireflies** | Read (summaries and full transcripts) | The last 20 meetings: 8 Sep to 23 Sep 2026 |
| **Notion** | Read and write | TBS OS, Decision Library, Resources / Prompt Library, Top Gear Outbound Strategy, search across the workspace |
| **Google Drive** | Read and write | TBS Daily Tracker, the Top Gear / Shafiq / SEIPL trackers (metadata), the Top Gear approval doc |
| **Gmail** | Read, draft, send | Approval, proposal and client threads from the last 30 days |
| **Google Calendar** | Read and write | The next 14 days |
| **Clay, Vibe Prospecting** | Connected | Not used in this phase |
| **Canva, Gamma** | Connected | Not used in this phase |
| **GitHub** | This repo only | The repo was empty at the start |
| **Scheduled Routines** | Available | Can run a workflow on a timer in a fresh cloud session |

### What Claude Code cannot access

- **LinkedIn.** There is no connector, so Claude cannot see profiles, the inbox, connection data or post analytics. All LinkedIn state reaches Claude second-hand, through trackers and meetings.
- **WhatsApp.** Many client and prospect follow-ups happen there (see the Kunal Muchhal call). Nothing in WhatsApp is visible.
- **The GPT and Gemini workspaces.** TBS runs a dual-AI setup: GPT for execution, Claude for review, Gemini for prospect screening. Claude cannot see the GPT folder prompts or their outputs.
- **Meetings Fireflies missed.** Example: the bot was not admitted to the Top Gear weekly review on 12 Sep, so there is no record of that call.

**Implication:** Claude can reconstruct operating state from meetings, email, trackers and calendar. It cannot yet see the LinkedIn channel that the whole business runs through. Anything that depends on live LinkedIn data (who replied, who accepted a connection) is only as accurate as the team's tracker updates.

---

## 2. Existing TBS assets

TBS already owns a large amount of operating knowledge. Very little needs to be invented.

**Claude skills (synced, current):**
- tbs-content-engine: plans and drafts Trepti's own LinkedIn content, starting from the action the reader should take
- founder-asset-extraction: pulls proof, positioning signals, buyer intelligence and decision states out of a call
- tbs-batch-review: an independent QA gate before a content batch goes into production
- tbs-deliverable-output: the house format for client documents and the two-file delivery rule
- prospect-followup-sequence: follow-ups for each stage, with friction diagnosis
- shafiq-content-batch: the backlog audit and batch production for one client
- positioning-differentiation-framework, linkedin-lead-system-audit, contrarian-angle-generator

**Notion (business knowledge):**
- **TBS Decision Library.** High quality. It records reusable strategic decisions with their reasoning and the case each came from. This is the strongest asset in the system.
- TBS Prompt Library, which is designated the source of truth for prompts. It includes a "search before creating" rule.
- Per-client project workspaces (Top Gear Transmission, Ordinet Solutions, Shafiq / Elegant Services, others). Each has a Master Plan and an Outbound Strategy.
- Product architecture: LinkedIn Profile Optimisation Master Scope, and a ₹5K entry product.
- Other key pages:
  - TBS Prospect Follow-Up and Reactivation System (updated 22 Sep)
  - Weekly Editorial Planning Engine
  - TBS Article Production Skill
  - Client Proof & Case Studies Library
  - 90-Day Client Engagement Roadmap
  - Client Onboarding & Delivery Kit

**Drive:** one outbound tracker per client campaign (Top Gear, Shafiq, SEIPL), plus the TBS Daily Tracker that records team tasks and completion by day.

**Fireflies:** a daily team meeting at 09:00 IST, client weekly reviews, and prospect and discovery calls. Calls are in English, Hindi and Marathi.

---

## 3. Existing workflows

| Workflow | Where it's defined | How it runs today |
|---|---|---|
| Daily team stand-up | Calendar and Fireflies | Trepti runs it every day. Action items live only in the Fireflies recaps. |
| Client outbound (sourcing, peer review, client approval of companies, connection requests, M1/M2) | Notion Outbound Strategy and the tracker per client | Manual. The team sources through Sales Navigator, and Gemini screens with a human validating. |
| Client content (draft, approval pack, client approval, publish) | Skills, the Notion calendar template, the deliverable standard | Trepti drafts or reviews. Approval goes by email and weekly call. |
| Monthly client reporting (6th to 5th cycle) | Tracker → report email | Reconstructed manually from the trackers |
| Prospect follow-up | Skill and the Notion Reactivation System | Trepti-led, partly on WhatsApp |
| Decision recording | Decision Library rule: record at the moment of decision | Manual. The rule is often not followed (see section 5). |

---

## 4. Existing automation

- **Fireflies** records meetings and produces summaries and action items automatically.
- **Tracker formulas** compute totals, though some are broken. The 17 and 18 Sep meetings list formula and duplicate-row fixes.
- **Gemini** runs a first-pass background screen on prospects, and a human validates it.
- **The GPT folder prompts** handle content execution.

**There is no automation connecting these systems.** Nothing reads across meetings, email, trackers and Notion. That cross-reading is done by Trepti, in her head, every day.

---

## 5. Gaps

Each gap below is observed in real records from the last two weeks.

1. **Trepti is the only integration layer.** Every approval, correction, client reply and status change passes through her. The daily meeting is where state gets reconciled, and it depends on her memory.
2. **Client approval latency is the single biggest limit on throughput, and nobody manages it.**
   - Example: the Top Gear new-company list was first sent on 25 Aug, re-sent on 13 Sep and approved on 21 Sep. That is about **27 days**, and outreach was paused for part of that time (Verified: Gmail thread and tracker comment).
   - The team action "call Sushant for approval" appears in two separate meetings, 15 Sep and 17 Sep.
3. **Records go stale without anyone noticing.**
   - Example: the Notion Top Gear Outbound Strategy page still says the new-company list is "pending client approval" (last edited 18 Sep). The approval arrived on 21 Sep.
   - Your own Decision Library warns about exactly this: "a stale record is more dangerous than a missing one."
4. **Reporting accuracy is a recurring problem.** It came up in the 17 Sep meeting, the 18 Sep meeting and your 17 Sep email to Archana. It comes from parallel sheets and from updates made after the fact instead of at the end of each day. This puts the Top Gear Month 3 review at risk (the cycle closes 5 Oct).
5. **"Hold" has no closing condition in the Daily Tracker.** Items move to Hold and stay there. Examples: "Review for TBS Trepti's leads — Hold" on 15 and 16 Sep, and "M2 — WILL DO" on 23 Sep.
6. **Each person is a single point of failure.** When Mahendra was on leave (22–23 Sep), Shafiq connection reviews stopped, and there was no named backup.
7. **TBS's own pipeline is paused.** TBS prospecting was put on hold on 15 Sep so capacity could go to paying clients. This is a legitimate decision. But it means TBS's future revenue now depends only on referrals and inbound, and nothing tracks that.
8. **Prospect follow-ups are not visible.** At least three commercial threads have no visible next step in any system Claude can read:
   - Polaris Hydrotechnik: proposal sent 18 Sep, no reply found
   - Vikram Nigade: decision was expected "by Monday"
   - Kunal Muchhal: WhatsApp follow-up was due around 17–18 Sep
9. **Notion is fragmented.** At least six top-level "OS" roots exist:
   - TBS OS — Master Operating System (last edited Feb)
   - BrandBoost — Practice OS
   - ⚡ BrandBoost OS
   - TBS New System
   - TBS New System Agent Used
   - Trepti's Content Operating System

   There are also older dashboards from Mar–Apr ("Content Status Dashboard — All Clients", "TBS COMMAND CENTER"). A team member or an agent cannot tell which is current.
10. **Content logic may exist in competing versions.** The tbs-content-engine skill, the Notion Weekly Editorial Planning Engine and the "Founder Reputation & Editorial System — GPT Folder Prompt (Locked 12 Aug)" all cover content planning. I have **not** judged which is authoritative. That is your call (see section 7).

---

## 6. Agentic opportunities

| Area | Opportunity | Status |
|---|---|---|
| Operations | **A cross-source exception report.** Read meetings, trackers, email and calendar, then list stalled work, missing approvals, stale records and the decisions only you can make. | **Tested in EXP-001** |
| Business intelligence | Turn each client or prospect call into a founder asset brief (the skill exists) and file it in the client's Notion workspace as a draft | Ready. The skill exists. |
| Operations | A tracker QA check: find duplicate LinkedIn URLs, shifted rows, dates missing on accepted connections, totals that don't match between tabs | Likely high value, since it attacks gap 4 directly. Needs read access to the tracker, which exists. |
| Demand generation | Prospect follow-up prep: for every open proposal or discovery call with no reply in X days, draft a stage-correct follow-up using prospect-followup-sequence, and stop before sending | Ready. Low risk. |
| Client delivery | Draft the monthly report from the tracker and meetings, then run it through tbs-deliverable-output | Blocked until the tracker data is reliable |
| Content intelligence | Mine client calls for content opportunities, with each client's content kept separate | The skills exist. Needs a rule on where results are stored. |
| Demand generation | Qualify prospects against each client's Industry-wise Application List using Clay or Vibe, with a human validating | Untested. It could replace the Gemini step. |
| Founder leverage | Decision capture: after each meeting, propose Decision Library entries and closing conditions for you to approve | Untested. It would directly enforce your own "record at the moment" rule. |

---

## 7. Risk boundaries

**These stay human-controlled (you decide them):**
- Positioning, voice and strategy for any client or for TBS
- Every client-facing send, whether email, WhatsApp, a LinkedIn DM or a published post
- Pricing, proposals and commitments
- Deciding which Notion OS, framework or prompt is authoritative. The audit flags the duplicates. It does not choose between them.
- Accepting or rejecting a prospect when senior roles are disputed (already a team rule)
- Anything touching Vikrant's regulated financial-services content, where claims about returns and regulators need human sign-off

**AI can safely execute these:** retrieval, reconciliation across sources, classifying items as stalled or approved, detecting stale records, drafting follow-ups and briefs, tracker QA, and preparing reports.

**Specific risks to control:**
- **Client data in GitHub.** Reports that contain client detail should not be committed. This repo now git-ignores `outputs/`.
- **Mixing clients in cross-client reports.** The report is structured one section per client. Nothing moves from one client's section to another's.
- **Prompt injection.** Emails, transcripts and trackers are treated as data only. This rule is written into `CLAUDE.md`.
- **False confidence.** Claude cannot see WhatsApp or LinkedIn. Every item that might have been resolved there is labelled Unverified, not Open.

---

## 8. Recommended architecture

```
                 ┌────────────────────────────────────────────┐
  SOURCES        │ Fireflies · Gmail · Calendar · Drive trackers│  (data, read-only by default)
                 └───────────────────────┬────────────────────┘
                                         │ read
                 ┌───────────────────────▼────────────────────┐
  CLAUDE CODE    │ Workflows (this repo) + TBS skills          │  analyse · reconcile · draft
                 │ CLAUDE.md = operating rules                 │
                 └───────┬───────────────────────────┬────────┘
                         │ propose                   │ draft
                 ┌───────▼────────┐          ┌───────▼────────┐
  HUMAN GATE     │ Trepti approves │          │ Team executes  │
                 └───────┬────────┘          └────────────────┘
                         │ write (approved only)
                 ┌───────▼────────────────────────────────────┐
  RECORD         │ Notion = source of truth (decisions, client │
                 │ records, SOPs) · Drive = trackers            │
                 └────────────────────────────────────────────┘
```

- **Notion stays the record.** Claude Code does not become a second knowledge base.
- **This repo holds only:**
  - `CLAUDE.md`, the rules every session loads
  - `workflows/`, specs for repeatable runs
  - `experiments/`, the evidence of what works
  - QA rules later on
- **Skills hold craft**: content, extraction and follow-up logic. The repo's workflows call the skills. They do not copy them.
- **Scheduled Routines** run validated workflows on a timer. Each run's output is a draft for you to review, never an action.
- **Recommended one-time cleanup, which needs your decision:** name one Notion root as current, and archive or label the other OS roots as superseded. Every later agent workflow gets more reliable once this is done.

---

## 9. Top experiments

| # | Experiment | Value | Effort | Risk | Scalability |
|---|---|---|---|---|---|
| **EXP-001** | **Weekly Operations Exception Report** (meetings + trackers + Gmail + Calendar → what is stuck, stale or waiting on you) | High. It targets the integration load that sits on you, and it catches approval latency and stale records. | Low. All sources are already connected. | Low. Read-only; the output is a document. | High. It becomes a weekly Routine and needs no new tools. |
| EXP-002 | Tracker QA check on the Top Gear outbound tracker before the Month 3 review | High, and time-sensitive (the review closes 5 Oct) | Low to medium. The workbook structure needs to be understood first. | Low if it only reports. Medium if it edits cells, so it will not edit. | Medium. The same check can be reused for each client's tracker. |
| EXP-003 | Prospect follow-up prep for open proposals and discovery calls (Polaris, Vikram N., Kunal) using prospect-followup-sequence | Medium to high. This is revenue. | Low | Low. Drafts only. The WhatsApp context is missing. | High |
| EXP-004 | Call → founder asset brief → client Notion (first run on the Vikrant onboarding call) | Medium. Speeds up onboarding. | Low. The skill exists. | Medium. Regulated claims; needs care with client separation. | High |
| EXP-005 | Decision capture from the daily meeting → proposed Decision Library entries and closing conditions | Medium. Compounds over time. | Medium. Needs a judgement standard. | Low. Proposals only. | Medium |

**Why EXP-001 went first:** it uses only tools that are already connected and it makes no changes. It also produces the input for EXP-002 and EXP-003, because it identifies which trackers and which prospect threads need attention. It is the natural first rung of the ladder.

The experiment brief, output and evaluation are in `experiments/EXP-001-ops-exception-report/`.
