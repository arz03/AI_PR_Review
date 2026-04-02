---
name: code-review
description: "Use when: a user asks to review code quality or review changes (e.g., 'review my code', 'check my code quality', 'review these changes'). Performs a structured, iterative code review, highlights critical gaps, and can hand off to a PR Draft skill after the review."
---

# Code Review Skill (v2)

This skill runs a structured, iterative code review that captures user context, highlights critical gaps, and optionally drafts a PR summary to speed up review.

## Workflow

0. **Execution Todo List (required)**
    - At the start of the skill, create a detailed todo list covering each step below using `TodoWrite` (todo tools).
    - The list must be broken down by step (preflight context, repo context, scope, review loop, static checks, reporting/logging, follow-up, PR draft).
    - Update the list after each step; do not finish the review until all items are completed.

1. **Preflight Context (required)**
    - Capture user intent and constraints using `AskUserQuestion` (ask question tool):
       - Review goal and critical areas
       - Preferred scope (files, commit, branch) and deadlines
       - Risk tolerance (what is considered critical)
       - Permission to run tests/builds
    - If the user already provided this, confirm and proceed.
    - Include possible answers in question based on available context

2. **Repo Context (create or refresh)**
    - Goal: produce or update [docs/repo_context.md](docs/repo_context.md) for this repository.
    - If the file exists, read it first and use it to configure the remaining steps. If it does not exist, create it on this run.
    - Use subagents in parallel to gather:
       - **Tech stack**: frameworks, languages, runtime, API/database layer, external dependencies.
       - **Code quality config**: linting, formatting, type checks, pre-commit hooks, CI checks.
       - **Test suites**: unit, integration, e2e, other test harnesses and entry points.
       - **Repo tree**: a README-like file tree with 1-line high-value comments per entry.
    - For the tree, include top-level directories and **key files**; if the repo is large, skip docs, config folders, and deep component trees, but include a concise note about what was skipped.
    - Format for repo_context.md:
       - First: a 2-line description of the repo.
       - Then sections: Tech Stack, Code Quality and Checks, Test Suites, Repo Tree.
       - Each file or directory entry must have a single, informative comment on its purpose.

3. **Scope the Review**
    - If the user specifies a scope, use it as the primary filter.
    - Otherwise, detect scope in this order:
       - Unstaged changes, then staged changes.
       - If no local changes exist, use the latest commit.
    - If no scope can be detected, ask the user to provide one before proceeding.
    - Use tools to collect scope evidence: changed files, git status, diff, and commit message. Record the scope in the report and log.
    - **Execution gates (hard checklist, no silent skips)**:
       - If scope exists, **MUST** run the review subagents. If subagents cannot run, mark this step as **blocked** with reason.
       - If repo_context.md lists checks, **MUST** run at least one relevant static check. Skip only with an explicit user request and quote it in the report.
       - Any skipped step must cite the user request that allowed the skip; otherwise mark it as **blocked**.
    - **Preflight permission**:
       - If running builds/tests/dev server and the user has not opted in, request permission using `AskUserQuestion` (ask question tool) before executing commands.

4. **Iterative Review Loop (required)**
    - For each iteration:
       - Refresh scope and file list.
       - Run subagents in parallel with clear roles and file scopes:
          - Architecture and patterns
          - Security and privacy
          - Performance and reliability
          - Tests and coverage
       - Merge findings without duplication and rank by severity.
       - Identify and label **critical gaps** (security, data loss, broken auth, inconsistent state, failing migrations, missing tests on high-risk paths).
       - If UI changes are in scope, add an optional visual check and note the results.
    - Present findings, call out critical gaps, and ask whether the user wants to fix issues now or proceed.
    - If the user applies fixes or updates, repeat this step with the new scope.

5. **Static Checks (repo-aware, no fixes)**
    - Use [docs/repo_context.md](docs/repo_context.md) to decide which checks to run (lint, type checks, tests, build, hooks).
    - Prefer existing IDE tasks; otherwise run the repository commands directly.
    - Do not fix issues in this step; report only.
    - If a check fails to run due to missing dependencies or environment constraints, mark it as **blocked** with the error output.
    - If a new check or config file is discovered, update repo_context.md so future runs are faster and more accurate.
    - Run atleast 3 checks; More if needed. Mnetion them in docs/repo_context.md for future runs.

6. **Reporting and Logging**
    - Save a detailed report to `docs/code-review/<date-time>_report.md`. Example '2026-03-31_2359_report.md'
    - Report must include: scope, critical gaps, findings by severity, static check results, visual verification notes, and follow-up decision.
    - Maintain a usage log at `docs/code-review/logs/review_log.jsonl` with one JSON object per line:
       - `date`, `time`, `git_user`, `summary`.
    - If the log file or folder does not exist, create it.
    - Example utility command: ```git config user.name; Get-Date -Format "yyyy-MM-dd"; Get-Date -Format "HH:mm:ss"; Get-Date -Format "yyyyMMdd_HHmmss"```

7. **Follow-up: Fix Issues or Draft PR (required)**
   - Ask the user to choose one:
      - Fix critical issues
      - Draft a PR summary
      - Stop
   - If fixing issues, get permission, apply changes or provide guidance, then re-run the review loop.
   - If drafting a PR, hand off to the PR Draft skill and provide the review report path, scope, critical gaps, and check results.

8. **PR Draft Handoff (when requested)**
   - Invoke the PR Draft skill in `.agents/skills/pr-draft/SKILL.md`.
   - Pass along: review report path, scope summary, critical gaps, and any check results.

## Reliability and Security Guidelines

- Use least-privilege and avoid destructive commands.
- Always update repo_context.md when new repo signals appear.
- Prefer evidence-based findings tied to file paths and scope.
