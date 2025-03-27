import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Define a team.
assistant_agent = AssistantAgent(
    name="assistant_agent",
    system_message="You are a helpful assistant",
    model_client=OpenAIChatCompletionClient(
        model="gpt-4o-mini",
    ),
)
agent_team = RoundRobinGroupChat(
    [assistant_agent], termination_condition=MaxMessageTermination(max_messages=2)
)

# Run the team and stream messages to the console.
stream = agent_team.run_stream(
    task="Write a beautiful poem 3-line about lake tangayika"
)

# Use asyncio.run(...) when running in a script.
asyncio.run(Console(stream))

# Save the state of the agent team.
team_state = asyncio.run(agent_team.save_state())

asyncio.run(agent_team.reset())
stream = agent_team.run_stream(task="What was the last line of the poem you wrote?")
print(team_state)

# can't accomplish this as there is no reference to the previous run.
# asyncio.run(Console(stream))

# Load team state.
# asyncio.run(agent_team.load_state(team_state))
# stream = agent_team.run_stream(task="What was the last line of the poem you wrote?")
# asyncio.run(Console(stream))
