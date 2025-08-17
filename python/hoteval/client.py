"""HotEval client for posting messages to the backend."""

import os
from typing import Any, Dict, Optional

import requests

from .types import AgentConfig, Run, Step


class HotEvalClient:
    """Client for posting telemetry data to HotEval backend."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        default_environment: Optional[str] = None,
        default_data_location: Optional[str] = None,
    ):
        self.api_key = api_key or os.getenv("HOTEVAL_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key required. Set HOTEVAL_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.base_url = base_url or os.getenv(
            "HOTEVAL_BASE_URL", "https://api.hoteval.com"
        )
        self.timeout = timeout

        # Default agent settings that can be overridden per agent
        self.default_environment = default_environment or os.getenv("ENVIRONMENT", "dev")
        self.default_data_location = default_data_location or os.getenv("DATA_LOCATION", "EU")

        # Current agent configuration (can be changed)
        self.current_agent_config: Optional[AgentConfig] = None

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "hoteval-python-sdk/0.1.0",
            }
        )

    def set_agent(
        self,
        name: str,
        version: Optional[str] = None,
        environment: Optional[str] = None,
        data_location: Optional[str] = None,
        description: Optional[str] = None,
        agent_type: str = "sdk_configured",
    ) -> None:
        """Set the current agent configuration.

        Args:
            name: Agent name (required)
            version: Agent version (required)
            environment: Environment (defaults to global setting)
            data_location: Data location (defaults to global setting)
            description: Optional description
            agent_type: Type of agent
        """
        if not name:
            raise ValueError("Agent name is required")
        if not version:
            raise ValueError("Agent version is required")

        # Ensure we have valid environment and data_location values
        final_environment = environment or self.default_environment
        final_data_location = data_location or self.default_data_location

        if not final_environment:
            raise ValueError("Environment is required (set globally or per agent)")
        if not final_data_location:
            raise ValueError("Data location is required (set globally or per agent)")

        self.current_agent_config = AgentConfig(
            name=name,
            version=version,
            environment=final_environment,
            data_location=final_data_location,
            description=description,
            agent_type=agent_type,
        )

    def _post(self, endpoint: str, data: Dict[str, Any]) -> requests.Response:
        """Post data to backend endpoint."""
        base = self.base_url.rstrip("/") if self.base_url else ""
        url = f"{base}/{endpoint.lstrip('/')}"

        try:
            response = self.session.post(
                url,
                json=data,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            # For now, just log and continue - don't fail user's code
            print(f"HotEval: Failed to send data to {url}: {e}")
            raise

    def send_run_start(self, run: Run) -> None:
        """Send run start event to backend."""
        run_dict = run.to_dict()

        # Include agent configuration if available
        if self.current_agent_config:
            run_dict["agent_metadata"] = self.current_agent_config.to_dict()
        else:
            raise RuntimeError(
                "No agent configured. Call client.set_agent() or use hoteval.set_agent() first."
            )

        data = {
            "type": "run_start",
            "run": run_dict,
        }
        self._post("/v1/runs/start", data)

    def send_run_end(self, run: Run) -> None:
        """Send run end event to backend."""
        data = {
            "type": "run_end",
            "run": run.to_dict(),
        }
        self._post("/v1/runs/end", data)

    def send_step(self, run_id: str, step: Step) -> None:
        """Send step data to backend."""
        data = {
            "type": "step",
            "run_id": run_id,
            "step": step.to_dict(),
        }
        self._post("/v1/steps", data)


# Global client instance
_client: Optional[HotEvalClient] = None


def configure(
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    timeout: float = 30.0,
    environment: Optional[str] = None,
    data_location: Optional[str] = None,
) -> None:
    """Configure the global HotEval client with shared settings.

    This sets up the global configuration that will be shared across all agents.
    You must call set_agent() to configure agent-specific settings before starting runs.

    Args:
        api_key: API key for authentication
        base_url: Base URL for the HotEval API
        timeout: Request timeout in seconds
        environment: Default environment (e.g., "dev", "prod", "staging")
        data_location: Default data location (e.g., "US", "EU")
    """
    global _client

    _client = HotEvalClient(
        api_key=api_key,
        base_url=base_url,
        timeout=timeout,
        default_environment=environment,
        default_data_location=data_location,
    )


def set_agent(
    name: str,
    version: str,
    environment: Optional[str] = None,
    data_location: Optional[str] = None,
    description: Optional[str] = None,
    agent_type: str = "sdk_configured",
) -> None:
    """Set the current agent configuration.

    This must be called before starting runs. You can call this multiple times
    to switch between different agents.

    Args:
        name: Agent name (required)
        version: Agent version (required)
        environment: Environment (defaults to global setting)
        data_location: Data location (defaults to global setting)
        description: Optional description of the agent
        agent_type: Type of agent (default: "sdk_configured")
    """
    client = get_client()
    client.set_agent(
        name=name,
        version=version,
        environment=environment,
        data_location=data_location,
        description=description,
        agent_type=agent_type,
    )


def get_client() -> HotEvalClient:
    """Get the global client instance."""
    if _client is None:
        raise RuntimeError(
            "HotEval client not configured. Call hoteval.configure() first."
        )
    return _client
