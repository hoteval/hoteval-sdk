# HotEval Python SDK

🎉 **Private Alpha** - Official Python SDK for [HotEval](https://hoteval.com) - Runtime Evaluation for Agentic AI Systems.

## Installation

```bash
pip install hoteval
```

## Quick Start

```python
import hoteval

# Configure global settings (shared across all agents)
hoteval.configure(
    api_key="your_api_key_here",
    environment="dev",  # dev, staging, production
    data_location="EU",  # EU only (US support coming soon)
)

# Create an agent instance
agent = hoteval.create_agent(
    name="my-chatbot-agent",
    version="1.0.0",
    description="My conversational AI agent"
)

# Use the agent for runs (strong coupling)
with agent.run(name="agent.chat", meta={"user_id": "u_123"}) as run:
    agent.log_step(
        run=run,
        name="llm.call",
        attrs={"model": "gpt-4"},
        events=[
            {"type": "prompt", "content": "What's the capital of France?"},
            {"type": "output", "content": "Paris"}
        ]
    )
# Run automatically ends when exiting the context

# 🎉 Checks will be configured and run automatically in your
# HotEval dashboard at dev.hoteval.com!
```

## Best Practices

### Multiple Agents

Create agent instances for strong coupling between agents and their runs:

```python
# Configure once
hoteval.configure(api_key="key", environment="production")

# Create agent instances
support_bot = hoteval.create_agent(
    name="customer-support-chatbot",
    version="2.1.0",
    description="AI chatbot for customer support"
)

analytics_engine = hoteval.create_agent(
    name="data-analytics-agent",
    version="1.5.2",
    description="Data processing engine"
)

# Use agents with strong coupling
with support_bot.run(name="support-chat") as run:
    support_bot.log_step(run=run, name="process_inquiry", events=[...])

with analytics_engine.run(name="data-analysis") as run:
    analytics_engine.log_step(run=run, name="process_data", events=[...])
```

## Configuration

### Global Configuration

Configure shared settings that apply to all agents:

```python
hoteval.configure(
    # Authentication
    api_key="your_api_key_here",  # or set HOTEVAL_API_KEY env var

    # Connection settings
    base_url="https://api.hoteval.com",  # or set HOTEVAL_BASE_URL env var
    timeout=30.0,

    # Default agent settings (can be overridden per agent)
    environment="dev",      # dev, staging, production
    data_location="EU",     # EU only (US support coming soon)
)
```

### Agent Configuration

Create agent instances with their specific configuration:

```python
# Create agents with specific settings
support_bot = hoteval.create_agent(
    name="customer-support-chatbot",
    version="2.1.0",
    description="AI chatbot for customer support"
)

analytics_engine = hoteval.create_agent(
    name="data-analytics-agent",
    version="1.5.2",
    environment="staging",  # Override global setting
    description="Agent for data analysis"
)
```

### Environment Variables

You can use environment variables for configuration:

```bash
export HOTEVAL_API_KEY="your_api_key_here"
export HOTEVAL_BASE_URL="http://localhost:8000"  # for local development
export ENVIRONMENT="dev"
export DATA_LOCATION="EU"
export VERSION="1.0.0"
```

```python
import os
hoteval.configure(
    environment=os.getenv("ENVIRONMENT", "dev"),
    data_location=os.getenv("DATA_LOCATION", "EU"),
)

agent = hoteval.create_agent(
    name="my-agent",
    version=os.getenv("VERSION", "main"),
)
```

### Version Management

Easily manage agent versions and upgrades:

```python
# Create initial agent
support_bot = hoteval.create_agent(
    name="customer-support-chatbot",
    version="2.1.0"
)

# Later, upgrade to new version
support_bot_v2 = hoteval.create_agent(
    name="customer-support-chatbot",  # Same name, different version
    version="2.2.0",
    description="Updated support bot with improved responses"
)

# Use the new version
with support_bot_v2.run(name="support-chat-v2") as run:
    support_bot_v2.log_step(run=run, name="process_inquiry_v2", events=[...])
```

## API Reference

### `hoteval.configure(api_key=None, base_url=None, timeout=30.0, environment=None, data_location=None)`

Configure the SDK with global settings.

**Parameters:**
- `api_key`: API key (or set `HOTEVAL_API_KEY` env var)
- `base_url`: Backend URL (or set `HOTEVAL_BASE_URL` env var)
- `timeout`: Request timeout in seconds
- `environment`: Default environment (dev, staging, production)
- `data_location`: Default data location (EU only, US support coming soon)

### `hoteval.create_agent(name, version, environment=None, data_location=None, description=None, agent_type="sdk_configured")`

Create an agent instance with strong coupling.

**Required parameters:**
- `name`: Agent name
- `version`: Agent version

**Optional parameters:**
- `environment`: Environment (defaults to global setting)
- `data_location`: Data location (defaults to global setting, EU only)
- `description`: Optional description of the agent
- `agent_type`: Type of agent (default: "sdk_configured")

**Returns:** Agent instance

### `agent.run(name, meta=None)`

Context manager for running with an agent.

**Parameters:**
- `name`: Run name
- `meta`: Optional metadata

**Yields:** Run object

### `agent.start_run(name, meta=None)`

Start a run with this agent.

**Parameters:**
- `name`: Run name
- `meta`: Optional metadata

**Returns:** Run object

### `agent.end_run(run)`

End a run.

**Parameters:**
- `run`: Run to end

### `agent.log_step(run, name, attrs=None, events=None)`

Log a step for this agent's run.

**Parameters:**
- `run`: Parent run
- `name`: Step name
- `attrs`: Optional attributes
- `events`: Optional events

**Returns:** Step object

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
