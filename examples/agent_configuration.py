"""Example: Configuring HotEval SDK with agent metadata.

This example shows how to configure the HotEval SDK with global settings
and then set agent-specific configuration.
"""

import os

from hoteval import configure, end_run, log_step, set_agent, start_run

# Configure global settings (shared across all agents)
configure(
    api_key=os.getenv("HOTEVAL_API_KEY"),
    base_url=os.getenv("HOTEVAL_BASE_URL", "https://api.hoteval.com"),
    environment=os.getenv("ENVIRONMENT", "dev"),  # dev, staging, production
    data_location=os.getenv("DATA_LOCATION", "EU"),  # EU only (US support coming soon)
)

# Set agent-specific configuration
set_agent(
    name="my-chatbot-agent",
    version=os.getenv("VERSION", "1.0.0"),
    description="A conversational AI agent for customer support",
)

# Now all runs will be associated with this agent configuration
def main():
    # Start a run - agent metadata is automatically included
    run = start_run(
        name="customer-inquiry-123",
        meta={
            "customer_id": "cust_456",
            "inquiry_type": "billing",
        }
    )

    # Log steps - they'll be associated with the configured agent
    log_step(
        run=run,
        name="process_inquiry",
        attrs={"model": "gpt-4", "temperature": 0.7},
        events=[
            {
                "type": "prompt",
                "content": "Customer asked about billing issue...",
            },
            {
                "type": "response",
                "content": "Here's how to resolve your billing issue...",
            }
        ]
    )

    # End the run
    end_run(run)
    print(f"Run completed: {run.id}")


if __name__ == "__main__":
    main()