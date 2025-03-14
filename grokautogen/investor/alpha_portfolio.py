import asyncio
import os
import sys
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

load_dotenv()

model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY")
)

investment_advisor = AssistantAgent(
    name="investment_advisor",
    model_client=model_client,
    system_message="""
        You are the face of the investment team.

        You look for investment opportunities based on a client's requirements.
        You make seven recommendations. Your recommendations must contain
        relevan tickers. You depend on the Portfolio Manger to cut down the
        investments to four.
    """.strip(),
)


async def lookup_investment_profile(client_name: str):
    try:
        with open(f"data/investor/Profile{client_name}.md") as f:
            investment_profile = f.read()
        return investment_profile
    except [FileNotFoundError, IOError]:
        return "This user does not exist. Use a standard medium riks profile."


portfolio_helper = AssistantAgent(
    name="portfolio_helper",
    model_client=model_client,
    tools=[
        lookup_investment_profile,
    ],
    system_message="""
        You are the investment team's back office support.
    
        You help the Portfolio Manager understand what the client's investment
        profile looks like.
    """.strip(),
)

portfolio_manager = AssistantAgent(
    name="portfolio_manager",
    model_client=model_client,
    system_message="""
        You are the Portfolio Manager.

        You verify that a client's investments fit in with their investment
        profile. You make investment recommendations based on the input of the
        Investment Advisor and Portfolio Helper. You reposed with 'APPROVE' if
        the investment is suitable for the client's portfolio.
    """.strip(),
)

termination_condition = TextMentionTermination("APPROVE")

investment_team = RoundRobinGroupChat(
    [
        investment_advisor,
        portfolio_helper,
        portfolio_manager,
    ],
    termination_condition=termination_condition,
)


async def verbose_run(task):
    async for message in investment_team.run_stream(task=task):
        if isinstance(message, TaskResult):
            print(f"{message.stop_reason=}")
        else:
            print(f"{message=}")


async def quiet_run(task) -> None:
    await Console(investment_team.run_stream(task=task))


if __name__ == "__main__":
    name = input("Hello. What is your name? ")
    investment = input("What investment are you considering? ")
    task = f"{name} is considering investing in {investment}."
    if "--verbose" in sys.argv:
        sys.argv.remove("--verbose")
        asyncio.run(verbose_run(task))
    else:
        asyncio.run(quiet_run(task))
