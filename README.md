# AI_PR_Review

Automated AI-powered PR review bot using OpenCode, with Slack notifications and support for OpenAI-compatible custom providers.

## Overview

This repository contains a GitHub Actions workflow that automatically reviews pull requests using an AI agent. The bot analyzes code changes, detects security issues, logic errors, performance problems, and provides structured feedback.

## Integration Guides (Start Here)

For quick setup in another repository:

- **Human setup guide**: [docs/setup-client-integration.md](docs/setup-client-integration.md)
- **LLM Agent setup guide (Claude Code / AI coding agents)**: [docs/guide/installation.md](docs/guide/installation.md)

This guide provides a deterministic, step-by-step setup flow including:
- initial configuration questions to ask the user,
- provider/model selection guardrails,
- file copy checklist,
- secrets/variables setup,
- and a dry-run PR validation workflow.

## Features

- 🤖 **Automated PR Review**: Triggers on PR creation and when marked ready for review
- 🔒 **Security Analysis**: Detects hardcoded credentials, SQL injection, security misconfigurations
- 🐛 **Logic Error Detection**: Finds boundary errors, missing validations, type issues
- ⚡ **Performance Checks**: Identifies N+1 queries, inefficient loops, missing optimizations
- 📊 **Analytics Focus**: Specialized for Data Science, AI, and Analytics pipeline code
- 💬 **Slack Notifications**: Posts compact PR review summary to configured channel
- 🧩 **Provider Flexibility**: Supports OpenAI-compatible providers via configurable `baseURL` + API key

## Runtime Configuration

- **Current workflow primary model**: `opencode/qwen3.6-plus-free`
- **Optional provider fallback**: `groq/openai/gpt-oss-20b` (via `@ai-sdk/openai-compatible`)
- **Pinned OpenCode CLI version in workflow**: `opencode-ai@1.3.13`
- **Agent**: Read-only PR reviewer (no code modifications)
- **Triggers**: `opened`, `ready_for_review` events only

## Workflow

1. PR is created or marked ready for review
2. GitHub Actions workflow triggers
3. OpenCode CLI runs the pr-reviewer agent
4. Agent analyzes diff and generates review report
5. Review findings are posted/updated as a single marker comment
6. Slack summary is sent (if webhook configured)
7. Review artifacts are uploaded (`pr-review.md`, `pr-review.raw.jsonl`, debug logs)

### Workflow Guardrails

- Fork PRs run in safe mode (secret-dependent AI execution is skipped)
- PR size policy supports warn/skip thresholds (`PR_REVIEW_WARN_FILES`, `PR_REVIEW_SKIP_FILES`)
- Review output is sanitized before PR comment and Slack notification

## Mock Files for Testing

The `mock/` directory contains intentionally flawed code for testing:
- `data_pipeline.py` - 4 seeded issues (security, performance, logic)
- `ml_model.py` - 5 seeded issues (logic errors, missing type hints)
- `config.yaml` - 10 seeded issues (security misconfigurations)
- `analytics_query.sql` - 9 seeded issues (SQL injection risks)
- `requirements.txt` - 20 seeded issues (unpinned dependencies)

Total: **39 intentionally seeded issues** for AI detection testing.

## Setup Requirements

1. Configure `SLACK_WEBHOOK_URL` in repository secrets
2. Ensure GitHub Actions permissions include `pull-requests: write`
3. (Optional) Configure provider secrets/vars for non-default model routes (`GROQ_API_KEY`, `CLIENT_LLM_API_KEY`, `CLIENT_LLM_BASE_URL`)
4. OpenCode CLI is installed automatically during workflow run

### Optional Variables (PR size policy)

Set in **Settings → Secrets and variables → Actions → Variables**:
- `PR_REVIEW_WARN_FILES` (default `20`)
- `PR_REVIEW_SKIP_FILES` (default `50`)

## Repository Structure

```
.
├── .github/workflows/
│   └── ai-pr-review.yml       # GitHub Actions workflow
├── .opencode/agents/
│   └── pr-reviewer.md         # AI agent configuration
├── mock/                       # Test files with seeded issues
├── docs/
│   ├── pr-reviews/            # Saved review reports
│   └── templates/             # Review templates
└── opencode.json              # OpenCode configuration
```

## Testing This PR

Expected workflow behavior:
- ✅ Workflow triggers on PR opened / ready_for_review
- ✅ PR comment is created/updated under the marker `<!-- ai-pr-review -->`
- ✅ Slack summary sends when `SLACK_WEBHOOK_URL` is configured
- ℹ️ Use Actions artifacts for execution logs and debug files

