# fxn-wms Project Overview
- Purpose: Warehouse Management System for Houston P9 automated warehouse; integrates AGV/RCS/WCS to automate inbound, storage, SMT logistics, and production supply.
- Workflow: Spec-driven development via Gemini CLI `speckit` commands; features tracked by specs/branches named `NNN-short-name`.
- Tech stack: Documentation-first; Python environment present (`.venv/`). No application source code in repo yet; materials are SRS and source documents in `docs/origin`.
- Key docs: `docs/SRS.md` (需求规格说明书), original customer docs in `docs/origin/*.xlsx/.docx/.pdf`, project guidance in `GEMINI.md`.
- Structure: `.specify/` scripts & templates, `.gemini/` command definitions, `specs/` generated feature specs, `docs/` for SRS and source artifacts, `.venv/` virtualenv, minimal tests folder (empty).
- Language: User prefers Chinese with bilingual annotations where needed.