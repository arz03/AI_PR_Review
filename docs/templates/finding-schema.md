## Finding Schema

Use this compact schema for every issue found by the PR review agent.

### Schema

```json
{
  "severity": "critical | high | medium | low | info",
  "category": "security | logic | performance | testing | api-schema",
  "file": "path/to/file.ext",
  "line": 123,
  "title": "Short issue title",
  "description": "Clear explanation of what is wrong and why it matters.",
  "suggestion": "Concrete remediation or safer alternative.",
  "confidence": "high | medium | low"
}
```

### Field Notes

- `line` is optional when no exact line is available.
- `title` should be one line and scannable.
- `description` should focus on impact/risk, not style nits.
- `suggestion` should be actionable and specific.

### Example Finding

```json
{
  "severity": "critical",
  "category": "security",
  "file": "mock/data_pipeline.py",
  "line": 47,
  "title": "SQL injection via string interpolation",
  "description": "User input is interpolated directly into SQL, allowing attacker-controlled query execution.",
  "suggestion": "Replace with parameterized query: cursor.execute(\"SELECT ... WHERE user_id = %s\", (user_id,)).",
  "confidence": "high"
}
```
