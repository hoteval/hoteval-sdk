"""Step logging functions."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .client import get_client
from .types import Event, Run, Step


def log_step(
    run: Run,
    name: str,
    attrs: Optional[Dict[str, Any]] = None,
    events: Optional[List[Dict[str, Any]]] = None,
) -> Step:
    """Log a step within a run.

    Args:
        run: Parent run
        name: Step name
        attrs: Optional step attributes
        events: Optional list of event dictionaries

    Returns:
        Step object
    """
    # Convert event dicts to Event objects
    event_objects = []
    if events:
        for event_dict in events:
            event = Event(
                type=event_dict["type"],
                content=event_dict["content"],
                timestamp=datetime.now(timezone.utc),
                metadata=event_dict.get("metadata"),
            )
            event_objects.append(event)

    step = Step(
        name=name,
        attrs=attrs,
        events=event_objects,
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(
            timezone.utc
        ),  # For simplicity, assume step completes immediately
    )

    # Add to run
    run.steps.append(step)

    # Send to backend
    client = get_client()
    client.send_step(run.id, step)

    return step
