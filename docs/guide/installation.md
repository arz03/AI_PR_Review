# Agent Installation Guide (Claude Code / AI coding agents)

Use this guide when an AI coding agent is asked to install this PR-review workflow into a different repository.

Goal: complete setup end-to-end with minimal ambiguity, then verify using a dry-run PR.

---

## Step 0 — Ask required setup questions first

Before copying or editing anything, the agent should ask the repo owner these decisions:

1. **LLM route**
   - Use default free route: `opencode/qwen3.6-plus-free`
   - Use Groq route (requires `GROQ_API_KEY`; recommended fallback is `groq/openai/gpt-oss-20b`)
   - Use custom OpenAI-compatible provider (requires `CLIENT_LLM_BASE_URL` + `CLIENT_LLM_API_KEY`)

2. **Slack notifications**
   - Enable Slack summary? (Yes/No)
   - If yes, confirm `SLACK_WEBHOOK_URL` is available.

3. **Trigger policy**
   - Keep default triggers (`pull_request` on `opened`, `ready_for_review`) or adjust?

4. **PR size policy**
   - Keep defaults (`PR_REVIEW_WARN_FILES=20`, `PR_REVIEW_SKIP_FILES=50`) or set custom values?

5. **Security policy for URL values**
   - Store `CLIENT_LLM_BASE_URL` as variable (recommended) or secret (org policy dependent).

---

## Step 0.5 — Model/tool-calling warning (important for new agents)

Tool-calling support quality matters for this workflow.

- Prefer models/routes known to reliably support tool use and multi-step instruction following.
- Newer agents should **avoid weak tool-calling model choices** for production setup.
- Strongly prefer models validated for tool-calling in your environment (for example GPT-OSS class routes and modern tool-capable models).
- In this repo, default runtime is `opencode/qwen3.6-plus-free`; fallback route in workflow is `groq/openai/gpt-oss-20b`.

> Practical warning: some older/open weights may run but behave poorly with tool calls and structured workflow instructions under load.

---

## Step 1 — Copy required files into target repository

From this package, copy these files into the client repo preserving paths:

Core runtime:
- `.github/workflows/ai-pr-review.yml`
- `.opencode/agents/pr-reviewer.md`
- `opencode.json`

Templates:
- `docs/templates/finding-schema.md`
- `docs/templates/pr-review-template.md`
- `docs/templates/slack-summary-template.md`

Operational docs (recommended):
- `docs/setup-client-integration.md`
- `docs/client-handoff-checklist.md`
- `docs/guide/installation.md`

Reference: also see `docs/setup-client-integration.md` section **"1) Required Files to Copy"**.

---

## Step 2 — Configure provider/model path

1. Open `opencode.json` and confirm provider blocks are present.
2. Decide default model:
   - Default free route: `opencode/qwen3.6-plus-free`
   - Or change `model` to a selected provider route.
3. In `.github/workflows/ai-pr-review.yml`, confirm `run_review` model route matches selected runtime strategy.

Deterministic check:
- Model route names in workflow `run_review` calls must match keys available in `opencode.json` provider models.
- If you rename a model route, update both workflow and `opencode.json` in the same change.

Current workflow baseline:
- Primary: `opencode/qwen3.6-plus-free`
- Fallback (transient failures): `groq/openai/gpt-oss-20b`

For custom provider route, use format similar to:
- `client-openai-compatible/client-model`

---

## Step 3 — Configure GitHub secrets and variables

Go to: **Settings → Secrets and variables → Actions**

### Secrets tab

Required:
- `SLACK_WEBHOOK_URL` (if Slack notifications are enabled)

Conditional (provider-specific):
- `GROQ_API_KEY`
- `CLIENT_LLM_API_KEY`

### Variables tab

Optional but recommended:
- `PR_REVIEW_WARN_FILES`
- `PR_REVIEW_SKIP_FILES`

Conditional:
- `CLIENT_LLM_BASE_URL` (recommended as variable unless policy requires secret)

Base URL rule:
- Use API root (often ending with `/v1`), **not** endpoint paths like `/chat/completions`.

---

## Step 4 — Confirm workflow behavior and guardrails

Verify in `.github/workflows/ai-pr-review.yml`:

- Trigger events: `opened`, `ready_for_review`
- Marker comment update flow: `<!-- ai-pr-review -->`
- PR size gating: warn/skip thresholds from variables
- Fork safety mode: secret-dependent AI review skipped on fork PRs
- Slack step only runs when webhook is configured and PR is not fork-safety-skipped
- Artifact upload enabled (`pr-review.md`, raw stream, debug logs)

---

## Step 5 — Dry run validation (must do)

1. Create branch in target repo (example: `chore/ai-pr-review-smoke-test`).
2. Add a small test change and open PR.
3. Confirm Actions run starts automatically.
4. Validate outcomes:
   - PR comment is created/updated under marker comment.
   - Slack receives risk/findings/summary (if enabled).
   - Artifacts are downloadable and include debug logs.
5. Re-run with `ready_for_review` transition if needed to validate trigger path.

---

## Step 6 — Troubleshooting quick path

- **AI step skipped**: check file count threshold and fork status.
- **Provider/model errors**: validate API key presence and model route string.
- **Custom provider fails**: verify `CLIENT_LLM_BASE_URL` points to API root.
- **Slack skipped**: ensure `SLACK_WEBHOOK_URL` exists and run is not fork-safety mode.
- **Need diagnostics**: download workflow artifacts (`opencode-debug.log`, fallback log).

For full details, refer to:
- `docs/setup-client-integration.md`
- `docs/client-handoff-checklist.md`

---

## Step 7 — Packaging guidance for zip handoff

When shipping to client for AI-agent installation, include only what is needed.

### Include

- `.github/workflows/ai-pr-review.yml`
- `.opencode/agents/pr-reviewer.md`
- `opencode.json`
- `docs/templates/finding-schema.md`
- `docs/templates/pr-review-template.md`
- `docs/templates/slack-summary-template.md`
- `docs/setup-client-integration.md`
- `docs/client-handoff-checklist.md`
- `docs/guide/installation.md`
- `README.md`

### Remove (before shipping zip)

- `.git/`
- `.env`
- `.sisyphus/`
- `.ruff_cache/`
- `docs/pr-reviews/` (internal run artifacts/history)
- `docs/context/` and `docs/misc/` unless client explicitly requested research/history notes
- any local debug outputs/log files

### Final pre-zip checks

- No secrets/tokens in files.
- Paths in docs match included files.
- Workflow YAML and `opencode.json` are syntactically valid.

---

## Suggested instruction prompt for client to give their agent

"Use `docs/guide/installation.md` and set up AI PR review in this repository end-to-end. Ask me Step 0 questions first, then apply configuration, set required secrets/variables, and run a dry-run PR validation. Do not skip guardrail checks or artifact verification."
