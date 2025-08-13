# HotEval SDK Development Guide

This guide covers developing and maintaining the HotEval SDK across multiple languages.

## Repository Structure

```
hoteval-sdk/
├── python/                 # Python SDK
│   ├── hoteval/           # Python source code
│   ├── tests/             # Python tests
│   ├── scripts/           # Python-specific scripts
│   │   └── release/       # Release automation
│   ├── pyproject.toml     # Python package config
│   └── README.md          # Python documentation
├── schemas/               # Shared message schemas
│   ├── messages.json      # JSON schema for API messages
│   └── tools/             # Schema generation tools
├── examples/              # Usage examples (all languages)
├── scripts/               # Cross-language release automation
├── DEVELOPMENT.md         # Development guide
└── README.md             # Multi-language overview
```

Future language directories (`node/`, `go/`, etc.) will follow the Python pattern.

## Multi-Language Consistency

### 1. Shared Message Schema

All language SDKs post identical JSON messages to the HotEval backend. The schema is defined in `schemas/messages.json` and includes:

- **Run messages**: `run_start`, `run_end`
- **Step messages**: `step`
- **Check messages**: `check`

Each language SDK must:
- Generate messages that conform to the JSON schema
- Use identical field names and types
- Handle timestamps in ISO 8601 format
- Use UUIDs for run/step IDs

### 2. API Consistency

All SDKs should provide equivalent functions:

| Function | Purpose | Parameters |
|----------|---------|------------|
| `init()` | Initialize SDK | `api_key`, `base_url`, `timeout` |
| `start_run()` | Start a run | `name`, `meta` |
| `end_run()` | End a run | `run` |
| `log_step()` | Log a step | `run`, `name`, `attrs`, `events` |
| `record_check()` | Record a check | `rule`, `target/run`, `status`, `score`, `details` |

### 3. Configuration

All SDKs should support the same environment variables:
- `HOTEVAL_API_KEY`: API key
- `HOTEVAL_BASE_URL`: Backend URL (defaults to `https://api.hoteval.com`)

### 4. Error Handling

- All SDKs should fail gracefully if the backend is unreachable
- Network errors should not crash user applications
- Missing API keys should raise clear error messages

## Local Development Setup

### Python SDK

```bash
cd python/
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -e ".[dev]"
```

Run tests:
```bash
pytest tests/ -v
```

Format code:
```bash
black hoteval/
ruff check hoteval/
mypy hoteval/
```

### Testing Against Local Backend

1. Start your HotEval backend locally (e.g., on port 8000)
2. Set environment variables:
   ```bash
   export HOTEVAL_API_KEY="test_key"
   export HOTEVAL_BASE_URL="http://localhost:8000"
   ```
3. Run the example:
   ```bash
   python examples/basic_usage.py
   ```

### Schema Validation

To validate that SDK messages conform to the schema:

```bash
# Install jsonschema
pip install jsonschema

# Validate a message (example)
python -c "
import json
import jsonschema
with open('schemas/messages.json') as f:
    schema = json.load(f)
message = {'type': 'run_start', 'run': {...}}
jsonschema.validate(message, schema)
"
```

## Release Process

### Python SDK

1. **Prepare release:**
   ```bash
   # Update version and run checks
   make release-python VERSION=0.1.0
   ```

2. **Create PR and release draft:**
   ```bash
   # Creates PR and GitHub release draft
   make release-push
   ```

3. **Complete release:**
   - Review and merge the PR
   - Publish the GitHub release
   - CI automatically publishes to PyPI

### Prerequisites

For Python releases, you need:
- PyPI account and API token
- `build` and `twine` packages: `pip install build twine`
- `.pypirc` configured with your credentials

## Future Languages

When adding new language SDKs:

1. **Create language directory** (e.g., `node/`, `go/`)
2. **Implement core types** that serialize to the shared schema
3. **Implement client** that posts to the same backend endpoints
4. **Add tests** that verify message schema compliance
5. **Create release script** following the same pattern
6. **Update this documentation**

### Language-Specific Considerations

**Node.js/TypeScript:**
- Use TypeScript interfaces generated from JSON schema
- Support both CommonJS and ESM
- Publish to npm

**Go:**
- Use struct tags for JSON serialization
- Support Go modules
- Consider using code generation from schema

**Rust:**
- Use serde for serialization
- Publish to crates.io
- Consider using JSON schema code generation

## Backend Contract

The HotEval backend expects HTTP POST requests to these endpoints:

| Endpoint | Purpose | Payload |
|----------|---------|---------|
| `POST /v1/runs/start` | Start run | `{type: "run_start", run: {...}}` |
| `POST /v1/runs/end` | End run | `{type: "run_end", run: {...}}` |
| `POST /v1/steps` | Log step | `{type: "step", run_id: "...", step: {...}}` |
| `POST /v1/checks` | Record check | `{type: "check", target_type: "run\|step", target_id: "...", check: {...}}` |

All requests require:
- `Authorization: Bearer <api_key>` header
- `Content-Type: application/json` header
- Request body must conform to `schemas/messages.json`

## Questions?

- Open an issue for bugs or feature requests
- Check existing issues for common questions
- Refer to language-specific READMEs for implementation details