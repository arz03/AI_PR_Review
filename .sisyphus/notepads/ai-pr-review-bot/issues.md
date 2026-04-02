# Issues - AI PR Review Bot

## [2026-04-02T08:15:11.885Z] Session Start

No issues encountered yet.

## [2026-04-02 14:25:51] Task 7 - Workflow Command Syntax Error

**Issue**: GitHub Actions workflow failed at "Run PR review agent" step with exit code 1.

**Symptom**: OpenCode CLI showed help output instead of executing agent, indicating unrecognized command.

**Root Cause**: Used non-existent command `opencode run-agent` with unsupported flags `--input` and `--output`.

**Resolution**: Fixed CLI syntax to match official OpenCode documentation:
- Changed `opencode run-agent pr-reviewer` to `opencode run --agent pr-reviewer`
- Removed `--input` flags, embedded PR context in prompt string
- Removed `--output` flag, used shell redirection `> pr-review.md`

**Status**: RESOLVED - Workflow syntax corrected

**Original Broken Command**:
```yaml
opencode run-agent pr-reviewer \
  --input "pr_url=${{ github.event.pull_request.html_url }}" \
  --input "pr_number=${{ github.event.pull_request.number }}" \
  --input "base_ref=${{ github.base_ref }}" \
  --input "head_ref=${{ github.head_ref }}" \
  --output pr-review.md
```

**Fixed Command**:
```yaml
opencode run --agent pr-reviewer "
Review this pull request:
- PR #${{ github.event.pull_request.number }}
- URL: ${{ github.event.pull_request.html_url }}
- Base: ${{ github.base_ref }}
- Head: ${{ github.head_ref }}

Analyze the changes and provide a detailed code review following your configured review procedure.
Write the full review report to pr-review.md in markdown format.
" > pr-review.md 2>&1
```

**Key Learnings**:
- OpenCode CLI uses `opencode run --agent <name>` NOT `opencode run-agent <name>`
- Inputs must be passed as prompt text, not via `--input` flags
- Output must be redirected via shell `>` not CLI flags
- The `--agent` flag is required when running custom agents
