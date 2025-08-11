# HotEval Python SDK

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/hoteval.svg)](https://pypi.org/project/hoteval/)
[![Python Versions](https://img.shields.io/pypi/pyversions/hoteval.svg)](https://pypi.org/project/hoteval/)

**HotEval Python SDK** is the official client library for [HotEval](https://hoteval.ai), enabling you to instrument your AI agents with **runs**, **steps**, and **automated checks**, fully compatible with [OpenTelemetry](https://opentelemetry.io/).

This SDK helps you:
- **Trace** entire agent runs and individual steps
- **Log** prompts, outputs, and tool calls
- **Attach** automated evaluations ("checks") to runs or steps
- **Export** telemetry in OpenTelemetry format for integration with your observability stack

---

## Features

- **Run-level & step-level tracing** — group operations under a single run
- **Structured events** — record prompts, outputs, tool I/O
- **Automated checks** — factuality, numeric sanity, compliance, etc.
- **OpenTelemetry under the hood** — compatible with Jaeger, Grafana, Sentry, etc.
- **Minimal API** — quick to integrate
- **Future-proof** — designed to expand into Node.js & Go SDKs in the same repo

---

## Installation

```bash
pip install hoteval
```

---

## Quickstart

```python
import hoteval

# Start a run (root span)
run = hoteval.start_run(name="agent.run", meta={"project": "Doc QA", "user_id": "u_42"})

# Log a step (child span) with events
step = hoteval.log_step(
    run=run,
    name="llm.call",
    attrs={"model": "gpt-4"},
    events=[
        {"type": "prompt", "content": "What's the capital of France?"},
        {"type": "output", "content": "Paris"}
    ]
)

# Record a check for that step
hoteval.record_check(
    target=step,
    rule="factuality"
)

# Run-level check (applies to whole run)
hoteval.record_check(
    run=run,
    rule="session_compliance"
)

# End the run (triggers run-level evaluations)
hoteval.end_run(run)
```

---

## Concepts

| Concept   | Description |
|-----------|-------------|
| **Run**   | A complete agent interaction or workflow. Maps to the root span in OpenTelemetry. |
| **Step**  | A timed operation inside a run (LLM call, tool invocation). Maps to a child span. |
| **Event** | A point-in-time record inside a step (prompt, output, tool I/O). |
| **Check** | An automated evaluation attached to a run or step (factuality, compliance, etc.). |

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Links

- [HotEval Website](https://hoteval.com)
- [OpenTelemetry](https://opentelemetry.io)
- [PyPI Package](https://pypi.org/project/hoteval/)
