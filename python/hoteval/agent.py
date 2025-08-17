"""Agent management for HotEval SDK."""

from contextlib import contextmanager
from typing import Any, Dict, Optional

from .client import get_client
from .runs import end_run, start_run
from .steps import log_step
from .types import Run, Step


class Agent:
    """An agent instance that manages its own runs and configuration."""

    def __init__(
        self,
        name: str,
        version: str,
        environment: Optional[str] = None,
        data_location: Optional[str] = None,
        description: Optional[str] = None,
        agent_type: str = "sdk_configured",
    ):
        """Initialize an agent with its configuration.

        Args:
            name: Agent name
            version: Agent version
            environment: Environment (defaults to global setting)
            data_location: Data location (defaults to global setting)
            description: Optional description
            agent_type: Type of agent
        """
        self.name = name
        self.version = version
        self.environment = environment
        self.data_location = data_location
        self.description = description
        self.agent_type = agent_type

        # Set this agent as the current agent
        client = get_client()
        client.set_agent(
            name=name,
            version=version,
            environment=environment,
            data_location=data_location,
            description=description,
            agent_type=agent_type,
        )

    def start_run(self, name: str, meta: Optional[Dict[str, Any]] = None) -> Run:
        """Start a run with this agent.

        Args:
            name: Run name
            meta: Optional metadata

        Returns:
            Run object
        """
        return start_run(name=name, meta=meta)

    def end_run(self, run: Run) -> None:
        """End a run.

        Args:
            run: Run to end
        """
        end_run(run)

    def log_step(
        self,
        run: Run,
        name: str,
        attrs: Optional[Dict[str, Any]] = None,
        events: Optional[list] = None,
    ) -> Step:
        """Log a step for this agent's run.

        Args:
            run: Parent run
            name: Step name
            attrs: Optional attributes
            events: Optional events

        Returns:
            Step object
        """
        return log_step(run=run, name=name, attrs=attrs, events=events)

    @contextmanager
    def run(self, name: str, meta: Optional[Dict[str, Any]] = None):
        """Context manager for running with this agent.

        Args:
            name: Run name
            meta: Optional metadata

        Yields:
            Run object
        """
        run = self.start_run(name=name, meta=meta)
        try:
            yield run
        finally:
            self.end_run(run)


def create_agent(
    name: str,
    version: str,
    environment: Optional[str] = None,
    data_location: Optional[str] = None,
    description: Optional[str] = None,
    agent_type: str = "sdk_configured",
) -> Agent:
    """Create an agent instance.

    Args:
        name: Agent name
        version: Agent version
        environment: Environment (defaults to global setting)
        data_location: Data location (defaults to global setting)
        description: Optional description
        agent_type: Type of agent

    Returns:
        Agent instance
    """
    return Agent(
        name=name,
        version=version,
        environment=environment,
        data_location=data_location,
        description=description,
        agent_type=agent_type,
    )
