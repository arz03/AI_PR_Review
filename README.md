# AI_PR_Review

Automated AI-powered PR review bot using OpenCode with Groq inference.

## Overview

This repository contains a GitHub Actions workflow that automatically reviews pull requests using an AI agent. The bot analyzes code changes, detects security issues, logic errors, performance problems, and provides structured feedback.

## Features

- 🤖 **Automated PR Review**: Triggers on PR creation and when marked ready for review
- 🔒 **Security Analysis**: Detects hardcoded credentials, SQL injection, security misconfigurations
- 🐛 **Logic Error Detection**: Finds boundary errors, missing validations, type issues
- ⚡ **Performance Checks**: Identifies N+1 queries, inefficient loops, missing optimizations
- 📊 **Analytics Focus**: Specialized for Data Science, AI, and Analytics pipeline code

## Configuration

- **AI Model**: OpenAI GPT-OSS 120B via Groq
- **Agent**: Read-only PR reviewer (no code modifications)
- **Triggers**: `opened`, `ready_for_review` events only

## Workflow

1. PR is created or marked ready for review
2. GitHub Actions workflow triggers
3. OpenCode CLI runs the pr-reviewer agent
4. Agent analyzes diff and generates review report
5. Review findings are posted as PR comment

## Mock Files for Testing

The `mock/` directory contains intentionally flawed code for testing:
- `data_pipeline.py` - 4 seeded issues (security, performance, logic)
- `ml_model.py` - 5 seeded issues (logic errors, missing type hints)
- `config.yaml` - 10 seeded issues (security misconfigurations)
- `analytics_query.sql` - 9 seeded issues (SQL injection risks)
- `requirements.txt` - 20 seeded issues (unpinned dependencies)

Total: **39 intentionally seeded issues** for AI detection testing.

## Setup Requirements

1. Set `GROQ_API_KEY` in repository secrets
2. Ensure GitHub Actions have PR write permissions
3. OpenCode CLI will be installed automatically during workflow run

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

This PR includes the Phase 1 implementation. Expected workflow behavior:
- ✅ Workflow should trigger on PR opened
- ⚠️ OpenCode CLI installation may fail (if npm package doesn't exist yet)
- ℹ️ Check Actions tab for detailed execution logs

## Development Status

- [x] Phase 1: Foundation (OpenCode config, agent skeleton, workflow, mock files)
- [ ] Phase 2: Template refinement (schemas, templates, enhanced prompts)
- [ ] Phase 3: Slack integration (webhook, summary extraction)
- [ ] Phase 4: Polish & hardening (idempotent comments, error handling)

