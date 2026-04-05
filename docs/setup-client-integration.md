# Integration Setup Guide

This guide documents how to integrate the AI PR Review workflow into a target repository, including OpenAI-compatible provider setup (custom `baseURL` + API key), Slack notifications, and operational controls.

## 1) Required Files to Copy

Core runtime files:
- `.github/workflows/ai-pr-review.yml`
- `.opencode/agents/pr-reviewer.md`
- `opencode.json`

Template files used by the agent/report format:
- `docs/templates/finding-schema.md`
- `docs/templates/pr-review-template.md`
- `docs/templates/slack-summary-template.md`

Recommended docs:
- `README.md`
- `docs/setup-client-integration.md`

## 2) OpenAI-Compatible Provider Configuration

OpenCode supports OpenAI-compatible providers via `@ai-sdk/openai-compatible` with `options.baseURL` and `options.apiKey`.

### 2.1 Reference (Groq)

```json
"groq": {
  "npm": "@ai-sdk/openai-compatible",
  "name": "Groq Inference",
  "options": {
    "baseURL": "https://api.groq.com/openai/v1",
    "apiKey": "{env:GROQ_API_KEY}"
  },
  "models": {
    "openai/gpt-oss-20b": { "name": "GPT-OSS 20B" },
    "openai/gpt-oss-120b": { "name": "GPT-OSS 120B" }
  }
}
```

### 2.2 Custom Internal Provider (OpenAI-compatible)

`opencode.json` includes a plug-and-play provider block:

```json
"client-openai-compatible": {
  "npm": "@ai-sdk/openai-compatible",
  "name": "Client OpenAI-Compatible Provider",
  "options": {
    "baseURL": "{env:CLIENT_LLM_BASE_URL}",
    "apiKey": "{env:CLIENT_LLM_API_KEY}"
  },
  "models": {
    "client-model": { "name": "Client LLM Model" }
  }
}
```

> If your provider model ID is different, rename the `client-model` key accordingly.

### 2.3 Base URL Requirements (Critical)

`CLIENT_LLM_BASE_URL` must be the OpenAI-compatible API root expected by your provider. In practice, this is often a URL ending with `/v1`.

Rules:
- Use full HTTPS URL (`https://...`) and avoid trailing spaces.
- Do **not** include endpoint suffixes like `/chat/completions`; OpenCode/SDK appends paths internally.
- Keep the value identical between local testing and GitHub Actions to avoid environment drift.

Examples:
- ✅ `https://api.groq.com/openai/v1`
- ✅ `https://<client-gateway>/v1`
- ❌ `https://<client-gateway>/v1/chat/completions`

## 3) Selecting Runtime Model in Workflow

The workflow chooses model in `run_review()` calls, not in docs commands.

Current primary call:

```bash
run_review "opencode/qwen3.6-plus-free" "pr-review.raw.jsonl" "opencode-debug.log"
```

To use client provider, update that line to:

```bash
run_review "client-openai-compatible/client-model" "pr-review.raw.jsonl" "opencode-debug.log"
```

Optional fallback can similarly be changed to your internal provider model.

## 4) GitHub Secrets

Set in **Settings → Secrets and variables → Actions** (open the **Secrets** tab, then click **New repository secret**).

Required:
- `SLACK_WEBHOOK_URL`

Provider-specific (as used):
- `GROQ_API_KEY` (if using Groq routes)
- `CLIENT_LLM_API_KEY` (if using client provider)

Also provide:
- `CLIENT_LLM_BASE_URL` (recommended as **repository variable** because it is not typically secret; store as secret only if internal policy classifies endpoints as sensitive)

## 5) GitHub Variables

Set in **Settings → Secrets and variables → Actions** (open the **Variables** tab):
- `PR_REVIEW_WARN_FILES` (default `20`)
- `PR_REVIEW_SKIP_FILES` (default `50`)

Suggested production starting point:
- `PR_REVIEW_WARN_FILES=30`
- `PR_REVIEW_SKIP_FILES=100`

## 6) Slack Setup

1. Create/use Slack app with Incoming Webhooks enabled.
2. Create webhook for target channel.
3. Store URL as `SLACK_WEBHOOK_URL` repository secret.

## 7) Validation Checklist

1. Open test PR and verify workflow triggers on `opened` / `ready_for_review`.
2. Verify single marker comment is created/updated (`<!-- ai-pr-review -->`).
3. Verify Slack message includes PR link, risk, counts, and summary.
4. Download artifacts and verify:
   - `pr-review.md`
   - `pr-review.raw.jsonl`
   - `opencode-debug.log`

## 8) Severity Counts Policy (Comment + Slack)

The workflow normalizes findings to these counts only:
- `Critical`
- `High`
- `Medium`

`Low` and `Info` are still allowed in narrative findings, but are **not** included in Slack count totals. This keeps alerts concise and triage-oriented.

## 9) Secrets vs Variables Matrix

| Name | Type | Required | Purpose |
|---|---|---:|---|
| `SLACK_WEBHOOK_URL` | Secret | Yes | Sends Slack summary |
| `GROQ_API_KEY` | Secret | Conditional | Needed only when Groq route is used |
| `CLIENT_LLM_API_KEY` | Secret | Conditional | Needed only for client OpenAI-compatible provider |
| `CLIENT_LLM_BASE_URL` | Variable (recommended) | Conditional | OpenAI-compatible API base URL |
| `PR_REVIEW_WARN_FILES` | Variable | No | Warn threshold for changed files |
| `PR_REVIEW_SKIP_FILES` | Variable | No | Skip threshold for very large PRs |

## 10) Troubleshooting (Short)

1. **AI step skipped unexpectedly**
   - Check PR changed file count vs `PR_REVIEW_SKIP_FILES`.
   - Check whether PR is from a fork (`fork` safety mode skips secret-dependent review).

2. **Provider auth/model errors**
   - Confirm required API key secret exists and is non-empty.
   - Verify model route matches provider naming (e.g., `provider/model-id`).
   - Verify `CLIENT_LLM_BASE_URL` is valid and points to API root, not endpoint path.

3. **Slack step skipped**
   - Ensure `SLACK_WEBHOOK_URL` repository secret is set.
   - Confirm workflow run is not in fork-safety mode.

4. **Need full debug details**
   - Download workflow artifacts and inspect `opencode-debug.log` and `opencode-debug-fallback.log`.

## 11) Security and Operational Notes

- Secret redaction runs before PR comment/Slack output.
- Fork PR detection prevents secret-dependent AI execution.
- Keep CLI/version/provider updates controlled in CI.
