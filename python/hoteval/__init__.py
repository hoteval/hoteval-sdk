"""HotEval Python SDK - Official client library for HotEval AI agent tracing and evaluation."""

__version__ = "0.1.0"
__author__ = "HotEval Team"
__email__ = "team@hoteval.com"

from .client import configure
from .runs import end_run, start_run
from .steps import log_step
from .types import Event, Run, Step

__all__ = [
    "configure",
    "start_run",
    "end_run",
    "log_step",
    "Run",
    "Step",
    "Event",
]
