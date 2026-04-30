# Spec-Kit: Spec-Driven Development (SDD) Framework

## Core Mandates
1.  **SDD Lifecycle**: Strictly follow the **Specification -> Implementation Plan -> Implementation** lifecycle.
2.  **Hybrid SDD Protocol (Thinking vs. Multi-Agent Executing)**:
    - **Claude (The Architect)**: Handle `/speckit-specify` and `/speckit-plan`. Use your reasoning to break down tasks into parallel-ready chunks (marked `[P]` in `tasks.md`).
    - **Gemini CLI (The Orchestrator)**: Fire up specialized agents to execute the tasks.
    - **Multi-Agent Command**: For complex implementations, delegate to Gemini using: 
      `gemini -p "Orchestrate your subagent team (@coder, @tester, @refactor) to execute the tasks in tasks.md. Parallelize all tasks marked [P]." --yolo`
    - **Token Saving**: This saves Claude's tokens by offloading the entire implementation loop (including sub-agent spawns) to Gemini's orchestration layer.
    - **Final Revision**: Once Gemini's team finishes, Claude performs the final surgical review with `/speckit-git-validate`.

## Build and Test Commands
- Build: `uv build`
- Test: `uv run pytest`
- Test (with coverage): `uv run pytest --cov=src`

<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan:
`specs/001-num-core-completion/plan.md`
<!-- SPECKIT END -->
