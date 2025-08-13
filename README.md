# HotEval SDKs

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

🎉 **Private Alpha** - Official SDKs for [HotEval](https://hoteval.com) - Runtime Evaluation for Agentic AI Systems.

Continuously monitor, score, and improve your LLM agents in production. HotEval is Sentry meets Pytest, for AI.

## Available SDKs

| Language | Status | Installation | Documentation |
|----------|--------|-------------|---------------|
| **Python** | ✅ Available | `pip install hoteval` | [python/README.md](python/README.md) |
| **Node.js** | 🔄 Under Consideration | - | Coming soon |
| **Go** | 🔄 Under Consideration | - | Coming soon |

## Quick Start

### Python

```python
import hoteval

# Configure with your API key
hoteval.configure(api_key="your_api_key_here")

# Start a run
run = hoteval.start_run(name="agent.chat", meta={"user_id": "u_123"})

# Log a step with events
step = hoteval.log_step(
    run=run,
    name="llm.call",
    attrs={"model": "gpt-4"},
    events=[
        {"type": "prompt", "content": "What's the capital of France?"},
        {"type": "output", "content": "Paris"}
    ]
)

# End the run
hoteval.end_run(run)

# 🎉 Checks are configured in your HotEval dashboard!
```

For detailed Python documentation, see [python/README.md](python/README.md).

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Run** | A complete agent interaction or workflow. Groups related steps together. |
| **Step** | A timed operation inside a run (LLM call, tool invocation, etc.). |
| **Event** | A point-in-time record inside a step (prompt, output, tool I/O). |
| **Check** | Automated evaluations configured in your dashboard (factuality, safety, etc.). |

## Dashboard-Driven Evaluation

**All evaluation logic is configured in your HotEval dashboard**, not in your code:

- **Visual check configuration** - Set up factuality, safety, performance checks with a UI
- **No code changes needed** - Modify check rules without redeploying your app
- **Team collaboration** - Share check configurations across your team
- **Real-time results** - See check results instantly in your dashboard
- **Cross-language consistency** - Same checks work across Python, Node.js, Go SDKs

Simply instrument your code with SDK calls and configure your evaluation rules at [dev.hoteval.com](https://dev.hoteval.com).

## Repository Structure

This repository contains multiple language SDKs with shared schemas and tooling:

```
hoteval-sdk/
├── python/                 # Python SDK
│   ├── hoteval/           # Python source code
│   ├── tests/             # Python tests
│   ├── pyproject.toml     # Python package config
│   └── README.md          # Python documentation
├── schemas/               # Shared message schemas
│   ├── messages.json      # JSON schema for API messages
│   └── tools/             # Schema generation tools
├── examples/              # Usage examples (all languages)
├── scripts/               # Release automation
├── DEVELOPMENT.md         # Development guide
└── README.md             # This file
```

Future language directories (`node/`, `go/`, etc.) will follow the same pattern.

## Authentication

Get your API key from the [HotEval dashboard](https://hoteval.com/dashboard) and set it as an environment variable:

```bash
export HOTEVAL_API_KEY="your_api_key_here"
```

## Development

For development setup and contribution guidelines, see [DEVELOPMENT.md](DEVELOPMENT.md).

Each language SDK has its own development instructions in its respective directory.

## Links

- [HotEval Website](https://hoteval.com)
- [Dashboard](https://dev.hoteval.com)
- [Python SDK Documentation](python/README.md)

## License

This project is licensed under the [MIT License](LICENSE).
