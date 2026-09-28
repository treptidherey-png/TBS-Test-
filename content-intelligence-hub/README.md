# TBS Content Intelligence Hub MVP

A lightweight internal workspace for the TBS content-intelligence workflow.

## Purpose

Reduce the amount of content intelligence Trepti must hold in her head.

The MVP supports:

1. Capture
2. Search
3. Develop an idea
4. One-prompt planning and recommendation\n5. Stop at the Trepti approval gate

It deliberately does not publish, replace Notion, or autonomously draft approved content. Calendar state is supported, but publishing remains a human-controlled action.

## Operating principle

Search what TBS already knows before researching again.

The development view separates:

- Known
- Related
- Missing
- Needs research

## First implementation

This first slice is intentionally local-first and storage-agnostic. The data model and workflow are explicit so a persistent/semantic storage layer can be added without redesigning the user-facing flow.

## One-prompt behaviour\n\nThe intended user experience is one instruction such as:\n\n> We need an article for tomorrow.\n\nThe planner then checks available content first, excludes published/scheduled work, diagnoses the question an existing asset answers, and returns one reuse/refinement or research-gap recommendation. It stops at `Awaiting Trepti Approval`.\n\nLive search-demand evidence is an external research input to the planner. The core engine accepts that evidence without making up demand.\n\nSee `DATA_MODEL.md`, `WORKFLOW.md`, and `planner.py`.
