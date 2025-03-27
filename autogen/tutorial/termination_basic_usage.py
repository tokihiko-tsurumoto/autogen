import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    temperature=1,
    # api_key="sk-...", # Optional if you have an OPENAI_API_KEY env variable set.
)

# Create the primary agent.
primary_agent = AssistantAgent(
    "primary",
    model_client=model_client,
    system_message="You are a helpful AI assistant.",
)

# Create the critic agent.
critic_agent = AssistantAgent(
    "critic",
    model_client=model_client,
    system_message="Provide constructive feedback for every message. Respond with 'APPROVE' to when your feedbacks are addressed.",
)

max_msg_termination = MaxMessageTermination(max_messages=5)
round_robin_team = RoundRobinGroupChat(
    [primary_agent, critic_agent], termination_condition=max_msg_termination
)

# Use asyncio.run(...) if you are running this script as a standalone script.
asyncio.run(
    Console(
        round_robin_team.run_stream(
            task="今後どのようなAIが流行るか考えてください。"
        )
    )
)
