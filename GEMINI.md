# Spec-Kit: Spec-Driven Development (SDD) Framework

## Core Mandates
1.  **SDD Lifecycle**: Strictly follow the **Specification -> Implementation Plan -> Implementation** lifecycle.
2.  **Multi-Agent Execution (The Builder)**: When running `/speckit.implement`, you are the **Lead Orchestrator**. 
    - **Delegation**: Use your subagent team to complete tasks efficiently. 
    - **Parallelism**: For tasks marked `[P]` in `tasks.md`, you **MUST** spawn parallel subagents using `@coder`, `@tester`, or `@refactor`.
    - **Autonomy**: Use `--yolo` mode for your subagents to ensure they can write code and run tests without halting the main orchestration.

<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan
<!-- SPECKIT END -->
