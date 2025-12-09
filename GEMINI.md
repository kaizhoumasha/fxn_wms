# fxn-wms Project Context

## Project Overview

**fxn-wms** is a Warehouse Management System (WMS) project that includes integration with Automated Guided Vehicles (AGV) and Robot Control Systems (RCS). The project is managed using a **Spec-Driven Development** workflow, facilitated by the Gemini CLI and custom `speckit` commands.

## Spec-Driven Development Workflow

This project enforces a structured lifecycle for feature development:

1. **Specify**: Define the feature in natural language. An agent creates a spec file and a corresponding git branch.

   * Command: `/speckit.specify "Feature description"`
   * Artifacts: `specs/NNN-feature-name/spec.md`, Git Branch `NNN-feature-name`
2. **Clarify** (Optional): Refine requirements and clear up ambiguities.

   * Command: `/speckit.clarify`
3. **Plan**: Create a technical implementation plan based on the spec.

   * Command: `/speckit.plan`
   * Artifacts: `specs/NNN-feature-name/plan.md`
4. **Tasks**: Break down the plan into actionable tasks.

   * Command: `/speckit.tasks`
   * Artifacts: `specs/NNN-feature-name/tasks.md`
5. **Implement**: Execute the tasks to build the feature.

   * Command: `/speckit.implement`

## Directory Structure

* **`.specify/`**: Contains the core logic for the Spec-Driven Development workflow, including bash scripts (`scripts/bash/`) and templates (`templates/`) used by the agents.
* **`.gemini/`**: Configuration for the Gemini CLI, including the definitions for `speckit` commands (`commands/*.toml`).
* **`docs/`**: Stores original project documentation, including specifications for AGVs, RCS interfaces, and functional lists.
* **`specs/`**: (Generated) Holds the specification, plan, and task files for each feature, organized by branch name (e.g., `specs/001-user-auth/`).
* **`.venv/`**: Python virtual environment, indicating Python is a primary language for this project.

## Key Files & Scripts

* **`.specify/scripts/bash/check-prerequisites.sh`**: Validates that the necessary documents (spec, plan, tasks) exist before proceeding to the next phase.
* **`.specify/scripts/bash/create-new-feature.sh`**: Automates the creation of new feature branches and spec directories.
* **`GEMINI.md`**: This file, serving as the context instruction for AI agents.

## Development Conventions

* **Feature Branches**: All work must be done on feature branches named `NNN-short-name` (e.g., `005-agv-routing`).
* **Documentation First**: Code should not be written until `spec.md`, `plan.md`, and `tasks.md` are approved/generated.
* **Python Environment**: Ensure the `.venv` is active or used for running Python scripts.

## Getting Started

To start working on a new feature:

1. Ensure you are in the project root.
2. Run `/speckit.specify "Your feature description here"`.
3. Follow the agent's guidance to refine the spec, create a plan, and generate tasks.

## Gemini Added Memories

- The user prefers to interact primarily in Chinese, with special meanings and key terminology marked with bilingual annotations.
