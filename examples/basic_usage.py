#!/usr/bin/env python3
"""Basic usage example for the HotEval Python SDK."""

import os
import sys

# Add the python directory to the path for local development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python'))

import hoteval  # type: ignore


def main():
    """Run a basic example workflow."""
    print("HotEval SDK Basic Usage Example")
    print("=" * 40)

    # Configure SDK
    # In real usage, set HOTEVAL_API_KEY environment variable
    try:
        hoteval.configure(
            api_key=os.getenv("HOTEVAL_API_KEY", "demo_key"),
            base_url=os.getenv("HOTEVAL_BASE_URL", "http://localhost:8000"),
        )
        print("✓ SDK configured")
    except Exception as e:
        print(f"✗ Failed to configure SDK: {e}")
        return

    # Start a run
    run = hoteval.start_run(
        name="demo.agent.chat",
        meta={
            "user_id": "demo_user",
            "session_id": "sess_123",
            "environment": "demo"
        }
    )
    print(f"✓ Started run: {run.id}")

    # Log a step with events
    step = hoteval.log_step(
        run=run,
        name="llm.chat_completion",
        attrs={
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 150
        },
        events=[
            {
                "type": "prompt",
                "content": "What's the capital of France?",
                "metadata": {"role": "user"}
            },
            {
                "type": "output",
                "content": "The capital of France is Paris.",
                "metadata": {"role": "assistant"}
            }
        ]
    )
    print(f"✓ Logged step: {step.id}")

    # Log another step (tool usage)
    tool_step = hoteval.log_step(
        run=run,
        name="tool.web_search",
        attrs={
            "tool": "web_search",
            "query": "Paris France capital"
        },
        events=[
            {
                "type": "tool_call",
                "content": {
                    "tool": "web_search",
                    "query": "Paris France capital",
                    "results_count": 5
                }
            },
            {
                "type": "tool_result",
                "content": {
                    "results": [
                        {"title": "Paris - Wikipedia", "snippet": "Paris is the capital..."}
                    ]
                }
            }
        ]
    )
    print(f"✓ Logged tool step: {tool_step.id}")

    # End the run
    hoteval.end_run(run)
    print(f"✓ Ended run: {run.id}")

    print()
    print("Summary:")
    print(f"  Run ID: {run.id}")
    print(f"  Steps: {len(run.steps)}")
    print(f"  Total events: {sum(len(step.events) for step in run.steps)}")
    print(f"  Duration: {(run.end_time - run.start_time).total_seconds():.2f}s")
    print()
    print("🎉 Checks will be configured and run automatically in your")
    print("   HotEval dashboard at dev.hoteval.com!")


if __name__ == "__main__":
    main()