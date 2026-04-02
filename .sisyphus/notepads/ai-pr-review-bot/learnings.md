# Learnings - AI PR Review Bot

## [2026-04-02T08:15:11.885Z] Session Start

Initial plan execution started. Key conventions to maintain:
- Model provider: Groq with OpenAI-compatible endpoint
- Agent permissions: Read-only (edit=deny)
- Review focus: Security, logic, performance, testing, API/schema
- Target use case: DS/AI/Analytics pipelines

## [2026-04-02T13:52:00Z] Task 1 Complete - Groq Provider Configuration

**File Created**: `opencode.json` at repository root

**Configuration Structure**:
```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "groq": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Groq Inference",
      "options": {
        "baseURL": "https://api.groq.com/openai/v1",
        "apiKey": "{env:GROQ_API_KEY}"
      },
      "models": {
        "openai-gpt-oss-120b": {
          "name": "GPT-OSS 120B"
        }
      }
    }
  },
  "model": "groq/openai-gpt-oss-120b"
}
```

**Verification Results**:
- ✅ JSON syntax validation passed (node parse successful)
- ✅ Schema field present (`$schema`: `https://opencode.ai/config.json`)
- ✅ Provider key is `groq` (not `groq-openai`)
- ✅ Default model set to `groq/openai-gpt-oss-120b`
- ✅ API key uses environment variable reference `{env:GROQ_API_KEY}`
- ✅ Base URL correctly points to Groq's OpenAI-compatible endpoint

**Key Observations**:
- OpenAI-compatible provider requires `npm` field specifying `@ai-sdk/openai-compatible`
- Custom endpoints use `options.baseURL` configuration
- Model ID format for reference: `{provider}/{model-name}` (`groq/openai-gpt-oss-120b`)
- Evidence saved to `.sisyphus/evidence/task-1-*.txt`

**Next Steps** (from plan):
- Parallel tasks continuing: `.gitignore` and `.aiexclude` configuration

## [2026-04-02T13:54:08Z] Task 3 Complete - Directory Structure Creation

**Directories Created**:
1. .opencode/agents/ - OpenCode agent definition files location
2. docs/pr-reviews/ - Saved review reports storage
3. docs/templates/ - Review and Slack message templates
4. mock/ - Test Python/analytics files with seeded issues
5. .sisyphus/evidence/ - QA evidence capture (existed, now confirmed)

**Initial State**:
- All new directories empty (0 files each)
- .sisyphus/evidence/ contained 1 file from Task 1
- Parent directories created automatically by New-Item -Force

**PowerShell Commands Used**:
- Directory creation: New-Item -ItemType Directory -Force -Path ...
- File counting: (Get-ChildItem -Force | Measure-Object).Count

**Key Observations**:
- Windows/PowerShell requires New-Item -Force vs Unix mkdir -p
- All directories ready for subsequent tasks to populate
- Evidence saved to .sisyphus/evidence/task-3-*.txt

**Directory Purposes**:
- .opencode/agents/ → Task 2 creates pr-reviewer.md
- docs/pr-reviews/ → Output storage for completed reviews
- docs/templates/ → Phase 2 template files
- mock/ → Phase 1 test files with intentional issues
- .sisyphus/evidence/ → Task verification artifacts

## [2026-04-02T14:08:00Z] Task 4 Complete - GitHub Actions PR Review Workflow

**File Created**: `.github/workflows/ai-pr-review.yml`

**Workflow Design Decisions**:
- Trigger scope is intentionally minimal: `pull_request` with `types: [opened, ready_for_review]` only (no `synchronize`) to avoid duplicate re-runs on every push.
- Permissions are job-scoped and least-privilege: `contents: read` + `pull-requests: write` only.
- CLI pattern is used (not OpenCode GitHub action) to preserve explicit output control to `pr-review.md`.
- PR comment publication uses `gh pr comment --body-file pr-review.md` with `GH_TOKEN` from `secrets.GITHUB_TOKEN`.

**Action/Tool Version Choices**:
- `actions/checkout@v4.2.0` pinned (no `@latest`).
- OpenCode CLI installed via npm package `opencode-ai` (current npm availability validated during implementation).
- YAML validation performed with pinned CLI: `npx -y yaml@2.8.1 valid`.

**Execution Inputs Passed to Agent**:
- `pr_url`, `pr_number`, `base_ref`, `head_ref` via repeated `--input` flags.
- `GROQ_API_KEY` injected from `${{ secrets.GROQ_API_KEY }}`.

**Verification Evidence Captured**:
- `.sisyphus/evidence/task-4-workflow-valid.txt` (YAML syntax valid)
- `.sisyphus/evidence/task-4-triggers.txt` (contains opened + ready_for_review; no synchronize)
- `.sisyphus/evidence/task-4-no-latest.txt` (no `@latest` tags)
- `.sisyphus/evidence/task-4-permissions.txt` (permissions block includes only required scopes)

**Observation**:
- PowerShell environment lacked `ConvertFrom-Yaml`; using pinned Node YAML CLI (`yaml@2.8.1`) provided deterministic syntax validation compatible with CI-local checks.

## [2026-04-02T13:53:51Z] Task 2 Complete - PR Reviewer Agent Skeleton

**File Created**: `.opencode/agents/pr-reviewer.md`

**Agent Structure**:
- YAML frontmatter with name, version, description
- Role section emphasizing read-only constraints
- Five focus areas: Security, Logic Errors, Test Coverage, Performance, API/Schema Changes
- Target context: DS/AI/Analytics pipelines
- Placeholder section for Phase 2 detailed review steps

**Key Design Decisions**:
1. **Read-Only Enforcement**: Explicitly documented in multiple sections
   - Role: States agent cannot modify files or execute commands
   - Capabilities: Only read/analyze, no write operations
   - Constraints section: Lists all forbidden actions
   
2. **Focus Area Prioritization**: Ordered by severity
   - Security first (credentials, injection, data exposure)
   - Logic Errors second (edge cases, null handling, types)
   - Test Coverage third (missing tests, coverage gaps)
   - Performance fourth (queries, memory, resource usage)
   - API/Schema fifth (breaking changes, migrations)

3. **Domain Context**: Explicit DS/AI/Analytics focus
   - Python frameworks: pandas, numpy, scikit-learn, pytorch, tensorflow
   - Data processing: spark, dask, ray
   - ML platforms: mlflow, weights & biases, clearml
   - APIs: FastAPI, Flask, gRPC

4. **CLI Invocation Pattern**: Documented for GitHub Actions
   ```bash
   opencode run-agent pr-reviewer --input "pr_url=..."
   ```

5. **Version History Section**: Tracks agent evolution
   - Initial release notes Phase 1, Task 2 origin
   - Allows future updates to document enhancements

**Verification Results**:
- ✅ File created: 3,516 bytes
- ✅ All major sections present: Role, Capabilities, Review Focus, Review Procedure
- ✅ Permissions explicitly documented as read-only
- ✅ Target context matches DS/AI/Analytics use case
- ✅ Placeholder for Phase 2 review logic clearly marked

**Evidence Saved**:
- `.sisyphus/evidence/task-2-file-exists.txt` - File existence verification
- `.sisyphus/evidence/task-2-structure-check.txt` - Section structure verification

**Pattern Observations**:
- Agent definition follows skill structure from `docs/context/skills/code-review/SKILL.md`
- Metadata in YAML frontmatter enables tooling integration
- Section ordering prioritizes critical info (Permissions before Role)
- Explicit constraints prevent misconfiguration in CI environments

**Next Steps** (from plan):
- Phase 2, Task 11 will populate detailed review procedure
- Phase 2, Task 9 will create report templates
## [2026-04-02T13:55:13Z] Task 3 Complete - Directory Structure Creation

**Directories Created**:
1. .opencode/agents/ - OpenCode agent definition files location
2. docs/pr-reviews/ - Saved review reports storage
3. docs/templates/ - Review and Slack message templates
4. mock/ - Test Python/analytics files with seeded issues
5. .sisyphus/evidence/ - QA evidence capture (existed, now confirmed)

**Initial State**:
- All new directories created successfully
- .opencode/agents/ contains pr-reviewer.md from parallel Task 2
- docs/pr-reviews/, docs/templates/, mock/ are empty (ready for content)
- .sisyphus/evidence/ has accumulated evidence from Tasks 1-3

**PowerShell Commands Used**:
- Directory creation: New-Item -ItemType Directory -Force -Path ...`n- File counting: (Get-ChildItem -Force | Measure-Object).Count`n
**Key Observations**:
- Windows/PowerShell requires New-Item -Force vs Unix mkdir -p`n- Parallel Task 2 already populated .opencode/agents/ with pr-reviewer.md`n- All directories ready for subsequent tasks to populate
- Evidence saved to .sisyphus/evidence/task-3-*.txt`n
**Directory Purposes**:
- .opencode/agents/ → Agent definition files (Task 2 created pr-reviewer.md)
- docs/pr-reviews/ → Output storage for completed reviews
- docs/templates/ → Phase 2 template files
- mock/ → Phase 1 test files with intentional issues
- .sisyphus/evidence/ → Task verification artifacts

## [2026-04-02T14:00:00Z] Task 6 Complete - Mock Analytics Configuration Files

**Files Created**:
1. `mock/config.yaml` - Analytics pipeline configuration with 10 seeded issues
2. `mock/analytics_query.sql` - SQL query with 9 seeded issues
3. `mock/requirements.txt` - Python dependencies with 20 seeded issues

**config.yaml Seeded Issues** (10 total):
1. Security: Debug mode enabled in production (`debug: true`)
2. Logic: Missing required 'database' field under database section
3. Security: Placeholder password not replaced (`password: "CHANGE_ME"`)
4. Logic: Missing required 'rate_limit' field under api section
5. Security: API key placeholder present (`api_key: "PLACEHOLDER_KEY_REPLACE_ME"`)
6. Security: Insecure CORS policy (`allow_all_origins: true`)
7. Security: Authentication disabled (`enabled: false`)
8. Security: No encryption specified (`algorithm: none`)
9. Performance: Verbose logging in production (`level: DEBUG`)
10. Logic: Missing required 'backup_enabled' field under features

**analytics_query.sql Seeded Issues** (9 total):
1. Security: SQL injection via `$user_status` interpolation (Line 20)
2. Security: SQL injection via `$region_code` interpolation (Line 21)
3. Performance: Missing index hint on LEFT JOIN for large tables (Line 12)
4. Security: SQL injection via `$start_date`/$`end_date` (Line 33)
5. Performance: CROSS JOIN without WHERE clause filter - cartesian product risk (Line 23)
6. Logic: Missing aggregation on potentially ungrouped data
7. Security: SQL injection in result column (`'$report_type'`) (Line 46)
8. Performance: No query timeout specification
9. Performance: Missing LIMIT clause for result pagination

**requirements.txt Seeded Issues** (20 total):
- 19 unpinned dependencies (no version pinning)
- 1 documented vulnerable package: `requests==2.25.1` (CVE-2023-32681)
- Security-sensitive packages with unpinned versions: pyjwt, cryptography
- ML frameworks without version pinning: tensorflow, torch, scikit-learn

**Verification Results**:
- ✅ YAML syntax validation passed (Python yaml.safe_load)
- ✅ SQL injection patterns detected (4 variable interpolation points)
- ✅ Unpinned dependencies identified (19 packages without ==)
- ✅ Vulnerable package documented in comments

**Pattern Observations**:
1. **Realistic Context**: Files simulate real analytics pipeline (warehouse queries, API configs, ML dependencies)
2. **Issue Detectability**: All issues are code-review-detectable, not runtime-only bugs
3. **Obvious Defaults**: Insecure settings made explicit (e.g., `debug: true`, `allow_all_origins: true`)
4. **Safe Vulnerabilities**: Used safe version numbers and placeholder strings (no real credentials)
5. **SQL Comments**: Added explanatory comments to provide review context
6. **Line-Level Tracking**: All issues documented with line numbers for evidence

**Evidence Files Created**:
- `.sisyphus/evidence/task-6-yaml-valid.txt` - YAML syntax validation
- `.sisyphus/evidence/task-6-sql-issues.txt` - SQL injection patterns
- `.sisyphus/evidence/task-6-unpinned-deps.txt` - Dependency analysis

**Quality Assurance**:
- All three files are syntactically valid and parse correctly
- Issues are realistic for DS/AI/Analytics codebases
- Issues map to agent review focus areas: Security, Logic, Performance
- No actual security vulnerabilities introduced (safe placeholders only)

**Next Steps** (from plan):
- Task 7 will create Python test files with seeded issues
- Agent will use these mock files for review testing

## [2026-04-02T14:02:27Z] Task 5 Complete - Mock Python Files with Seeded Issues

**Files Created**:
1. mock/data_pipeline.py - Data processing script with 4 seeded issues
2. mock/ml_model.py - ML model code with 5 seeded issues

**data_pipeline.py Seeded Issues** (4 total):
1. **Security**: Hardcoded database password (Line 19: DB_PASSWORD = "admin123")
2. **Security**: SQL injection vulnerability (Line 47: query = f"SELECT * FROM users WHERE user_id = '{user_id}'")
3. **Performance**: N+1 query pattern (Line 62: individual queries in loop)
4. **Logic**: Off-by-one boundary error (Line 78: ange(0, user_count + 1, batch_size) should exclude +1)

**ml_model.py Seeded Issues** (5 total):
1. **Logic**: Missing input validation (Line 70-77: no null/empty checks for X, y)
2. **Logic**: Missing error handling (Line 82-90: no try-except around matrix operations)
3. **Code Quality**: Missing type hints on initialize_weights() (Line 41)
4. **Code Quality**: Missing type hints on 	rain() (Line 44)
5. **Code Quality**: Missing type hints on predict() and create_feature_vector() (Lines 98, 126)

**Verification Results**:
- ✅ Python syntax validation passed for both files (python -m py_compile)
- ✅ Hardcoded credential found: DB_PASSWORD = "admin123"
- ✅ SQL injection pattern found: f-string interpolation in SQL query
- ✅ N+1 query pattern present in process_batch() function
- ✅ Missing type hints confirmed on multiple function signatures

**Pattern Observations**:
1. **Realistic DS Context**: Both files use pandas, numpy, psycopg2 (common analytics stack)
2. **Comment Annotations**: Added inline comments marking each issue for easy identification
3. **Safe Placeholders**: Used obviously fake credentials (dmin123) not real-looking secrets
4. **Functional Code**: Both files have complete, runnable logic (not just stubs)
5. **Detectability**: All issues are code-review-detectable without execution
6. **Line-Level Tracking**: All issues documented with line numbers

**Evidence Files Created**:
- .sisyphus/evidence/task-5-python-valid.txt - Python syntax validation
- .sisyphus/evidence/task-5-seeded-issues.txt - Hardcoded credentials verification
- .sisyphus/evidence/task-5-sql-injection.txt - SQL injection pattern verification

**Key Observations for AI PR Review Testing**:
- SQL injection in f-strings is a common real-world pattern
- N+1 queries often hide in "simple" batch processing loops
- Type hints are frequently missing in DS codebases (Python dynamic nature)
- Hardcoded credentials remain common in prototype/POC code
- Off-by-one errors are subtle but critical in batch processing

**Issue Categories Covered**:
- ✅ Security (hardcoded credentials, SQL injection)
- ✅ Logic Errors (off-by-one, missing validation)
- ✅ Performance (N+1 queries, inefficient iteration)
- ✅ Code Quality (missing type hints)

**Files Ready For**: AI PR review bot testing (all issues detectable via static analysis)

