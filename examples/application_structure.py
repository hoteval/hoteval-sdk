"""Example: Real Application Structure with Multiple Agents.

This example shows how to structure a real application with multiple agents
using the best practice approach for strong coupling and version management.
"""

import os
from typing import Any, Dict, Optional

from hoteval import configure, create_agent


class AgentManager:
    """Manages multiple agents in an application."""

    def __init__(self):
        """Initialize the agent manager."""
        # Configure global settings
        configure(
            api_key=os.getenv("HOTEVAL_API_KEY"),
            base_url=os.getenv("HOTEVAL_BASE_URL", "https://api.hoteval.com"),
            environment=os.getenv("ENVIRONMENT", "dev"),
            data_location=os.getenv("DATA_LOCATION", "EU"),
        )

        # Initialize agents
        self.agents = self._initialize_agents()

    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize all agents used in the application."""
        return {
            "support": create_agent(
                name="customer-support-chatbot",
                version=os.getenv("SUPPORT_BOT_VERSION", "2.1.0"),
                description="AI chatbot for customer support"
            ),
            "analytics": create_agent(
                name="data-analytics-engine",
                version=os.getenv("ANALYTICS_VERSION", "1.5.2"),
                description="Data processing and analytics engine"
            ),
            "recommendations": create_agent(
                name="product-recommendation-engine",
                version=os.getenv("RECOMMENDATION_VERSION", "3.0.1"),
                description="Product recommendation system"
            ),
            "fraud_detection": create_agent(
                name="fraud-detection-system",
                version=os.getenv("FRAUD_DETECTION_VERSION", "1.2.0"),
                description="Fraud detection and prevention system"
            ),
        }

    def get_agent(self, agent_type: str):
        """Get an agent by type."""
        if agent_type not in self.agents:
            raise ValueError(f"Unknown agent type: {agent_type}")
        return self.agents[agent_type]

    def upgrade_agent(self, agent_type: str, new_version: str, description: Optional[str] = None):
        """Upgrade an agent to a new version."""
        if agent_type not in self.agents:
            raise ValueError(f"Unknown agent type: {agent_type}")

        # Get the current agent to copy its name
        current_agent = self.agents[agent_type]

        # Create new agent with updated version
        self.agents[agent_type] = create_agent(
            name=current_agent.name,
            version=new_version,
            description=description or current_agent.description,
        )

        print(f"Upgraded {agent_type} agent to version {new_version}")


class CustomerSupportService:
    """Service for handling customer support."""

    def __init__(self, agent_manager: AgentManager):
        self.agent_manager = agent_manager
        self.support_agent = agent_manager.get_agent("support")

    def handle_inquiry(self, customer_id: str, inquiry: str, inquiry_type: str):
        """Handle a customer support inquiry."""
        with self.support_agent.run(
            name=f"support-{customer_id}",
            meta={
                "customer_id": customer_id,
                "inquiry_type": inquiry_type,
                "timestamp": "2024-01-15T10:30:00Z"
            }
        ) as run:

            # Log the inquiry
            self.support_agent.log_step(
                run=run,
                name="receive_inquiry",
                attrs={"model": "gpt-4", "temperature": 0.7},
                events=[
                    {"type": "user_input", "content": inquiry}
                ]
            )

            # Process the inquiry (simulated)
            response = self._process_inquiry(inquiry, inquiry_type)

            # Log the response
            self.support_agent.log_step(
                run=run,
                name="generate_response",
                attrs={"response_length": len(response)},
                events=[
                    {"type": "response", "content": response}
                ]
            )

            return response

    def _process_inquiry(self, inquiry: str, inquiry_type: str) -> str:
        """Process the inquiry and generate a response."""
        # Simulated processing
        if inquiry_type == "billing":
            return "I can help you with your billing question. Please provide your account number."
        elif inquiry_type == "technical":
            return "I'll help you with the technical issue. Can you describe the problem in detail?"
        else:
            return "Thank you for your inquiry. How can I assist you today?"


class AnalyticsService:
    """Service for data analytics."""

    def __init__(self, agent_manager: AgentManager):
        self.agent_manager = agent_manager
        self.analytics_agent = agent_manager.get_agent("analytics")

    def analyze_sales_data(self, dataset: str, analysis_type: str):
        """Analyze sales data."""
        with self.analytics_agent.run(
            name=f"sales-analysis-{dataset}",
            meta={
                "dataset": dataset,
                "analysis_type": analysis_type,
                "data_points": 10000
            }
        ) as run:

            # Load data
            self.analytics_agent.log_step(
                run=run,
                name="load_data",
                attrs={"dataset_size": "10MB", "format": "CSV"},
                events=[
                    {"type": "data_loaded", "content": f"Loaded {dataset}"}
                ]
            )

            # Process data
            self.analytics_agent.log_step(
                run=run,
                name="process_data",
                attrs={"algorithm": "linear_regression", "features": 15},
                events=[
                    {"type": "processing_start", "content": "Started data processing"},
                    {"type": "processing_complete", "content": "Data processing completed"}
                ]
            )

            # Generate insights
            insights = self._generate_insights(analysis_type)

            self.analytics_agent.log_step(
                run=run,
                name="generate_insights",
                attrs={"insight_count": len(insights)},
                events=[
                    {"type": "insights_generated", "content": str(insights)}
                ]
            )

            return insights

    def _generate_insights(self, analysis_type: str) -> list:
        """Generate insights from the analysis."""
        if analysis_type == "trends":
            return ["Sales increased 15% this quarter", "Peak sales on weekends"]
        elif analysis_type == "segments":
            return ["Premium customers drive 60% of revenue", "Young adults prefer mobile"]
        else:
            return ["General insights available"]


def main():
    """Main application example."""
    # Initialize agent manager
    agent_manager = AgentManager()

    # Create services
    support_service = CustomerSupportService(agent_manager)
    analytics_service = AnalyticsService(agent_manager)

    # Handle customer support
    print("Handling customer support...")
    response = support_service.handle_inquiry(
        customer_id="cust_123",
        inquiry="I have a billing question about my last invoice",
        inquiry_type="billing"
    )
    print(f"Support response: {response}")

    # Analyze data
    print("\nAnalyzing sales data...")
    insights = analytics_service.analyze_sales_data(
        dataset="sales_2024_q1",
        analysis_type="trends"
    )
    print(f"Analytics insights: {insights}")

    # Upgrade an agent (simulating a deployment)
    print("\nUpgrading support agent...")
    agent_manager.upgrade_agent(
        agent_type="support",
        new_version="2.2.0",
        description="Updated support bot with improved response quality"
    )

    # Use the upgraded agent
    print("Using upgraded support agent...")
    support_service = CustomerSupportService(agent_manager)
    response = support_service.handle_inquiry(
        customer_id="cust_456",
        inquiry="I need help with a technical issue",
        inquiry_type="technical"
    )
    print(f"Upgraded support response: {response}")


if __name__ == "__main__":
    main()