# AI PR Review Bot - Implementation Plan

## TL;DR

> **Quick Summary**: Build an automated AI-powered PR review bot using OpenCode on GitHub Actions with Groq inference, posting structured review findings to PRs and Slack summaries.
> 
> **Deliverables**:
> - OpenCode configuration with Groq provider (`opencode.json`)
> - Custom PR review agent (`.opencode/agents/pr-reviewer.md`)
> - GitHub Actions workflow (`.github/workflows/ai-pr-review.yml`)
> - Review report template and Slack summary format
> - Mock Python/analytics code for testing
> - End-to-end working integration
> 
> **Estimated Effort**: Medium (4 phases)
> **Parallel Execution**: YES - 3 waves per phase
> **Critical Path**: Config → Agent → Workflow → Mock Files → Test PR → Template Refinement → Slack → Polish

---

## Context

### Original Request
Build an internal automated PR review AI bot running on GitHub Actions using OpenCode with Groq (OpenAI-compatible provider). The bot should follow step-by-step review procedures, post findings in a defined template to the PR, and send a summary to Slack.

### Interview Summary
**Key Discussions**:
- **Model**: `openai/gpt-oss-120b` via Groq's OpenAI-compatible endpoint
- **Slack**: Incoming Webhook (simpler than bot token)
- **Report storage**: Both file (`docs/pr-reviews/`) AND PR comment
- **Agent permissions**: Read-only (no command execution)
- **Triggers**: `opened`, `ready_for_review` only (not synchronize)
- **Testing**: Mock Python/analytics code in this repo
- **Focus areas**: Security, logic errors, test coverage, performance, API/schema changes

**Research Findings**:
- CLI pattern recommended for output control (extract summary for Slack)
- `@ai-sdk/openai-compatible` with `options.baseURL` for Groq
- Permission matrix: `contents:read`, `pull-requests:write`
- Reference skills (code-review, pr-draft) provide template structure

### Gap Analysis Review
**Identified Gaps** (addressed in guardrails):
- Idempotent comment strategy (single updatable bot comment per PR)
- PR size limits and chunking behavior
- Fork PR handling (skip with notice)
- Failure-safe messaging on API errors
- Prompt injection resistance
- Output sanitization (no secrets in comments)
- Pinned action versions (no `@latest` in production)

---

## Work Objectives

### Core Objective
Create an automated, reliable AI PR review system that accelerates code review for Data Science/AI/Analytics repositories by surfacing critical issues before human reviewers engage.

### Concrete Deliverables
- `opencode.json` - Provider configuration for Groq
- `.opencode/agents/pr-reviewer.md` - Custom review agent with step-by-step procedure
- `.github/workflows/ai-pr-review.yml` - GitHub Actions workflow
- `docs/templates/pr-review-template.md` - Review output template
- `docs/templates/slack-summary-template.md` - Slack message format
- `mock/` - Test Python/analytics files with seeded issues
- `docs/pr-reviews/` - Directory for saved review reports

### Definition of Done
- [ ] PR created against mock code triggers workflow automatically
- [ ] Review report file saved to `docs/pr-reviews/<PR>_<timestamp>_review.md`
- [ ] Single canonical PR comment posted (updates on reruns)
- [ ] Slack webhook receives summary with severity counts and PR link
- [ ] Seeded issues in mock files are detected by the bot
- [ ] Graceful failure message on API/model errors

### Must Have
- Working end-to-end flow: PR → AI Review → Comment + File + Slack
- Read-only agent (no code modifications)
- Structured output with severity levels and file references
- Idempotent PR comments (update, don't duplicate)
- Groq provider configuration with custom base_url

### Must NOT Have (Guardrails)
- **No auto-fix/code-mod** - Advisory only, no code changes
- **No blocking checks** - PR review is informational, not a required gate
- **No synchronize trigger** - Only `opened` and `ready_for_review`
- **No full-repo audits** - PR diff-focused only
- **No historical dashboards** - Store files but no analytics in v1
- **No threaded discussions** - Single canonical comment only
- **No fork PR execution** - Skip with notice if secrets unavailable
- **No `@latest` tags** - Pin all action versions by SHA or version
- **No secrets in output** - Sanitize all outputs before posting

---

## Verification Strategy (MANDATORY)

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: NO (new project)
- **Automated tests**: None (workflow testing via actual PR creation)
- **Framework**: N/A - Integration testing via GitHub Actions runs

### QA Policy
Every task MUST include agent-executed QA scenarios.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **Workflow/Config**: Use Bash - validate JSON/YAML syntax, check file existence
- **GitHub Actions**: Create test PR, observe workflow run, capture logs
- **PR Comment**: Use `gh pr view` to verify comment content
- **Slack**: Check webhook delivery (manual test URL or log inspection)

---

## Execution Strategy

### Parallel Execution Waves

```
PHASE 1: Foundation (Start Immediately)
├── Wave 1.1 (Parallel - scaffolding):
│   ├── Task 1: Create opencode.json with Groq provider [quick]
│   ├── Task 2: Create .opencode/agents/pr-reviewer.md skeleton [quick]
│   └── Task 3: Create directory structure [quick]
│
├── Wave 1.2 (After 1.1 - workflow + mock):
│   ├── Task 4: Create GitHub Actions workflow [deep]
│   ├── Task 5: Create mock Python files with seeded issues [quick]
│   └── Task 6: Create mock analytics/config files [quick]
│
└── Wave 1.3 (After 1.2 - test):
    └── Task 7: Test Phase 1 - Create PR and verify workflow runs [quick]

PHASE 2: Template Refinement (After Phase 1 verified)
├── Wave 2.1 (Parallel - templates):
│   ├── Task 8: Define structured finding schema [quick]
│   ├── Task 9: Create PR review report template [quick]
│   └── Task 10: Create Slack summary template [quick]
│
├── Wave 2.2 (After 2.1 - agent enhancement):
│   ├── Task 11: Enhance agent with step-by-step procedure [deep]
│   └── Task 12: Add DS/AI/Analytics specific checks [quick]
│
└── Wave 2.3 (After 2.2 - test):
    └── Task 13: Test Phase 2 - Verify improved output quality [quick]

PHASE 3: Slack Integration (After Phase 2 verified)
├── Wave 3.1 (Parallel - Slack setup):
│   ├── Task 14: Add Slack webhook step to workflow [quick]
│   └── Task 15: Create summary extraction script [quick]
│
└── Wave 3.2 (After 3.1 - test):
    └── Task 16: Test Phase 3 - End-to-end with Slack [quick]

PHASE 4: Polish & Hardening (After Phase 3 verified)
├── Wave 4.1 (Parallel - hardening):
│   ├── Task 17: Add idempotent comment logic [quick]
│   ├── Task 18: Add failure handling and graceful messages [quick]
│   ├── Task 19: Add PR size limits and chunking [quick]
│   └── Task 20: Pin action versions to SHA [quick]
│
├── Wave 4.2 (After 4.1 - security):
│   ├── Task 21: Add output sanitization [quick]
│   └── Task 22: Add fork PR handling [quick]
│
└── Wave 4.3 (After 4.2 - final test):
    └── Task 23: Final end-to-end verification [deep]

Wave FINAL (After ALL tasks):
├── Task F1: Plan compliance audit [deep]
├── Task F2: Documentation review [quick]
└── Task F3: Client handoff preparation [quick]
-> Present results -> Get explicit user okay
```

### Dependency Matrix

| Task | Depends On | Blocks | Wave |
|------|------------|--------|------|
| 1-3 | — | 4-7 | 1.1 |
| 4 | 1,2,3 | 7 | 1.2 |
| 5-6 | 3 | 7 | 1.2 |
| 7 | 4,5,6 | 8-10 | 1.3 |
| 8-10 | 7 | 11,12 | 2.1 |
| 11-12 | 8,9,10 | 13 | 2.2 |
| 13 | 11,12 | 14,15 | 2.3 |
| 14-15 | 13 | 16 | 3.1 |
| 16 | 14,15 | 17-20 | 3.2 |
| 17-20 | 16 | 21,22 | 4.1 |
| 21-22 | 17-20 | 23 | 4.2 |
| 23 | 21,22 | F1-F3 | 4.3 |
| F1-F3 | 23 | — | FINAL |

### Agent Dispatch Summary

- **Wave 1.1**: 3 tasks → `quick` x3
- **Wave 1.2**: 3 tasks → `deep` x1, `quick` x2
- **Wave 1.3**: 1 task → `quick`
- **Wave 2.1**: 3 tasks → `quick` x3
- **Wave 2.2**: 2 tasks → `deep` x1, `quick` x1
- **Wave 2.3**: 1 task → `quick`
- **Wave 3.1**: 2 tasks → `quick` x2
- **Wave 3.2**: 1 task → `quick`
- **Wave 4.1**: 4 tasks → `quick` x4
- **Wave 4.2**: 2 tasks → `quick` x2
- **Wave 4.3**: 1 task → `deep`
- **FINAL**: 3 tasks → `deep` x1, `quick` x2

---

## TODOs

### PHASE 1: Foundation

- [x] 1. Create opencode.json with Groq Provider

  **What to do**:
  - Create `opencode.json` at repo root
  - Configure Groq as OpenAI-compatible provider using `@ai-sdk/openai-compatible`
  - Set `baseURL` to `https://api.groq.com/openai/v1`
  - Use `{env:GROQ_API_KEY}` for API key (resolved from environment)
  - Configure model `openai/gpt-oss-120b`
  - Set default model for the project

  **Must NOT do**:
  - Hardcode API keys
  - Use `@latest` or unstable provider versions

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1.1 (with Tasks 2, 3)
  - **Blocks**: Tasks 4, 7
  - **Blocked By**: None

  **References**:
  - `docs/context/perplexity-report.md:23-46` - OpenCode config example with Groq
  - `docs/context/gemini-report.md:30-52` - Groq provider configuration
  - OpenCode docs: https://opencode.ai/docs/providers/

  **Acceptance Criteria**:
  - [ ] File `opencode.json` exists at repo root
  - [ ] JSON is valid (parseable with `jq`)
  - [ ] Contains `provider.groq` with correct baseURL
  - [ ] Contains `model` field set to `groq/openai-gpt-oss-120b`

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: Valid JSON configuration
    Tool: Bash
    Preconditions: opencode.json created
    Steps:
      1. Run `cat opencode.json | jq .`
      2. Assert exit code is 0
      3. Assert output contains "baseURL": "https://api.groq.com/openai/v1"
    Expected Result: Valid JSON with Groq provider configured
    Evidence: .sisyphus/evidence/task-1-json-validation.txt

  Scenario: Missing API key handling
    Tool: Bash
    Preconditions: opencode.json created
    Steps:
      1. Run `grep -c "GROQ_API_KEY" opencode.json`
      2. Assert output is "1" (key referenced via env)
      3. Assert file does NOT contain actual key value
    Expected Result: API key referenced via {env:GROQ_API_KEY}, not hardcoded
    Evidence: .sisyphus/evidence/task-1-no-hardcoded-key.txt
  ```

  **Commit**: YES (groups with Task 2, 3)
  - Message: `feat(pr-review): add opencode config with groq provider`
  - Files: `opencode.json`

---

- [x] 2. Create PR Reviewer Agent Skeleton

  **What to do**:
  - Create `.opencode/agents/pr-reviewer.md`
  - Add YAML frontmatter with: description, mode (primary), model, permissions
  - Set permissions: edit=deny, bash restricted to git/read-only commands
  - Add placeholder system prompt (will be enhanced in Phase 2)
  - Include basic review structure outline

  **Must NOT do**:
  - Allow edit permissions
  - Allow unrestricted bash access
  - Create overly complex prompt (skeleton only)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1.1 (with Tasks 1, 3)
  - **Blocks**: Tasks 4, 7, 11
  - **Blocked By**: None

  **References**:
  - `docs/context/perplexity-report.md:68-122` - Agent YAML frontmatter example
  - `docs/context/gemini-report.md:9-20` - Agent types and permissions
  - `docs/context/skills/code-review/SKILL.md` - Review workflow inspiration

  **Acceptance Criteria**:
  - [ ] File `.opencode/agents/pr-reviewer.md` exists
  - [ ] YAML frontmatter is valid
  - [ ] `permission.edit` is set to `deny`
  - [ ] Model references groq provider

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: Agent file structure valid
    Tool: Bash
    Preconditions: Agent file created
    Steps:
      1. Run `Test-Path ".opencode/agents/pr-reviewer.md"`
      2. Assert returns True
      3. Run `Select-String -Path ".opencode/agents/pr-reviewer.md" -Pattern "^---"`
      4. Assert at least 2 matches (frontmatter delimiters)
    Expected Result: File exists with valid YAML frontmatter
    Evidence: .sisyphus/evidence/task-2-agent-structure.txt

  Scenario: Permissions are read-only
    Tool: Bash
    Preconditions: Agent file created
    Steps:
      1. Run `Select-String -Path ".opencode/agents/pr-reviewer.md" -Pattern "edit:\s*deny"`
      2. Assert match found
    Expected Result: Edit permission explicitly denied
    Evidence: .sisyphus/evidence/task-2-permissions.txt
  ```

  **Commit**: YES (groups with Task 1, 3)
  - Message: `feat(pr-review): add pr-reviewer agent skeleton`
  - Files: `.opencode/agents/pr-reviewer.md`

---

- [x] 3. Create Directory Structure

  **What to do**:
  - Create `.opencode/agents/` directory
  - Create `docs/pr-reviews/` directory for saved reports
  - Create `docs/templates/` directory for templates
  - Create `mock/` directory for test files
  - Create `.sisyphus/evidence/` for QA evidence
  - Add `.gitkeep` files where needed

  **Must NOT do**:
  - Create unnecessary nested structures
  - Add placeholder files beyond .gitkeep

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1.1 (with Tasks 1, 2)
  - **Blocks**: Tasks 4, 5, 6
  - **Blocked By**: None

  **References**:
  - Project structure conventions

  **Acceptance Criteria**:
  - [ ] All directories created
  - [ ] `.gitkeep` files present in empty directories

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: All directories exist
    Tool: Bash
    Preconditions: None
    Steps:
      1. Run `Test-Path ".opencode/agents", "docs/pr-reviews", "docs/templates", "mock"`
      2. Assert all return True
    Expected Result: All required directories exist
    Evidence: .sisyphus/evidence/task-3-directories.txt

  Scenario: Empty directories have .gitkeep
    Tool: Bash
    Preconditions: Directories created
    Steps:
      1. Run `Test-Path "docs/pr-reviews/.gitkeep"`
      2. Assert returns True
    Expected Result: .gitkeep files present
    Evidence: .sisyphus/evidence/task-3-gitkeep.txt
  ```

  **Commit**: YES (groups with Task 1, 2)
  - Message: `chore: create project directory structure`
  - Files: `.opencode/`, `docs/`, `mock/`

---

- [x] 4. Create GitHub Actions Workflow

  **What to do**:
  - Create `.github/workflows/ai-pr-review.yml`
  - Configure triggers: `pull_request: [opened, ready_for_review]`
  - Set permissions: `contents: read`, `pull-requests: write`
  - Add checkout step with `fetch-depth: 0`
  - Add OpenCode CLI installation step
  - Add review execution step using CLI pattern (for output control)
  - Pass GROQ_API_KEY from secrets
  - Write review to `pr-review.md` file
  - Add step to post PR comment using `gh` CLI
  - Pin action versions (not `@latest`)

  **Must NOT do**:
  - Use `@latest` for actions
  - Add `synchronize` trigger
  - Grant unnecessary permissions
  - Hardcode any secrets

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Workflow creation requires careful permission handling and multi-step logic
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1.2 (with Tasks 5, 6)
  - **Blocks**: Task 7
  - **Blocked By**: Tasks 1, 2, 3

  **References**:
  - `docs/context/perplexity-report.md:131-166` - GitHub Action workflow example
  - `docs/context/perplexity-report.md:183-253` - CLI pattern with output capture
  - `docs/context/gemini-report.md:77-127` - Workflow structure and permissions
  - GitHub Actions docs: https://docs.github.com/actions

  **Acceptance Criteria**:
  - [ ] Workflow file exists at `.github/workflows/ai-pr-review.yml`
  - [ ] YAML is valid
  - [ ] Triggers only on `opened` and `ready_for_review`
  - [ ] Permissions are minimal (read contents, write PRs)
  - [ ] No `@latest` tags used
  - [ ] GROQ_API_KEY referenced from secrets

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: Workflow YAML is valid
    Tool: Bash
    Preconditions: Workflow file created
    Steps:
      1. Run `gh workflow list` (if repo is connected)
      2. Or validate with `yq e '.' .github/workflows/ai-pr-review.yml`
      3. Assert no syntax errors
    Expected Result: Valid YAML workflow
    Evidence: .sisyphus/evidence/task-4-workflow-valid.txt

  Scenario: Triggers are correct
    Tool: Bash
    Preconditions: Workflow file created
    Steps:
      1. Run `Select-String -Path ".github/workflows/ai-pr-review.yml" -Pattern "opened"`
      2. Run `Select-String -Path ".github/workflows/ai-pr-review.yml" -Pattern "ready_for_review"`
      3. Run `Select-String -Path ".github/workflows/ai-pr-review.yml" -Pattern "synchronize"`
      4. Assert first two match, third does NOT match
    Expected Result: Only opened and ready_for_review triggers present
    Evidence: .sisyphus/evidence/task-4-triggers.txt

  Scenario: No @latest tags
    Tool: Bash
    Preconditions: Workflow file created
    Steps:
      1. Run `Select-String -Path ".github/workflows/ai-pr-review.yml" -Pattern "@latest"`
      2. Assert no matches found
    Expected Result: All actions pinned to specific versions
    Evidence: .sisyphus/evidence/task-4-no-latest.txt
  ```

  **Commit**: YES
  - Message: `feat(pr-review): add github actions workflow`
  - Files: `.github/workflows/ai-pr-review.yml`

---

- [x] 5. Create Mock Python Files with Seeded Issues

  **What to do**:
  - Create `mock/data_pipeline.py` - Data processing script with seeded issues
  - Include seeded issues:
    - Security: hardcoded credentials, SQL injection risk
    - Logic error: off-by-one, incorrect condition
    - Performance: N+1 pattern, inefficient loop
    - Missing tests indicator (no test file)
  - Create `mock/ml_model.py` - ML model code with issues
  - Include: no input validation, no error handling, missing type hints

  **Must NOT do**:
  - Create actual working ML models
  - Include real credentials (even fake-looking ones should be obvious placeholders)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1.2 (with Tasks 4, 6)
  - **Blocks**: Task 7
  - **Blocked By**: Task 3

  **References**:
  - `docs/context/skills/code-review/SKILL.md:59-64` - Issue categories to seed

  **Acceptance Criteria**:
  - [ ] `mock/data_pipeline.py` exists with 3+ seeded issues
  - [ ] `mock/ml_model.py` exists with 2+ seeded issues
  - [ ] Issues are realistic but obvious to AI reviewer
  - [ ] Files are syntactically valid Python

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: Python files are syntactically valid
    Tool: Bash
    Preconditions: Mock files created
    Steps:
      1. Run `python -m py_compile mock/data_pipeline.py`
      2. Run `python -m py_compile mock/ml_model.py`
      3. Assert both exit with code 0
    Expected Result: Valid Python syntax
    Evidence: .sisyphus/evidence/task-5-python-valid.txt

  Scenario: Security issues are present
    Tool: Bash
    Preconditions: Mock files created
    Steps:
      1. Run `Select-String -Path "mock/*.py" -Pattern "password|secret|api_key" -SimpleMatch`
      2. Assert at least 1 match (seeded credential issue)
    Expected Result: Seeded security issues present for AI to detect
    Evidence: .sisyphus/evidence/task-5-seeded-issues.txt
  ```

  **Commit**: YES (groups with Task 6)
  - Message: `test(pr-review): add mock python files with seeded issues`
  - Files: `mock/data_pipeline.py`, `mock/ml_model.py`

---

- [x] 6. Create Mock Analytics/Config Files

  **What to do**:
  - Create `mock/config.yaml` - Configuration with issues
  - Include: missing required fields, insecure defaults
  - Create `mock/analytics_query.sql` - SQL with issues
  - Include: no parameterization (injection risk), inefficient joins
  - Create `mock/requirements.txt` - Dependencies with issues
  - Include: unpinned versions, known vulnerable packages

  **Must NOT do**:
  - Use actual vulnerable package versions that could be installed
  - Create overly complex configurations

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1.2 (with Tasks 4, 5)
  - **Blocks**: Task 7
  - **Blocked By**: Task 3

  **References**:
  - Common analytics pipeline patterns

  **Acceptance Criteria**:
  - [ ] `mock/config.yaml` exists with seeded issues
  - [ ] `mock/analytics_query.sql` exists with SQL issues
  - [ ] `mock/requirements.txt` exists with dependency issues
  - [ ] All files are syntactically valid

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: Config file is valid YAML
    Tool: Bash
    Preconditions: Config file created
    Steps:
      1. Run `yq e '.' mock/config.yaml` or equivalent
      2. Assert exit code 0
    Expected Result: Valid YAML syntax
    Evidence: .sisyphus/evidence/task-6-yaml-valid.txt

  Scenario: SQL injection risk present
    Tool: Bash
    Preconditions: SQL file created
    Steps:
      1. Run `Select-String -Path "mock/analytics_query.sql" -Pattern "'\s*\+|format\(|%s"`
      2. Assert match found (string concatenation in SQL = injection risk)
    Expected Result: Seeded SQL injection pattern present
    Evidence: .sisyphus/evidence/task-6-sql-issues.txt
  ```

  **Commit**: YES (groups with Task 5)
  - Message: `test(pr-review): add mock analytics files with seeded issues`
  - Files: `mock/config.yaml`, `mock/analytics_query.sql`, `mock/requirements.txt`

---

- [x] 7. Test Phase 1 - Create PR and Verify Workflow

  **What to do**:
  - Create a feature branch with the mock files
  - Push branch to remote
  - Create a PR against main/master
  - Verify workflow triggers automatically
  - Check workflow logs for successful execution
  - Verify PR comment is posted (even if basic)
  - Document any issues found

  **Must NOT do**:
  - Merge the test PR (keep for reference)
  - Skip verification if workflow fails (document and fix)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`git-master`]

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 1.3 (sequential after 1.2)
  - **Blocks**: Tasks 8-10 (Phase 2 start)
  - **Blocked By**: Tasks 4, 5, 6

  **References**:
  - GitHub Actions documentation
  - `gh` CLI documentation

  **Acceptance Criteria**:
  - [ ] Feature branch created and pushed
  - [ ] PR created successfully
  - [ ] Workflow triggered (visible in Actions tab)
  - [ ] Workflow completes (success or documented failure)
  - [ ] If successful: PR comment visible

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: PR triggers workflow
    Tool: Bash
    Preconditions: PR created
    Steps:
      1. Run `gh pr create --title "Test: Phase 1 AI Review" --body "Testing workflow trigger"`
      2. Wait 10 seconds
      3. Run `gh run list --workflow=ai-pr-review.yml --limit 1`
      4. Assert workflow run is visible
    Expected Result: Workflow triggered by PR creation
    Evidence: .sisyphus/evidence/task-7-workflow-triggered.txt

  Scenario: Workflow execution status
    Tool: Bash
    Preconditions: Workflow triggered
    Steps:
      1. Run `gh run list --workflow=ai-pr-review.yml --limit 1 --json status`
      2. Capture status (completed/in_progress/failed)
      3. If failed, capture logs with `gh run view <run-id> --log`
    Expected Result: Workflow status documented
    Evidence: .sisyphus/evidence/task-7-workflow-status.txt
  ```

  **Commit**: NO (test only)

---

### PHASE 2: Template Refinement

- [ ] 8. Define Structured Finding Schema

  **What to do**:
  - Create `docs/templates/finding-schema.md` documenting the structure
  - Define JSON-like schema for findings:
    - `severity`: critical | high | medium | low | info
    - `category`: security | logic | performance | testing | api-schema
    - `file`: file path
    - `line`: line number (optional)
    - `title`: short description
    - `description`: detailed explanation
    - `suggestion`: recommended fix
    - `confidence`: high | medium | low
  - This schema guides agent output format

  **Must NOT do**:
  - Over-complicate the schema
  - Add fields that won't be used

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2.1 (with Tasks 9, 10)
  - **Blocks**: Task 11
  - **Blocked By**: Task 7

  **References**:
  - `docs/context/skills/code-review/SKILL.md:63` - Severity categories
  - Gap analysis: "Structured finding schema + severity taxonomy"

  **Acceptance Criteria**:
  - [ ] Schema documented in `docs/templates/finding-schema.md`
  - [ ] All required fields defined
  - [ ] Enum values for severity and category specified
  - [ ] Example finding included

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: Schema file exists with required fields
    Tool: Bash
    Preconditions: Schema file created
    Steps:
      1. Run `Test-Path "docs/templates/finding-schema.md"`
      2. Run `Select-String -Path "docs/templates/finding-schema.md" -Pattern "severity|category|file|title|description"`
      3. Assert file exists and all fields mentioned
    Expected Result: Complete schema documented
    Evidence: .sisyphus/evidence/task-8-schema.txt
  ```

  **Commit**: YES (groups with Tasks 9, 10)
  - Message: `docs(pr-review): define finding schema`
  - Files: `docs/templates/finding-schema.md`

---

- [ ] 9. Create PR Review Report Template

  **What to do**:
  - Create `docs/templates/pr-review-template.md`
  - Structure sections:
    - Header: PR number, title, author, timestamp, model version
    - Summary: Overall risk level, key themes, one-line verdict
    - Critical Findings: Must-fix issues (severity: critical/high)
    - Other Findings: Medium/low severity items
    - What Was Checked: Categories reviewed
    - Reviewer Focus: Areas human reviewer should examine
    - Agent Notes: Confidence levels, limitations, assumptions
  - Design for human reviewer efficiency

  **Must NOT do**:
  - Make template too verbose (keep it scannable)
  - Include sections that won't have content

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2.1 (with Tasks 8, 10)
  - **Blocks**: Task 11
  - **Blocked By**: Task 7

  **References**:
  - `docs/context/skills/pr-draft/pr_template.md` - PR template inspiration
  - `docs/context/perplexity-report.md:97-119` - Review template example

  **Acceptance Criteria**:
  - [ ] Template file exists at `docs/templates/pr-review-template.md`
  - [ ] Contains: Summary, Critical Findings, Other Findings, Reviewer Focus
  - [ ] Each section has clear formatting instructions
  - [ ] Template is under 50 lines (concise)

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: Template has all required sections
    Tool: Bash
    Preconditions: Template created
    Steps:
      1. Run `Select-String -Path "docs/templates/pr-review-template.md" -Pattern "## Summary|## Critical|## Reviewer Focus"`
      2. Assert at least 3 matches for key sections
    Expected Result: All required sections present
    Evidence: .sisyphus/evidence/task-9-template-sections.txt
  ```

  **Commit**: YES (groups with Tasks 8, 10)
  - Message: `docs(pr-review): add review report template`
  - Files: `docs/templates/pr-review-template.md`

---

- [ ] 10. Create Slack Summary Template

  **What to do**:
  - Create `docs/templates/slack-summary-template.md`
  - Define compact format for Slack:
    - PR title and link
    - Overall risk level (emoji: 🔴🟡🟢)
    - Finding counts by severity
    - One-line summary
    - Link to full review (PR comment)
  - Keep under 500 characters for readability

  **Must NOT do**:
  - Include full findings (summary only)
  - Use complex Block Kit (keep webhook-simple)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2.1 (with Tasks 8, 9)
  - **Blocks**: Task 15
  - **Blocked By**: Task 7

  **References**:
  - `docs/context/gemini-report.md:175-198` - Slack payload example
  - `docs/context/perplexity-report.md:243-253` - Slack notification structure

  **Acceptance Criteria**:
  - [ ] Template file exists at `docs/templates/slack-summary-template.md`
  - [ ] Includes: PR link, risk level, severity counts, summary
  - [ ] Template is compact (under 500 chars when filled)

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: Slack template is compact
    Tool: Bash
    Preconditions: Template created
    Steps:
      1. Run `(Get-Content "docs/templates/slack-summary-template.md" -Raw).Length`
      2. Assert length < 1000 (template itself should be short)
    Expected Result: Template is concise
    Evidence: .sisyphus/evidence/task-10-slack-template.txt
  ```

  **Commit**: YES (groups with Tasks 8, 9)
  - Message: `docs(pr-review): add slack summary template`
  - Files: `docs/templates/slack-summary-template.md`

---

- [ ] 11. Enhance Agent with Step-by-Step Procedure

  **What to do**:
  - Update `.opencode/agents/pr-reviewer.md` with detailed system prompt
  - Define step-by-step review procedure:
    1. Load PR context (title, description, author)
    2. Get diff using `git diff base...head`
    3. Identify changed files and categorize
    4. For each file: analyze security, logic, performance, tests
    5. Cross-reference with project conventions (if AGENTS.md exists)
    6. Prioritize critical issues over nits
    7. Format findings using schema
    8. Generate summary with risk assessment
    9. Write output to file
  - Include DS/AI/Analytics specific checks
  - Reference the finding schema and templates

  **Must NOT do**:
  - Allow agent to modify files
  - Include instructions to run arbitrary commands
  - Make prompt too long (keep focused)

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Complex prompt engineering requiring careful instruction design
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2.2 (with Task 12)
  - **Blocks**: Task 13
  - **Blocked By**: Tasks 8, 9, 10

  **References**:
  - `docs/context/perplexity-report.md:68-122` - Full agent example
  - `docs/context/skills/code-review/SKILL.md:54-66` - Review loop structure
  - `docs/context/gemini-report.md:130-142` - Analysis methodology
  - `docs/templates/finding-schema.md` - Output format

  **Acceptance Criteria**:
  - [ ] Agent prompt includes numbered step-by-step procedure
  - [ ] Each check category has explicit instructions
  - [ ] Output format matches finding schema
  - [ ] Agent references templates for formatting
  - [ ] Read-only permissions maintained

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: Agent has step-by-step procedure
    Tool: Bash
    Preconditions: Agent updated
    Steps:
      1. Run `Select-String -Path ".opencode/agents/pr-reviewer.md" -Pattern "Step [0-9]|1\.|2\.|3\."`
      2. Assert at least 5 matches (numbered steps)
    Expected Result: Clear numbered procedure present
    Evidence: .sisyphus/evidence/task-11-steps.txt

  Scenario: All check categories present
    Tool: Bash
    Preconditions: Agent updated
    Steps:
      1. Run `Select-String -Path ".opencode/agents/pr-reviewer.md" -Pattern "security|logic|performance|test"`
      2. Assert at least 4 matches (all categories mentioned)
    Expected Result: All review categories covered
    Evidence: .sisyphus/evidence/task-11-categories.txt
  ```

  **Commit**: YES (groups with Task 12)
  - Message: `feat(pr-review): enhance agent with detailed review procedure`
  - Files: `.opencode/agents/pr-reviewer.md`

---

- [ ] 12. Add DS/AI/Analytics Specific Checks

  **What to do**:
  - Add to agent prompt specific checks for:
    - Data pipeline integrity (data leakage, train/test contamination)
    - Model versioning (are models pinned, reproducibility)
    - Experiment tracking (are experiments logged properly)
    - Data schema validation (input/output contracts)
    - Resource management (GPU memory, batch sizes)
    - Notebook hygiene (if .ipynb files present)
  - Keep these as additional context, not mandatory checks

  **Must NOT do**:
  - Make these checks mandatory for all PRs
  - Add domain-specific jargon without explanation

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2.2 (with Task 11)
  - **Blocks**: Task 13
  - **Blocked By**: Tasks 8, 9, 10

  **References**:
  - ML best practices
  - Data pipeline patterns

  **Acceptance Criteria**:
  - [ ] DS/AI checks added to agent prompt
  - [ ] At least 4 specific checks defined
  - [ ] Checks are contextual (apply when relevant files detected)

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: DS/AI checks present in agent
    Tool: Bash
    Preconditions: Agent updated
    Steps:
      1. Run `Select-String -Path ".opencode/agents/pr-reviewer.md" -Pattern "data|model|pipeline|experiment"`
      2. Assert at least 3 matches
    Expected Result: DS/AI specific checks included
    Evidence: .sisyphus/evidence/task-12-ds-checks.txt
  ```

  **Commit**: YES (groups with Task 11)
  - Message: `feat(pr-review): add DS/AI specific review checks`
  - Files: `.opencode/agents/pr-reviewer.md`

---

- [ ] 13. Test Phase 2 - Verify Improved Output

  **What to do**:
  - Update the test PR branch with new changes
  - Push and observe re-review (or create new PR)
  - Verify review output matches template structure
  - Check that seeded issues are detected
  - Document detection rate and output quality
  - Note any template adjustments needed

  **Must NOT do**:
  - Skip testing if output looks reasonable
  - Ignore missed detections

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 2.3 (sequential)
  - **Blocks**: Tasks 14, 15 (Phase 3 start)
  - **Blocked By**: Tasks 11, 12

  **References**:
  - Phase 1 test PR

  **Acceptance Criteria**:
  - [ ] Review output follows template structure
  - [ ] At least 50% of seeded issues detected
  - [ ] Severity levels are appropriate
  - [ ] Output is human-readable

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: Review detects seeded issues
    Tool: Bash
    Preconditions: PR reviewed
    Steps:
      1. Run `gh pr view <PR_NUMBER> --comments`
      2. Search output for key issue indicators (security, performance, etc.)
      3. Count detected vs seeded issues
    Expected Result: Majority of seeded issues detected
    Evidence: .sisyphus/evidence/task-13-detection-rate.txt

  Scenario: Output follows template
    Tool: Bash
    Preconditions: Review comment posted
    Steps:
      1. Run `gh pr view <PR_NUMBER> --comments`
      2. Assert contains "## Summary" and "## Critical" sections
    Expected Result: Output matches template structure
    Evidence: .sisyphus/evidence/task-13-template-match.txt
  ```

  **Commit**: NO (test only)

---

### PHASE 3: Slack Integration

- [ ] 14. Add Slack Webhook Step to Workflow

  **What to do**:
  - Add Slack notification step to `.github/workflows/ai-pr-review.yml`
  - Use `slackapi/slack-github-action` (pinned version)
  - Configure for incoming webhook
  - Reference `SLACK_WEBHOOK_URL` from secrets
  - Set `SLACK_WEBHOOK_TYPE: INCOMING_WEBHOOK`
  - Add step after PR comment posting

  **Must NOT do**:
  - Use bot token (keep webhook simple)
  - Send full review content (summary only)
  - Use unpinned action version

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3.1 (with Task 15)
  - **Blocks**: Task 16
  - **Blocked By**: Task 13

  **References**:
  - `docs/context/perplexity-report.md:243-255` - Slack action usage
  - `docs/context/gemini-report.md:177-198` - Slack workflow step
  - Slack GitHub Action: https://github.com/slackapi/slack-github-action

  **Acceptance Criteria**:
  - [ ] Slack step added to workflow
  - [ ] Uses incoming webhook method
  - [ ] Secrets referenced correctly
  - [ ] Action version pinned

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: Slack step present in workflow
    Tool: Bash
    Preconditions: Workflow updated
    Steps:
      1. Run `Select-String -Path ".github/workflows/ai-pr-review.yml" -Pattern "slack-github-action"`
      2. Assert match found
    Expected Result: Slack action step present
    Evidence: .sisyphus/evidence/task-14-slack-step.txt

  Scenario: Webhook configuration correct
    Tool: Bash
    Preconditions: Workflow updated
    Steps:
      1. Run `Select-String -Path ".github/workflows/ai-pr-review.yml" -Pattern "SLACK_WEBHOOK_URL|INCOMING_WEBHOOK"`
      2. Assert both patterns found
    Expected Result: Webhook properly configured
    Evidence: .sisyphus/evidence/task-14-webhook-config.txt
  ```

  **Commit**: YES (groups with Task 15)
  - Message: `feat(pr-review): add slack notification step`
  - Files: `.github/workflows/ai-pr-review.yml`

---

- [ ] 15. Create Summary Extraction Script

  **What to do**:
  - Add inline script or step to extract summary from review file
  - Use `awk` or PowerShell to extract `## Summary` section
  - Format for Slack: include PR link, risk level, finding counts
  - Store extracted summary in GitHub Actions output variable
  - Pass to Slack action payload

  **Must NOT do**:
  - Create complex external scripts
  - Send raw review file to Slack

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3.1 (with Task 14)
  - **Blocks**: Task 16
  - **Blocked By**: Task 13

  **References**:
  - `docs/context/perplexity-report.md:235-241` - Summary extraction example
  - `docs/templates/slack-summary-template.md` - Target format

  **Acceptance Criteria**:
  - [ ] Summary extraction step in workflow
  - [ ] Output stored in GitHub Actions variable
  - [ ] Summary format matches Slack template

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: Summary extraction step exists
    Tool: Bash
    Preconditions: Workflow updated
    Steps:
      1. Run `Select-String -Path ".github/workflows/ai-pr-review.yml" -Pattern "summary|extract"`
      2. Assert extraction step present
    Expected Result: Summary extraction logic in workflow
    Evidence: .sisyphus/evidence/task-15-extraction.txt
  ```

  **Commit**: YES (groups with Task 14)
  - Message: `feat(pr-review): add summary extraction for slack`
  - Files: `.github/workflows/ai-pr-review.yml`

---

- [ ] 16. Test Phase 3 - End-to-End with Slack

  **What to do**:
  - Ensure `SLACK_WEBHOOK_URL` secret is configured
  - Create or update test PR
  - Verify full flow: review → comment → file → Slack
  - Check Slack message format and content
  - Document any issues

  **Must NOT do**:
  - Skip Slack verification
  - Proceed if Slack notification fails silently

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3.2 (sequential)
  - **Blocks**: Tasks 17-20 (Phase 4 start)
  - **Blocked By**: Tasks 14, 15

  **References**:
  - Slack webhook testing

  **Acceptance Criteria**:
  - [ ] Full workflow completes successfully
  - [ ] Slack message received in channel
  - [ ] Message contains PR link and summary
  - [ ] No sensitive data in Slack message

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: Slack notification sent
    Tool: Bash
    Preconditions: PR created, secrets configured
    Steps:
      1. Create/update test PR
      2. Wait for workflow completion
      3. Run `gh run view <run-id> --log` 
      4. Search for Slack step completion
    Expected Result: Slack step shows successful send
    Evidence: .sisyphus/evidence/task-16-slack-sent.txt
  ```

  **Commit**: NO (test only)

---

### PHASE 4: Polish & Hardening

- [ ] 17. Add Idempotent Comment Logic

  **What to do**:
  - Modify PR comment step to find existing bot comment
  - If exists: update comment instead of creating new
  - Use comment identifier (e.g., hidden marker `<!-- ai-pr-review -->`)
  - Implement using `gh api` or `actions/github-script`
  - Add timestamp to show last update time

  **Must NOT do**:
  - Delete old comments (update in place)
  - Create multiple bot comments per PR

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4.1 (with Tasks 18, 19, 20)
  - **Blocks**: Task 23
  - **Blocked By**: Task 16

  **References**:
  - GitHub API: comments endpoint
  - Gap analysis: "Idempotent comment strategy"

  **Acceptance Criteria**:
  - [ ] Bot comment has unique identifier marker
  - [ ] Workflow updates existing comment if present
  - [ ] Only one bot comment exists per PR

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: Comment has identifier marker
    Tool: Bash
    Preconditions: PR reviewed
    Steps:
      1. Run `gh pr view <PR> --comments --json body`
      2. Search for "<!-- ai-pr-review -->" marker
    Expected Result: Identifier marker present in comment
    Evidence: .sisyphus/evidence/task-17-marker.txt

  Scenario: Second run updates comment
    Tool: Bash
    Preconditions: PR reviewed twice
    Steps:
      1. Count bot comments: `gh pr view <PR> --comments | grep -c "AI PR Review"`
      2. Assert count is 1 (not 2)
    Expected Result: Single comment updated, not duplicated
    Evidence: .sisyphus/evidence/task-17-no-duplicate.txt
  ```

  **Commit**: YES (groups with Tasks 18, 19, 20)
  - Message: `fix(pr-review): add idempotent comment updates`
  - Files: `.github/workflows/ai-pr-review.yml`

---

- [ ] 18. Add Failure Handling and Graceful Messages

  **What to do**:
  - Add error handling around OpenCode execution
  - On failure: post "Review unavailable" comment with reason
  - Add timeout handling (set reasonable limits)
  - Ensure Slack still notifies on failure (with error status)
  - Add workflow `continue-on-error` where appropriate

  **Must NOT do**:
  - Fail silently without notification
  - Expose detailed error messages with secrets

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4.1 (with Tasks 17, 19, 20)
  - **Blocks**: Task 23
  - **Blocked By**: Task 16

  **References**:
  - Gap analysis: "Failure-safe messaging"
  - GitHub Actions error handling

  **Acceptance Criteria**:
  - [ ] Error handling wraps OpenCode execution
  - [ ] Failure posts informative comment
  - [ ] Slack notifies on failure
  - [ ] No secrets exposed in error messages

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: Graceful failure handling
    Tool: Bash
    Preconditions: Workflow has error handling
    Steps:
      1. Run `Select-String -Path ".github/workflows/ai-pr-review.yml" -Pattern "continue-on-error|if:.*failure"`
      2. Assert error handling patterns present
    Expected Result: Error handling logic in workflow
    Evidence: .sisyphus/evidence/task-18-error-handling.txt
  ```

  **Commit**: YES (groups with Tasks 17, 19, 20)
  - Message: `fix(pr-review): add failure handling and graceful messages`
  - Files: `.github/workflows/ai-pr-review.yml`

---

- [ ] 19. Add PR Size Limits and Chunking

  **What to do**:
  - Add check for PR size (file count, line count)
  - Define thresholds: warn at 20 files, skip at 50 files
  - For large PRs: post message explaining limitation
  - Optionally: summarize changed file list without full review
  - Document size limits in README

  **Must NOT do**:
  - Attempt to review extremely large PRs (token/cost explosion)
  - Fail silently on large PRs

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4.1 (with Tasks 17, 18, 20)
  - **Blocks**: Task 23
  - **Blocked By**: Task 16

  **References**:
  - Gap analysis: "PR size policy + chunking/fallback behavior"

  **Acceptance Criteria**:
  - [ ] PR size check added to workflow
  - [ ] Large PRs get informative skip message
  - [ ] Thresholds documented

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: Size check logic present
    Tool: Bash
    Preconditions: Workflow updated
    Steps:
      1. Run `Select-String -Path ".github/workflows/ai-pr-review.yml" -Pattern "files|size|too large"`
      2. Assert size handling logic present
    Expected Result: PR size limits implemented
    Evidence: .sisyphus/evidence/task-19-size-limits.txt
  ```

  **Commit**: YES (groups with Tasks 17, 18, 20)
  - Message: `fix(pr-review): add PR size limits`
  - Files: `.github/workflows/ai-pr-review.yml`

---

- [ ] 20. Pin Action Versions to SHA

  **What to do**:
  - Replace all `@vX` tags with commit SHA
  - Actions to pin: `actions/checkout`, `slackapi/slack-github-action`
  - Document pinned versions in workflow comments
  - Add Dependabot config for action updates (optional)

  **Must NOT do**:
  - Use `@latest` anywhere
  - Use floating major version tags in production

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4.1 (with Tasks 17, 18, 19)
  - **Blocks**: Task 23
  - **Blocked By**: Task 16

  **References**:
  - Gap analysis: "Pinned dependencies/actions policy"
  - GitHub security best practices

  **Acceptance Criteria**:
  - [ ] All actions use commit SHA or exact version
  - [ ] No `@latest` tags remain
  - [ ] Versions documented in comments

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: No latest tags
    Tool: Bash
    Preconditions: Workflow updated
    Steps:
      1. Run `Select-String -Path ".github/workflows/ai-pr-review.yml" -Pattern "@latest"`
      2. Assert no matches
    Expected Result: All versions pinned
    Evidence: .sisyphus/evidence/task-20-pinned.txt
  ```

  **Commit**: YES (groups with Tasks 17, 18, 19)
  - Message: `security(pr-review): pin action versions`
  - Files: `.github/workflows/ai-pr-review.yml`

---

- [ ] 21. Add Output Sanitization

  **What to do**:
  - Add sanitization step before posting comment
  - Patterns to redact: API keys, tokens, passwords, connection strings
  - Use regex replacement for common secret patterns
  - Apply sanitization to both PR comment and Slack message
  - Log sanitization actions (without revealing content)

  **Must NOT do**:
  - Skip sanitization
  - Log actual secret values

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4.2 (with Task 22)
  - **Blocks**: Task 23
  - **Blocked By**: Tasks 17, 18, 19, 20

  **References**:
  - Gap analysis: "Output sanitization"
  - `docs/context/gemini-report.md:203-213` - Security considerations

  **Acceptance Criteria**:
  - [ ] Sanitization step added to workflow
  - [ ] Common secret patterns covered
  - [ ] Sanitization applied before all outputs

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: Sanitization patterns present
    Tool: Bash
    Preconditions: Workflow updated
    Steps:
      1. Run `Select-String -Path ".github/workflows/ai-pr-review.yml" -Pattern "sanitize|redact|secret|password|token"`
      2. Assert sanitization logic present
    Expected Result: Output sanitization implemented
    Evidence: .sisyphus/evidence/task-21-sanitization.txt
  ```

  **Commit**: YES (groups with Task 22)
  - Message: `security(pr-review): add output sanitization`
  - Files: `.github/workflows/ai-pr-review.yml`

---

- [ ] 22. Add Fork PR Handling

  **What to do**:
  - Detect if PR is from a fork
  - For fork PRs: post notice that full review unavailable
  - Reason: secrets not available for fork PRs
  - Provide manual review guidance instead
  - Log fork detection

  **Must NOT do**:
  - Attempt to use secrets on fork PRs (will fail)
  - Skip notification entirely for forks

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4.2 (with Task 21)
  - **Blocks**: Task 23
  - **Blocked By**: Tasks 17, 18, 19, 20

  **References**:
  - Gap analysis: "Fork PR secret policy"
  - GitHub Actions fork behavior

  **Acceptance Criteria**:
  - [ ] Fork detection logic added
  - [ ] Fork PRs get informative message
  - [ ] No secret access attempted on forks

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: Fork detection present
    Tool: Bash
    Preconditions: Workflow updated
    Steps:
      1. Run `Select-String -Path ".github/workflows/ai-pr-review.yml" -Pattern "fork|head_repo"`
      2. Assert fork handling logic present
    Expected Result: Fork PR handling implemented
    Evidence: .sisyphus/evidence/task-22-fork-handling.txt
  ```

  **Commit**: YES (groups with Task 21)
  - Message: `fix(pr-review): handle fork PRs gracefully`
  - Files: `.github/workflows/ai-pr-review.yml`

---

- [ ] 23. Final End-to-End Verification

  **What to do**:
  - Create final test PR with all mock files
  - Verify complete flow:
    - Workflow triggers correctly
    - Review generated with proper format
    - PR comment posted (single, with marker)
    - File saved to `docs/pr-reviews/`
    - Slack notification received
  - Test edge cases:
    - Large PR handling
    - Error message display
  - Document final configuration
  - Create setup guide for client
  - Document OpenAI-compatible custom provider integration (custom `baseURL` + API key) for client internal LLM

  **Must NOT do**:
  - Skip any verification step
  - Approve without full test

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Comprehensive verification requiring attention to detail
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 4.3 (sequential)
  - **Blocks**: F1, F2, F3
  - **Blocked By**: Tasks 21, 22

  **References**:
  - All previous tasks
  - Success criteria in this plan

  **Acceptance Criteria**:
  - [ ] All workflow steps complete successfully
  - [ ] Review quality meets expectations
  - [ ] No duplicate comments
  - [ ] Slack received summary
  - [ ] Setup guide created
  - [ ] Setup guide includes OpenAI-compatible custom provider instructions

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: Full workflow success
    Tool: Bash
    Preconditions: Final PR created
    Steps:
      1. Create test PR
      2. Wait for workflow completion
      3. Run `gh run view <run-id>` - assert success
      4. Run `gh pr view <PR> --comments` - verify single bot comment
      5. Run `ls docs/pr-reviews/` - verify file saved
    Expected Result: Complete end-to-end success
    Evidence: .sisyphus/evidence/task-23-e2e-success.txt

  Scenario: Setup guide complete
    Tool: Bash
    Preconditions: Documentation created
    Steps:
      1. Run `Test-Path "README.md"` or setup guide location
      2. Verify contains: GROQ_API_KEY setup, SLACK_WEBHOOK_URL setup, activation steps
    Expected Result: Client-ready setup documentation
    Evidence: .sisyphus/evidence/task-23-setup-guide.txt
  ```

  **Commit**: YES
  - Message: `docs(pr-review): add setup guide and finalize`
  - Files: `README.md`, `docs/`

---

## Final Verification Wave

- [ ] F1. **Plan Compliance Audit** — `deep`
  Read the plan end-to-end. Verify each "Must Have" exists. For each "Must NOT Have": search codebase for forbidden patterns. Check all evidence files exist.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [ ] F2. **Documentation Review** — `quick`
  Verify README updated with setup instructions. Check all templates have usage examples. Ensure secrets documentation is complete.
  Output: `Docs [N/N complete] | VERDICT`

- [ ] F3. **Client Handoff Preparation** — `quick`
  Create setup guide for client: required secrets (GROQ_API_KEY, SLACK_WEBHOOK_URL), workflow activation, testing instructions.
  Output: `Handoff checklist complete | VERDICT`

---

## Commit Strategy

| Phase | Commit |
|-------|--------|
| 1 | `feat(pr-review): add OpenCode config and basic workflow` |
| 2 | `feat(pr-review): enhance agent with review templates` |
| 3 | `feat(pr-review): add Slack integration` |
| 4 | `fix(pr-review): add hardening and error handling` |
| Final | `docs(pr-review): add setup documentation` |

---

## Success Criteria

### Verification Commands
```bash
# Validate JSON config
cat opencode.json | jq .  # Expected: valid JSON with groq provider

# Check workflow syntax
gh workflow list  # Expected: ai-pr-review workflow visible

# Test PR creation triggers workflow
gh pr create --title "Test PR" --body "Testing AI review"
gh run list --workflow=ai-pr-review.yml  # Expected: workflow triggered

# Verify PR comment
gh pr view <PR_NUMBER> --comments  # Expected: AI review comment present

# Check review file saved
ls docs/pr-reviews/  # Expected: review file present
```

### Final Checklist
- [ ] All "Must Have" requirements present
- [ ] All "Must NOT Have" guardrails respected
- [ ] Workflow triggers on `opened` and `ready_for_review` only
- [ ] Single canonical comment per PR (not duplicates)
- [ ] Slack summary sent with PR link and severity counts
- [ ] Graceful failure on API errors
- [ ] No secrets leaked in any output
