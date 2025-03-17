import asyncio
import os
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

# Define a model client. You can use other model clients that implement the
# `ChatCompletionClient` interface.
model_client = OpenAIChatCompletionClient(
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY"),
)


def get_city_from_command_line() -> str:
    """Get the city from the command line."""
    return input("Enter the city: ")


# Define a simple function tool that the agent can use.  For this example, we
# use a fake weather tool for demonstration purposes.
async def weather_forcast_tool(city: str) -> str:
    """Get the weather for a given city."""
    return f"The weather sunny in {city}."


async def new_zealand_weather_forecast_tool(city: str) -> str:
    """Get the weather for a given city."""
    return f"The weather is sunny in {city}. But it will rain soon!"


# Define an AssistantAgent with the model, tool, system message, and reflection
# enabled.  The system message instructs the agent via natural language.
weather_forcaster = AssistantAgent(
    name="weather_agent",
    model_client=model_client,
    tools=[weather_forcast_tool, new_zealand_weather_forecast_tool],
    system_message="""You forcast the whether and use different tools based on
    whether the city is in New Zealand or not.""",
    reflect_on_tool_use=True,
    model_client_stream=True,  # Enable streaming tokens from the model client.
)

city: str = get_city_from_command_line()


# Run the agent and stream the messages to the console.
async def main() -> None:
    """Use the approiate tool to get the weather for a city.

    The agent will use different tools based on whether the city is in New Zealand or not.
    """
    await Console(weather_forcaster.run_stream(task=f"What is the weather in {city}?"))


# NOTE: if running this inside a Python script you'll need to use asyncio.run(main()).
if __name__ == "__main__":
    asyncio.run(main())
