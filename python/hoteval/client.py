"""HotEval client for posting messages to the backend."""

import os
from typing import Any, Dict, Optional

import requests

from .types import Run, Step


class HotEvalClient:
    """Client for posting telemetry data to HotEval backend."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
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

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "hoteval-python-sdk/0.1.0",
            }
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
        data = {
            "type": "run_start",
            "run": run.to_dict(),
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
) -> None:
    """Configure the global HotEval client."""
    global _client
    _client = HotEvalClient(
        api_key=api_key,
        base_url=base_url,
        timeout=timeout,
    )


def get_client() -> HotEvalClient:
    """Get the global client instance."""
    if _client is None:
        raise RuntimeError(
            "HotEval client not configured. Call hoteval.configure() first."
        )
    return _client
