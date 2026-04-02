---
name: pr-draft
description: "Use when: a user asks to draft a PR, create a pull request summary, or fill a PR template. Produces a concise, high-signal PR title/body that highlights critical gaps and reviewer focus."
---

# PR Draft Skill

This skill drafts a fast, high-value PR description for authors and reviewers.

## Workflow

0. **Execution Todo List (required)**
   - Create a detailed todo list using `TodoWrite` (todo tools) (context, inputs, draft, confirm).

1. **Collect Context (required)**
   - Use `AskUserQuestion` (ask question tool) to gather missing fields:
     - JIRA ID, short title, PR type
     - Problem/impact and root cause
     - Changes summary and behavior changes
     - Tests/validation performed
     - Risks and rollback plan
     - Deployment notes (migrations, backfill, flags/config)
     - Reviewer focus areas
   - If a review report path or scope summary is provided, read it and extract critical gaps and check results.
   - Note: try finding these context yourself before asking questions to user. Include possible answers in question based on available context  

2. **Draft PR (required)**
   - Use the template in [pr_template.md](.agents/skills/pr-draft/pr_template.md).
   - Fill in only relevant sections and keep each bullet crisp.
   - Include critical gaps and reviewer focus to speed review.

3. **Confirm and Deliver**
   - Ask the user to confirm the final title/body before posting or saving. Proceed to make PR using git/available tools on user's behalf as required.
   - If the user wants to fix issues instead, hand off to the code-review skill.

4. **PR creation**
   - If user instructs to proceed with curretn PR draft, create a pull request using git tools.
   - Use `AskUserQuestion` (ask question tool) to ask questions such as target branch (if required).

## Output Rules

- Keep the PR summary under 12 lines when possible.
- Highlight any unresolved critical gaps explicitly.
