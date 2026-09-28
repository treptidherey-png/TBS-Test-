# TBS Content Intelligence Hub MVP

A lightweight internal workspace for the TBS content-intelligence workflow.

## Purpose

Reduce the amount of content intelligence Trepti must hold in her head.

The MVP supports:

1. Capture
2. Search
3. Develop an idea
4. Stop at the Trepti approval gate

It deliberately does not publish, schedule, replace Notion, or autonomously draft approved content.

## Operating principle

Search what TBS already knows before researching again.

The development view separates:

- Known
- Related
- Missing
- Needs research

## First implementation

This first slice is intentionally local-first and storage-agnostic. The data model and workflow are explicit so a persistent/semantic storage layer can be added without redesigning the user-facing flow.

See `DATA_MODEL.md` and `WORKFLOW.md`.
