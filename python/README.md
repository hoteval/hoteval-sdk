# HotEval Python SDK

🎉 **Private Alpha** - Official Python SDK for [HotEval](https://hoteval.com) - Runtime Evaluation for Agentic AI Systems.

## Installation

```bash
pip install hoteval
```

## Quick Start

```python
import hoteval

# Configure (requires HOTEVAL_API_KEY env var or pass api_key)
hoteval.configure()

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

# 🎉 Checks will be configured and run automatically in your
# HotEval dashboard at dev.hoteval.com!
```

## Configuration

Set your API key:
```bash
export HOTEVAL_API_KEY="your_api_key_here"
```

Or pass it directly:
```python
hoteval.configure(api_key="your_api_key_here")
```

For local development:
```bash
export HOTEVAL_BASE_URL="http://localhost:8000"
```

## API Reference

### `hoteval.configure(api_key=None, base_url=None, timeout=30.0)`

Configure the SDK.

- `api_key`: API key (or set `HOTEVAL_API_KEY` env var)
- `base_url`: Backend URL (or set `HOTEVAL_BASE_URL` env var)
- `timeout`: Request timeout in seconds

### `hoteval.start_run(name, meta=None)`

Start a new run.

- `name`: Run name/identifier
- `meta`: Optional metadata dictionary

Returns a `Run` object.

### `hoteval.end_run(run)`

End a run.

- `run`: Run object to end

### `hoteval.log_step(run, name, attrs=None, events=None)`

Log a step within a run.

- `run`: Parent run object
- `name`: Step name
- `attrs`: Optional attributes dictionary
- `events`: Optional list of event dictionaries

Returns a `Step` object.

## Data Types

### Event

Events represent point-in-time records within a step:

```python
{
    "type": "prompt",           # Event type
    "content": "Hello world",   # Content (string or dict)
    "metadata": {...}           # Optional metadata
}
```

## Evaluation & Checks 🎉

**Checks are configured in your HotEval dashboard** at [dev.hoteval.com](https://dev.hoteval.com), not in your code! This gives you:

- **Visual check configuration** - Set up factuality, safety, performance checks with a UI
- **No code changes needed** - Modify check rules without redeploying
- **Team collaboration** - Share check configurations across your team
- **Real-time results** - See check results instantly in your dashboard
- **Automated alerts** - Get notified when checks fail

Simply instrument your code with `hoteval.log_step()` and configure your evaluation rules in the dashboard.

## Development

Install development dependencies:
```bash
pip install -e ".[dev]"
```

Run tests:
```bash
pytest
```

Format code:
```bash
black hoteval/
ruff check hoteval/
```

## License

MIT License - see [LICENSE](../LICENSE) file.