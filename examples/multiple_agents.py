"""Example: Using multiple agents with shared global configuration.

This example shows how to configure the SDK once with global settings,
then switch between different agents for different runs.
"""

import os

from hoteval import configure, end_run, log_step, set_agent, start_run

# Configure global settings once (shared across all agents)
configure(
    api_key=os.getenv("HOTEVAL_API_KEY"),
    base_url=os.getenv("HOTEVAL_BASE_URL", "https://api.hoteval.com"),
    environment=os.getenv("ENVIRONMENT", "dev"),  # Shared environment
    data_location=os.getenv("DATA_LOCATION", "EU"),  # Shared data location
)

def run_chatbot_agent():
    """Run with chatbot agent configuration."""
    # Set agent-specific configuration
    set_agent(
        name="customer-support-chatbot",
        version="2.1.0",
        description="AI chatbot for customer support inquiries"
    )

    # Start a run with this agent
    run = start_run(
        name="support-chat-123",
        meta={"customer_id": "cust_456", "inquiry_type": "billing"}
    )

    log_step(
        run=run,
        name="process_inquiry",
        attrs={"model": "gpt-4", "temperature": 0.7},
        events=[
            {"type": "user_input", "content": "I have a billing question"},
            {"type": "response", "content": "I'd be happy to help with your billing question..."}
        ]
    )

    end_run(run)
    print(f"Chatbot run completed: {run.id}")


def run_analytics_agent():
    """Run with analytics agent configuration."""
    # Switch to different agent
    set_agent(
        name="data-analytics-agent",
        version="1.5.2",
        description="Agent for processing and analyzing data"
    )

    # Start a run with this agent
    run = start_run(
        name="analytics-job-789",
        meta={"dataset": "sales_data_2024", "analysis_type": "trends"}
    )

    log_step(
        run=run,
        name="data_processing",
        attrs={"algorithm": "linear_regression", "data_points": 10000},
        events=[
            {"type": "data_loaded", "content": "Loaded 10,000 sales records"},
            {"type": "analysis_complete", "content": "Trend analysis completed"}
        ]
    )

    end_run(run)
    print(f"Analytics run completed: {run.id}")


def run_recommendation_agent():
    """Run with recommendation agent configuration."""
    # Switch to another agent
    set_agent(
        name="product-recommendation-engine",
        version="3.0.1",
        description="ML-powered product recommendation system"
    )

    # Start a run with this agent
    run = start_run(
        name="recommendation-456",
        meta={"user_id": "user_789", "category": "electronics"}
    )

    log_step(
        run=run,
        name="generate_recommendations",
        attrs={"model": "collaborative_filtering", "top_k": 5},
        events=[
            {"type": "user_profile", "content": "User interested in electronics"},
            {"type": "recommendations", "content": "Generated 5 product recommendations"}
        ]
    )

    end_run(run)
    print(f"Recommendation run completed: {run.id}")


def main():
    """Run examples with different agents."""
    print("Running multiple agents with shared global configuration...")

    # Run with different agents
    run_chatbot_agent()
    run_analytics_agent()
    run_recommendation_agent()

    print("All runs completed!")


if __name__ == "__main__":
    main()