# Client Handoff Checklist

Use this checklist when onboarding the workflow into a client repository.

## Required Secrets

- [ ] `SLACK_WEBHOOK_URL`
- [ ] `GROQ_API_KEY` (if Groq route is used)
- [ ] `CLIENT_LLM_API_KEY` (if internal provider route is used)

## Required Variables

- [ ] `PR_REVIEW_WARN_FILES` (recommended: `30`)
- [ ] `PR_REVIEW_SKIP_FILES` (recommended: `100`)
- [ ] `CLIENT_LLM_BASE_URL` (if internal provider route is used)

## Required Files

- [ ] `.github/workflows/ai-pr-review.yml`
- [ ] `.opencode/agents/pr-reviewer.md`
- [ ] `opencode.json`
- [ ] `docs/templates/finding-schema.md`
- [ ] `docs/templates/pr-review-template.md`
- [ ] `docs/templates/slack-summary-template.md`
- [ ] `docs/setup-client-integration.md`

## Verification Steps

- [ ] Open PR and confirm workflow triggers on `opened` / `ready_for_review`
- [ ] Confirm single marker comment is created/updated (`<!-- ai-pr-review -->`)
- [ ] Confirm Slack receives risk + findings + summary + review link
- [ ] Confirm artifacts are downloadable (`pr-review.md`, debug logs)
- [ ] Confirm fork PRs do not attempt secret-dependent AI execution

## Operational Notes

- The workflow is advisory (informational review), not an auto-fix pipeline.
- Output sanitization is applied before comment and Slack publication.
- Review size policy is configurable with repo variables.
