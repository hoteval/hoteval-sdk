"""Example: Best Practice - Using Agent instances for strong coupling.

This example shows the recommended approach for managing multiple agents
with strong coupling between agents and their runs.
"""

import os

from hoteval import configure, create_agent

# Configure global settings once
configure(
    api_key=os.getenv("HOTEVAL_API_KEY"),
    base_url=os.getenv("HOTEVAL_BASE_URL", "https://api.hoteval.com"),
    environment=os.getenv("ENVIRONMENT", "dev"),
    data_location=os.getenv("DATA_LOCATION", "EU"),
)

# Create agent instances (strong coupling)
support_bot = create_agent(
    name="customer-support-chatbot",
    version="2.1.0",
    description="AI chatbot for customer support inquiries"
)

analytics_engine = create_agent(
    name="data-analytics-agent",
    version="1.5.2",
    description="Agent for processing and analyzing data"
)

recommendation_engine = create_agent(
    name="product-recommendation-engine",
    version="3.0.1",
    description="ML-powered product recommendation system"
)


def handle_customer_support():
    """Handle customer support with the support bot agent."""
    # Method 1: Manual run management
    run = support_bot.start_run(
        name="support-chat-123",
        meta={"customer_id": "cust_456", "inquiry_type": "billing"}
    )

    support_bot.log_step(
        run=run,
        name="process_inquiry",
        attrs={"model": "gpt-4", "temperature": 0.7},
        events=[
            {"type": "user_input", "content": "I have a billing question"},
            {"type": "response", "content": "I'd be happy to help with your billing question..."}
        ]
    )

    support_bot.end_run(run)
    print(f"Support run completed: {run.id}")


def process_analytics():
    """Process analytics with the analytics engine agent."""
    # Method 2: Context manager (recommended for complex workflows)
    with analytics_engine.run(
        name="analytics-job-789",
        meta={"dataset": "sales_data_2024", "analysis_type": "trends"}
    ) as run:

        analytics_engine.log_step(
            run=run,
            name="data_processing",
            attrs={"algorithm": "linear_regression", "data_points": 10000},
            events=[
                {"type": "data_loaded", "content": "Loaded 10,000 sales records"},
                {"type": "analysis_complete", "content": "Trend analysis completed"}
            ]
        )

        # Run automatically ends when exiting the context
        print(f"Analytics run completed: {run.id}")


def generate_recommendations():
    """Generate recommendations with the recommendation engine agent."""
    with recommendation_engine.run(
        name="recommendation-456",
        meta={"user_id": "user_789", "category": "electronics"}
    ) as run:

        recommendation_engine.log_step(
            run=run,
            name="generate_recommendations",
            attrs={"model": "collaborative_filtering", "top_k": 5},
            events=[
                {"type": "user_profile", "content": "User interested in electronics"},
                {"type": "recommendations", "content": "Generated 5 product recommendations"}
            ]
        )

        print(f"Recommendation run completed: {run.id}")


def version_upgrade_example():
    """Example of handling version upgrades."""
    # Create a new version of the support bot
    support_bot_v2 = create_agent(
        name="customer-support-chatbot",  # Same name, different version
        version="2.2.0",  # New version
        description="Updated support bot with improved responses"
    )

    # Use the new version
    with support_bot_v2.run(name="support-chat-v2") as run:
        support_bot_v2.log_step(
            run=run,
            name="process_inquiry_v2",
            attrs={"model": "gpt-4-turbo", "temperature": 0.5},
            events=[
                {"type": "user_input", "content": "I need help with my order"},
                {"type": "response", "content": "I can help you with your order..."}
            ]
        )

        print(f"Support v2 run completed: {run.id}")


def main():
    """Run examples with strongly-coupled agents."""
    print("Running best practice agent examples...")

    # Each agent is strongly coupled to its runs
    handle_customer_support()
    process_analytics()
    generate_recommendations()

    # Version upgrade example
    version_upgrade_example()

    print("All runs completed!")


if __name__ == "__main__":
    main()