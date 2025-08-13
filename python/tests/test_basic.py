"""Basic tests for the HotEval SDK."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

import hoteval
from hoteval.types import Event, Run, Step


def test_types_serialization():
    """Test that types can be serialized to dictionaries."""
    # Test Event
    event = Event(
        type="prompt",
        content="Hello world",
        timestamp=datetime(2024, 1, 1, 12, 0, 0),
        metadata={"key": "value"}
    )
    event_dict = event.to_dict()
    assert event_dict["type"] == "prompt"
    assert event_dict["content"] == "Hello world"
    assert event_dict["timestamp"] == "2024-01-01T12:00:00"
    assert event_dict["metadata"] == {"key": "value"}

    # Test Step
    step = Step(
        name="llm.call",
        attrs={"model": "gpt-4"},
        events=[event]
    )
    step_dict = step.to_dict()
    assert step_dict["name"] == "llm.call"
    assert len(step_dict["events"]) == 1

    # Test Run
    run = Run(
        name="agent.run",
        meta={"user_id": "u_123"},
        steps=[step]
    )
    run_dict = run.to_dict()
    assert run_dict["name"] == "agent.run"
    assert run_dict["meta"]["user_id"] == "u_123"
    assert len(run_dict["steps"]) == 1


@patch('hoteval.client.requests.Session.post')
def test_sdk_workflow(mock_post):
    """Test the basic SDK workflow."""
    # Mock successful responses
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    # Configure SDK
    hoteval.configure(api_key="test_key", base_url="http://localhost:8000")

    # Start a run
    run = hoteval.start_run(name="test.run", meta={"test": True})
    assert run.name == "test.run"
    assert run.meta is not None
    assert run.meta["test"] is True
    assert run.start_time is not None

    # Log a step
    step = hoteval.log_step(
        run=run,
        name="test.step",
        attrs={"model": "test"},
        events=[
            {"type": "prompt", "content": "Test prompt"},
            {"type": "output", "content": "Test output"}
        ]
    )
    assert step.name == "test.step"
    assert len(step.events) == 2
    assert len(run.steps) == 1

    # End the run
    hoteval.end_run(run)
    assert run.end_time is not None

    # Verify API calls were made (run_start, step, run_end)
    assert mock_post.call_count == 3


def test_client_configure_no_api_key():
    """Test that client configuration fails without API key."""
    with patch.dict('os.environ', {}, clear=True):
        with pytest.raises(ValueError, match="API key required"):
            hoteval.configure()


def test_client_not_configured():
    """Test that functions fail when client not configured."""
    # Reset global client
    hoteval.client._client = None

    with pytest.raises(RuntimeError, match="not configured"):
        hoteval.start_run("test")
