# Decisions - AI PR Review Bot

## [2026-04-02T08:15:11.885Z] Session Start

### Key Architectural Decisions
1. **CLI Pattern over Action**: Use OpenCode CLI directly for better output control (enables Slack summary extraction)
2. **Idempotent Comments**: Single updatable bot comment per PR (prevents spam)
3. **Incoming Webhook**: Slack integration via webhook (simpler than bot token)
4. **Read-only Agent**: No command execution or file modifications (safest for CI)
5. **Model Format**: `groq/openai-gpt-oss-120b` via `@ai-sdk/openai-compatible`
