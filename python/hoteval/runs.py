"""Run management functions."""

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from .client import get_client
from .types import Run


def start_run(name: str, meta: Optional[Dict[str, Any]] = None) -> Run:
    """Start a new run.

    Args:
        name: Run name
        meta: Optional metadata dictionary

    Returns:
        Run object
    """
    run = Run(
        name=name,
        meta=meta,
        start_time=datetime.now(timezone.utc),
    )

    # Send to backend
    client = get_client()
    client.send_run_start(run)

    return run


def end_run(run: Run) -> None:
    """End a run.

    Args:
        run: Run object to end
    """
    run.end_time = datetime.now(timezone.utc)

    # Send to backend
    client = get_client()
    client.send_run_end(run)
