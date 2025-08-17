"""Example: Using environment variables for agent configuration.

This example shows how to use environment variables to configure
the agent for different environments (dev, staging, production).
"""

import os

from hoteval import configure, end_run, log_step, set_agent, start_run

# Environment-specific configuration
# You can set these in your deployment environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
DATA_LOCATION = os.getenv("DATA_LOCATION", "EU")
VERSION = os.getenv("VERSION", "main")

# Configure global settings with environment-aware configuration
configure(
    api_key=os.getenv("HOTEVAL_API_KEY"),
    base_url=os.getenv("HOTEVAL_BASE_URL", "https://api.hoteval.com"),
    environment=ENVIRONMENT,  # Will be "dev", "staging", or "production"
    data_location=DATA_LOCATION,  # Will be "US" or "EU"
)

# Set agent configuration
set_agent(
    name="production-chatbot",
    version=VERSION,  # Your deployment version
    description=f"Production chatbot running in {ENVIRONMENT} environment",
)

def main():
    print(f"Starting run in {ENVIRONMENT} environment...")

    # Start a run
    run = start_run(
        name="user-interaction",
        meta={
            "environment": ENVIRONMENT,
            "data_location": DATA_LOCATION,
            "version": VERSION,
        }
    )

    # Log a step
    log_step(
        run=run,
        name="process_user_input",
        attrs={
            "model": "gpt-4",
            "environment": ENVIRONMENT,
        },
        events=[
            {
                "type": "user_input",
                "content": "Hello, I need help with my account",
            }
        ]
    )

    # End the run
    end_run(run)
    print(f"Run completed in {ENVIRONMENT} environment: {run.id}")


if __name__ == "__main__":
    main()