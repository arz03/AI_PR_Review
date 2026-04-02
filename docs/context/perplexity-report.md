# Designing an OpenCode-based AI PR Review Bot in GitHub Actions with Custom OpenAI-Compatible Providers

## Overview

OpenCode can be run headlessly inside GitHub Actions to review pull requests automatically and post comments back to the PR, either via the dedicated `anomalyco/opencode/github` action or by invoking the CLI directly in a job.[^1][^2][^3] The same workflow can send a Slack message using any standard Slack GitHub Action or direct webhook call, so an AI-generated review can be surfaced both in GitHub and Slack.[^4][^5][^6]

## Architecture at a Glance

A practical architecture for your use case has three main pieces:

- OpenCode configuration (providers, models, and optional custom review agent) that lives in `opencode.json` and `auth.json` or environment variables on the runner.[^7][^8][^9]
- A GitHub Actions workflow triggered on `pull_request` that either calls the `anomalyco/opencode/github` action with a custom review prompt or runs the OpenCode CLI directly with a scripted prompt.[^1][^2][^9][^10]
- One or more Slack steps in the same job that construct a message (using the PR metadata and, optionally, parsed AI review output) and send it to a target channel.[^4][^5][^6]

This keeps all execution on your GitHub runners so no third‑party SaaS needs repository access, and still lets you talk to OpenAI-compatible APIs such as Groq via OpenCode’s provider system.[^11][^7][^12]

## Configuring OpenCode with a Custom OpenAI-Compatible Base URL

OpenCode uses the AI SDK and Models.dev under the hood and supports 75+ providers, including arbitrary OpenAI-compatible endpoints configured via `options.baseURL` in `opencode.json`.[^7][^13] The provider docs explicitly state that the `baseURL` option lets you point a provider at a proxy or custom endpoint, and the custom-provider section shows using `@ai-sdk/openai-compatible` for `/v1/chat/completions` style APIs with `options.baseURL`, `options.apiKey`, and `options.headers`.[^7][^8]

A common pattern for OpenAI-compatible services (Poe, Z.AI, local gateways, etc.) is to define a custom provider entry that wraps the OpenAI schema and sets `baseURL` to the third-party service, then reference it as `provider/model` from OpenCode and from GitHub Actions.[^7][^8][^9] For example, this configuration (reduced from real-world blog and tutorial examples) shows how to point OpenCode at an OpenAI-compatible HTTP endpoint using AI SDK’s OpenAI-compatible adapter:

```jsonc
// opencode.json at repo root or in ~/.config/opencode/opencode.json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "groq-openai": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Groq (OpenAI-compatible)",
      "options": {
        "baseURL": "https://api.groq.com/openai/v1",
        "headers": {
          "Authorization": "Bearer {env:GROQ_API_KEY}"
        }
      },
      "models": {
        "gpt-oss-120b": {
          "name": "GPT-OSS 120B"
        }
      }
    }
  },
  "model": "groq-openai/gpt-oss-120b"
}
```

This structure exactly matches how the OpenCode docs configure other OpenAI-compatible providers (like Poe, Z.AI, LM Studio, Ollama, and generic custom providers), only differing in the service-specific `baseURL` and model IDs.[^7][^8][^13][^9]

## Environment Variable-Based Base URL Overrides

Several integration guides and client-agnostic docs also show configuring OpenAI-compatible tools (including OpenCode) by setting `OPENAI_API_KEY` and `OPENAI_BASE_URL` environment variables before launching the tool, so calls to OpenAI’s SDK automatically go through your gateway instead of the default API endpoint.[^12][^14] A StepFun/OpenCode integration, for example, exports `OPENAI_BASE_URL` to point OpenCode at `https://api.stepfun.ai/step_plan/v1`, then verifies it with `echo $OPENAI_BASE_URL` before running OpenCode.[^14]

Community troubleshooting threads confirm that when running OpenCode inside Docker, the correct behavior is to ensure `OPENAI_API_KEY` and `OPENAI_BASE_URL` are set on the container and that any `baseURL` in `opencode.json` matches the environment configuration, otherwise OpenCode will fall back to defaults.[^15] Coder’s AI Bridge documentation also explicitly calls out OpenCode as a typical OpenAI-compatible client where you customize the base URL so `/v1/chat/completions` calls are routed through the bridge host instead of directly to OpenAI.[^12]

## Using Groq Specifically with OpenCode

Groq is supported in two ways with OpenCode:

- As a first-class provider selected via `/connect Groq` and `/models`, using Groq’s own provider configuration.[^7][^16]
- As a generic OpenAI-compatible endpoint reachable at `https://api.groq.com/openai/v1`, which is compatible with AI SDK’s OpenAI-compatible adapter.

Groq’s own docs show calling the models endpoint at `https://api.groq.com/openai/v1/models`, matching the OpenAI-compatible path shape that OpenCode’s custom-provider mechanism expects.[^17][^18] Combining this with OpenCode’s example for a custom OpenAI-compatible provider gives you a clean way to use model IDs like `openai/gpt-oss-120b` through OpenCode by specifying `npm: "@ai-sdk/openai-compatible"` and setting `options.baseURL` to Groq’s OpenAI-style endpoint.[^7][^17][^18]

## Defining a Review Agent and Passing Step-by-Step Instructions

OpenCode lets you define agents either in `opencode.json` or as Markdown files under `~/.config/opencode/agents/` or `.opencode/agents/` in your project, including specialized “code-reviewer” agents.[^19] Agent configs can include a `prompt` field pointing to a file with detailed system instructions, including step-by-step review procedures and output templates, which are loaded whenever that agent is invoked.[^19]

For example, you can create a project-scoped review agent that bakes in your multi-step process and output template:

```yaml
# .opencode/agents/pr-reviewer.md
---
description: PR code reviewer for this repo
mode: primary
model: groq-openai/gpt-oss-120b
permission:
  edit: deny
  bash:
    "*": allow
---

You are the strict internal PR review bot for this repository.

Follow this exact step-by-step procedure on every run:
1. Briefly restate the PR title and description.
2. Inspect the full git diff for this PR and identify the main areas of change.
3. Evaluate:
   - Correctness and potential bugs
   - Security risks
   - Performance regressions
   - API and schema changes
   - Test coverage and missing tests
4. Prioritize **high-impact issues** over nits; ignore style and naming unless they affect readability or correctness.
5. If changes are large, focus your deep review on the most critical modules.

Respond using this markdown template only:

```markdown
## Summary
- Overall risk: ow/medium/high>
- Key theme: <one-line description>

## Must-fix issues before merge
- [ ] <issue 1>
- [ ] <issue 2>

## Nice-to-have improvements
- [ ] <suggestion 1>

## Test coverage
- Existing tests impacted:
  - st or "none">
- Recommended new/updated tests:
  - st>

## Notes
- Any assumptions or caveats.
```
```

When you invoke this `pr-reviewer` agent, it will always follow the baked-in step list and emit output in the specified template unless overridden.[^19] For workflows that prefer to keep configuration in code, you can instead define the agent in `opencode.json` with a `prompt` pointing to a `./prompts/pr-reviewer.md` file that contains the same instructions.[^19]

## Using the Official `anomalyco/opencode/github` Action on PRs

The OpenCode GitHub integration provides a composite action `anomalyco/opencode/github@latest` that can be wired to multiple GitHub events, including `pull_request`.[^1][^2][^20] For `pull_request` events, if no `prompt` is provided, the GitHub docs state that OpenCode will “default to reviewing the pull request,” and the action can create comments and PR updates using either the OpenCode GitHub App or the standard `GITHUB_TOKEN`.[^2][^20]

The same docs show that you can override the default behavior by passing a custom `prompt`, and that parameters like `model`, `agent`, `share`, and `use_github_token` are available.[^1][^2][^20] Community examples (for instance, using Z.AI’s GLM‑5 with OpenCode in Actions) demonstrate a typical pattern where a `pull_request`-triggered workflow checks out the repo, runs `anomalyco/opencode/github@latest` with a `model` like `zai/glm-5`, and provides a multi-line `prompt` instructing OpenCode to review the PR for code quality, bugs, and improvements.[^9]

A minimal PR-review workflow using your custom Groq-backed provider might look like this:

```yaml
name: opencode-pr-review

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          persist-credentials: false

      - name: Run OpenCode PR review
        uses: anomalyco/opencode/github@latest
        env:
          GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          model: groq-openai/gpt-oss-120b
          agent: pr-reviewer          # uses the agent defined in opencode config
          use_github_token: true
          prompt: |
            Review this pull request using the `pr-reviewer` agent.
            - Use the repository diff and PR metadata.
            - Follow the agent's built-in step-by-step procedure.
            - Post a single PR comment in the exact markdown template.
```

This mirrors the official examples, just swapping Anthropic or Z.AI models for your Groq-backed provider and custom agent; the OpenCode docs explicitly treat `model` as `provider/model`, and the GitHub examples show the same syntax.[^1][^2][^9][^20]

## Capturing AI Output for Slack Summaries

By default, the OpenCode GitHub action posts its response back into GitHub (as comments, branches, or PRs) and logs details in the job output, but does not expose a dedicated `output` field for downstream steps.[^2][^20] There are two main strategies seen in community setups and blog posts for feeding AI review content into Slack:

- Use the OpenCode CLI directly so you can write the AI review to a file (for example, `report.md`), then both post that file as a PR comment and parse out a summary section to send to Slack.[^10]
- Let OpenCode comment on the PR, then in a later step query the GitHub API (using `actions/github-script` or `gh api`) to fetch that comment, extract the `## Summary` section, and pass it to a Slack action.

Martin Alderson’s CI/CD walkthrough describes the first pattern generically: clone repo, install OpenCode (often via Docker), inject `auth.json`, run `opencode` with a prompt that asks it to generate `report.md` based on the PR diff, then post that report back to the PR and optionally send it to Slack.[^10] The same pattern can be implemented inside GitHub Actions with a shell step instead of a generic CI job.

## Example Workflow Using OpenCode CLI Plus Slack

To maximize control over Slack summaries, the CLI pattern is often the most straightforward, because you fully control where the AI output is written and how it is parsed.[^10] An end-to-end workflow might look like this (simplified):

```yaml
name: pr-ai-review

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write

    env:
      GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
      SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install OpenCode (CLI)
        run: |
          curl -fsSL https://raw.githubusercontent.com/opencode-ai/opencode/main/install.sh | bash

      - name: Run OpenCode PR review
        run: |
          # Assume opencode.json + agents are in repo
          opencode run -m groq-openai/gpt-oss-120b "\
          You are the internal PR review bot.\n\
          1. Read the git diff for this PR (base: ${{ github.base_ref }}, head: ${{ github.head_ref }}).\n\
          2. Apply the following checklist: correctness, security, performance, tests.\n\
          3. Produce a markdown report with these sections: Summary, Must-fix issues, Nice-to-have, Test coverage.\n\
          4. Keep Summary to 3 bullet points.\n\
          Write the full report to pr-review.md in the repo root." > /tmp/opencode-log.txt

      - name: Comment on PR with review
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const fs = require('fs');
            const body = fs.readFileSync('pr-review.md', 'utf8');
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.payload.pull_request.number,
              body
            });

      - name: Extract summary for Slack
        id: summary
        run: |
          awk '/^## Summary/{flag=1;next}/^## /{flag=0}flag' pr-review.md > summary.txt
          echo "summary<<EOF" >> $GITHUB_OUTPUT
          cat summary.txt >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Send Slack notification
        uses: slackapi/slack-github-action@v1.23.0
        with:
          payload: |
            {
              "text": "AI PR review summary for ${{ github.event.pull_request.html_url }}:\n${{ steps.summary.outputs.summary }}"
            }
        env:
          SLACK_WEBHOOK_URL: ${{ env.SLACK_WEBHOOK_URL }}
          SLACK_WEBHOOK_TYPE: INCOMING_WEBHOOK
```

The Slack integration here is based on Slack’s official GitHub Action examples, which show sending a JSON payload containing rich Block Kit messages or simple text via `slackapi/slack-github-action` with `SLACK_WEBHOOK_URL` and `SLACK_WEBHOOK_TYPE` set.[^6][^21] Other Slack actions, such as `act10ns/slack` or `step-security/github-actions-slack`, provide similar patterns if you prefer using bot tokens and channels over webhooks.[^4][^5]

## Choosing Between the Official Action and the CLI Pattern

If you only need a comment in the PR and are comfortable with a more “black box” behavior, the official `anomalyco/opencode/github` action is the easiest to wire up and benefits from OpenCode’s built-in GitHub context handling and authentication via the GitHub App or `GITHUB_TOKEN`.[^1][^2][^20] It is already used in examples and tutorials for automated PR reviews with providers like Anthropic, Hugging Face-backed models, and Z.AI, demonstrating that this pattern is stable in production setups.[^9][^22]

If you need to treat the AI review as data—storing it in files, parsing specific sections, or combining it with other tooling such as Slack—you get more control by invoking `opencode` directly, as described in the CI/CD blog and community orchestrator projects.[^10][^23] In this pattern you manage your own GitHub API calls and Slack messages, but OpenCode still does all the heavy lifting for diff analysis and review logic.

## Known Pitfalls and Version Notes

A GitHub issue in the OpenCode repo reports a bug where options such as `baseURL` and `apiKey` for custom OpenAI-compatible providers were not being forwarded correctly to the AI SDK provider instance, causing API calls to ignore the configured custom endpoint.[^24] The issue describes a configuration with `npm: "@ai-sdk/openai-compatible"` and `options.baseURL: "http://localhost:3000/v1"` that should have been used but was not, implying that on older OpenCode versions you might need to upgrade or verify that the fix has been released before relying on advanced `options` fields.[^24][^25]

Additionally, several community posts around Dockerized OpenCode emphasize aligning environment variables like `OPENAI_BASE_URL` and provider-specific env variables (for example, `ZAI_API_KEY`) with what your `opencode.json` expects, otherwise the wrong provider or default base URL can be used.[^15][^9] As always, running `opencode auth list` and `opencode models` locally with the same config you intend to use in CI is a good smoke test before wiring everything into GitHub Actions.[^7]

## Practical Guidance for Your Implementation

Putting the research together, a practical approach for your internal AI PR review bot is:

- Configure an OpenAI-compatible provider in `opencode.json` that points to your Groq (or other) base URL using either `options.baseURL` or `OPENAI_BASE_URL`, and keep the API key in GitHub Secrets.[^7][^12][^14][^9]
- Define a `pr-reviewer` agent (JSON or Markdown) that encodes your strict step-by-step review checklist and markdown output template so it can be reused across local and CI runs.[^19]
- Start with the official `anomalyco/opencode/github` action for low-friction PR comments; once that works, switch to the CLI pattern if you need fine-grained control of the review output for Slack.[^1][^2][^9][^10]
- For Slack, adopt a webhook-based GitHub Action (or Slack’s official action) and feed it either a parsed `## Summary` section from the AI report or a short, human-readable message linking back to the PR and AI review comment.[^4][^5][^6]

Following these patterns aligns with how OpenCode’s own docs, third-party tutorials, and community posts run agents in CI/CD for PR reviews, while giving you the flexibility to plug in any OpenAI-compatible backend via base URL configuration.

---

## References

1. [GitHub Integration - Actions - OpenCode Docs](https://open-code.ai/en/docs/github) - AI-powered GitHub automation. Fix issues, review PRs, automate with Actions. Mention /opencode in co...

2. [GitHub - OpenCode](https://opencode.ai/docs/github/) - Use OpenCode in GitHub issues and pull-requests.

3. [CLI | OpenCode](https://opencode.ai/docs/cli/) - This sets up the necessary GitHub Actions workflow and guides you through the configuration process....

4. [Github Action for sending message (and reactions/threads ...](https://github.com/step-security/github-actions-slack) - This Action allows you to send messages (and reactions/threads/update/blocks) to Slack from your Git...

5. [GitHub Actions Slack integration - GitHub Marketplace](https://github.com/marketplace/actions/slack-github-actions-slack-integration) - Examples. To send a Slack message when a workflow job has completed add the following as the last st...

6. [plato-app/github_actions_slack: Send data into Slack using ...](https://github.com/plato-app/github_actions_slack) - This package has three different techniques to send data to Slack. The recommended way to use this a...

7. [Providers - OpenCodeopencode.ai › docs › providers](https://opencode.ai/docs/providers/) - Using any LLM provider in OpenCode.

8. [Connect OpenAI-Compatible APIs to OpenCode - Mehmet Baykar](https://mehmetbaykar.com/posts/connect-openai-compatible-apis-to-opencode/) - Configure OpenCode to use any OpenAI-compatible endpoint like Poe with provider and auth JSON files.

9. [How to use GLM-5 with OpenCode in GitHub Actions - AI Engineer ...](https://aiengineerguide.com/til/opencode-github-actions-glm-5/) - Make sure that you've configured API key in Github Actions which you can do via repo's setting. ... ...

10. [GitHub - darrenhinde/OpenAgentsControl: AI agent framework for plan-first development workflows with approval-based execution. Multi-language support (TypeScript, Python, Go, Rust) with automatic testing, code review, and validation built for OpenCode](https://github.com/darrenhinde/OpenAgentsControl) - AI agent framework for plan-first development workflows with approval-based execution. Multi-languag...

11. [How Coding Agents Actually Work: Inside OpenCode | Moncef Abboud](https://cefboud.com/posts/coding-agents-internals-opencode-deepdive/) - A hands-on exploration of OpenCode, an open-source coding agent built with a client/server architect...

12. [Client Configuration | Coder Docs](https://coder.com/docs/ai-coder/ai-bridge/clients) - OpenAI-compatible clients: Set the base URL (commonly via the OPENAI_BASE_URL ... OpenCode. Configur...

13. [Proveedores IA - Configuración de 75+ Modelos LLM](https://open-code.ai/es/docs/providers) - Conecta Claude, GPT-4, DeepSeek, Ollama y 75+ modelos IA. Configuracion facil para Anthropic, OpenAI...

14. [Open Code Integration Guide](https://platform.stepfun.ai/docs/en/step-plan/integrations/opencode) - brew install anomalyco/tap/opencode ... Whether the environment variables were written correctly (ru...

15. [Opencode docker container not taking base url or api key - Reddit](https://www.reddit.com/r/docker/comments/1r5ofk0/opencode_docker_container_not_taking_base_url_or/) - -e OPENAI_BASE_URL=" https://api.z.ai/api/coding/paas/v4" \ ghcr.io ... and ~/opencode/data/opencode...

16. [OpenCode + Groq - GroqDocs](https://console.groq.com/docs/coding-with-groq/opencode) - Connect OpenCode's open-source AI coding agent to Groq for fast inference in terminal, desktop, or I...

17. [Groq provider - AI SDK](https://ai-sdk.dev/providers/ai-sdk-providers/groq)

18. [Supported Models - GroqDocs - Groq Console](https://console.groq.com/docs/models) - Explore all available models on GroqCloud.

19. [Agents - OpenCode](https://opencode.ai/docs/agents/) - Configure and use specialized agents.

20. [GitHub | OpenCode](https://dev.opencode.ai/docs/github) - ... anomalyco/opencode/github@latest. env ... Action runner's built-in GITHUB_TOKEN without installi...

21. [Example workflow: direct message the author - Slack API](https://docs.slack.dev/tools/slack-github-action/sending-techniques/sending-data-slack-api-method/direct-message-author/) - This workflow sends a direct message to the user that pushed the most recent commits. This example u...

22. [Automating Code Review with GitHub Actions - Hugging Face](https://huggingface.co/docs/inference-providers/guides/github-actions-code-review) - Automating Code Review with GitHub ActionsWhat the OpenCode GitHub App DoesStep 1: Install OpenCodeS...

23. [I built an OpenCode Automation Orchestrator for GitHub Repos](https://www.reddit.com/r/opencodeCLI/comments/1q6x3dj/i_built_an_opencode_automation_orchestrator_for/) - I built an OpenCode Automation Orchestrator for GitHub Repos

24. [Custom OpenAI-compatible provider options not being passed to ...](https://github.com/anomalyco/opencode/issues/5674) - Custom OpenAI-compatible provider options not being passed to API calls Description Summary When usi...

25. [Releases · anomalyco/opencode](https://github.com/anomalyco/opencode/releases) - The open source coding agent. Contribute to anomalyco/opencode development by creating an account on...

