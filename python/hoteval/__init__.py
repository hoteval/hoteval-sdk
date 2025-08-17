"""HotEval Python SDK - Official client library for HotEval AI agent tracing and evaluation."""

__version__ = "0.0.9000"
__author__ = "HotEval Team"
__email__ = "team@hoteval.com"

from .agent import Agent, create_agent
from .client import configure
from .types import AgentConfig, Event, Run, Step

__all__ = [
    "configure",
    "Agent",
    "create_agent",
    "AgentConfig",
    "Run",
    "Step",
    "Event",
]
