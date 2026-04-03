# Client Integration Setup Guide

This guide explains how to integrate the AI PR Review workflow into a client repository, including:
- OpenCode provider setup
- OpenAI-compatible custom LLM provider (custom `baseURL` + API key)
- Slack webhook setup
- GitHub secrets/variables
- Validation steps

## 1) Required Repository Files

- `.github/workflows/ai-pr-review.yml`
- `.opencode/agents/pr-reviewer.md`
- `opencode.json`

## 2) LLM Provider Configuration

The repository supports both:
- `opencode/qwen3.6-plus-free` (current workflow runtime model)
- OpenAI-compatible providers (e.g. Groq, internal client provider)

### 2.1 Groq (reference)

Already configured in `opencode.json`:

```json
"groq": {
  "npm": "@ai-sdk/openai-compatible",
  "options": {
    "baseURL": "https://api.groq.com/openai/v1",
    "apiKey": "{env:GROQ_API_KEY}"
  }
}
```

### 2.2 Client OpenAI-Compatible Provider (plug-and-play)

`opencode.json` includes:

```json
"client-openai-compatible": {
  "npm": "@ai-sdk/openai-compatible",
  "options": {
    "baseURL": "{env:CLIENT_LLM_BASE_URL}",
    "apiKey": "{env:CLIENT_LLM_API_KEY}"
  },
  "models": {
    "client-model": { "name": "Client LLM Model" }
  }
}
```

To use it in workflow, set model override in run step:

```bash
opencode run --agent pr-reviewer --model client-openai-compatible/client-model ...
```

If the client provider uses a different model ID, update `opencode.json` model key accordingly.

## 3) GitHub Secrets

Configure in: **Settings → Secrets and variables → Actions → Repository secrets**

Required:
- `SLACK_WEBHOOK_URL` (for Slack notifications)

Optional (for non-qwen providers):
- `GROQ_API_KEY`
- `CLIENT_LLM_API_KEY`

For custom provider base URL (if sensitive), either:
- add as secret and map in workflow env, or
- store as repository variable and reference at runtime.

## 4) GitHub Variables (recommended)

Configure in: **Settings → Secrets and variables → Actions → Repository variables**

Supported runtime controls:
- `PR_REVIEW_WARN_FILES` (default `20`)
- `PR_REVIEW_SKIP_FILES` (default `50`)

Suggested production defaults:
- `PR_REVIEW_WARN_FILES=30`
- `PR_REVIEW_SKIP_FILES=100`

## 5) Slack Setup

1. Create/choose Slack app → enable Incoming Webhooks
2. Generate webhook URL for target channel
3. Store as `SLACK_WEBHOOK_URL` repository secret

## 6) Validation Checklist

1. Open a PR and verify workflow triggers
2. Confirm PR review comment is posted/updated (single marker comment)
3. Confirm Slack message contains:
   - PR link
   - Risk
   - Findings counts
   - Summary
4. Download workflow artifacts and verify:
   - `pr-review.md`
   - `pr-review.raw.jsonl`
   - `opencode-debug.log`

## 7) Security Notes

- Do not print secrets in logs.
- Output sanitization is applied before posting PR comment and Slack summary.
- Fork PRs are detected and handled without secret-dependent AI execution.
