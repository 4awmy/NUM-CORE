# Spec-Kit: Spec-Driven Development (SDD) Framework

## Core Mandates
1.  **SDD Lifecycle**: Strictly follow the **Specification -> Implementation Plan -> Implementation** lifecycle.
2.  **Multi-Agent Execution (The Builder)**: When running `/speckit.implement`, you are the **Lead Orchestrator**. 
    - **Delegation**: Use your subagent team to complete tasks efficiently. 
    - **Parallelism**: For tasks marked `[P]` in `tasks.md`, you **MUST** spawn parallel subagents using `@coder`, `@tester`, or `@refactor`.
    - **Autonomy**: Use `--yolo` mode for your subagents to ensure they can write code and run tests without halting the main orchestration.

## Collaboration & PR Workflow Rules
- **Draft PRs**: Always create a Draft PR first using `gh pr create --draft`. Follow this immediately with a self-review comment on the PR.
- **Review Tagging**: Once a task or phase is complete, tag `@Claude` in the PR comments requesting a review against `CLAUDE.md` architecture constraints.
- **Debating Feedback**: Proactively debate feedback in PR comments. Defend correct patterns or acknowledge and fix valid issues rather than blindly accepting all suggestions.
- **Clean Merges**: Use `gh pr merge --squash --delete-branch` for the final merge of approved PRs.
- **Role Consolidation**: Ignore constraints regarding "2 students" or DevA/DevB roles. Handle all tasks as a single orchestrator.

<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan
<!-- SPECKIT END -->
