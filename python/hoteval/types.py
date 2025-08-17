"""Core types and data models for the HotEval SDK."""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Union


@dataclass
class AgentConfig:
    """Configuration for an agent, set during SDK initialization."""

    name: str
    environment: str  # e.g., "dev", "prod", "staging"
    data_location: str  # e.g., "EU" (US support coming soon)
    version: str  # e.g., "1.0.0", "main", "feature-branch"
    description: Optional[str] = None
    agent_type: str = "sdk_configured"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "environment": self.environment,
            "data_location": self.data_location,
            "version": self.version,
            "description": self.description,
            "agent_type": self.agent_type,
        }


@dataclass
class Event:
    """An event within a step (e.g., prompt, output, tool call)."""

    type: str
    content: Union[str, Dict[str, Any]]
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "type": self.type,
            "content": self.content,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "metadata": self.metadata,
        }


@dataclass
class Step:
    """A step within a run (e.g., LLM call, tool invocation)."""

    name: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    attrs: Optional[Dict[str, Any]] = None
    events: List[Event] = field(default_factory=list)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "attrs": self.attrs,
            "events": [event.to_dict() for event in self.events],
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
        }


@dataclass
class Run:
    """A complete agent run/workflow."""

    name: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    meta: Optional[Dict[str, Any]] = None
    steps: List[Step] = field(default_factory=list)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "meta": self.meta,
            "steps": [step.to_dict() for step in self.steps],
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
        }
