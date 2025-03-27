import asyncio
import json

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

team_state = {
    "type": "TeamState",
    "version": "1.0.0",
    "agent_states": {
        "assistant_agent": {
            "type": "ChatAgentContainerState",
            "version": "1.0.0",
            "agent_state": {
                "type": "AssistantAgentState",
                "version": "1.0.0",
                "llm_context": {
                    "messages": [
                        {
                            "content": "Write a beautiful poem 3-line about lake tangayika",
                            "source": "user",
                            "type": "UserMessage",
                        },
                        {
                            "content": "In Tanganyika's embrace, where waters gleam,  \nMountains whisper secrets to the tranquil dream,  \nNature's canvas painted in a timeless theme.  ",
                            "thought": None,
                            "source": "assistant_agent",
                            "type": "AssistantMessage",
                        },
                    ]
                },
            },
            "message_buffer": [],
        },
        "RoundRobinGroupChatManager": {
            "type": "RoundRobinManagerState",
            "version": "1.0.0",
            "message_thread": [
                {
                    "source": "user",
                    "models_usage": None,
                    "metadata": {},
                    "content": "Write a beautiful poem 3-line about lake tangayika",
                    "type": "TextMessage",
                },
                {
                    "source": "assistant_agent",
                    "models_usage": {"prompt_tokens": 29, "completion_tokens": 33},
                    "metadata": {},
                    "content": "In Tanganyika's embrace, where waters gleam,  \nMountains whisper secrets to the tranquil dream,  \nNature's canvas painted in a timeless theme.  ",
                    "type": "TextMessage",
                },
            ],
            "current_turn": 0,
            "next_speaker_index": 0,
        },
    },
}

assistant_agent = AssistantAgent(
    name="assistant_agent",
    system_message="You are a helpful assistant",
    model_client=OpenAIChatCompletionClient(
        model="gpt-4o-mini",
    ),
)

## save state to disk
with open("coding/team_state.json", "w") as f:
    json.dump(team_state, f)

## load state from disk
with open("coding/team_state.json", "r") as f:
    team_state = json.load(f)

new_agent_team = RoundRobinGroupChat(
    [assistant_agent], termination_condition=MaxMessageTermination(max_messages=2)
)
asyncio.run(new_agent_team.load_state(team_state))
stream = new_agent_team.run_stream(task="What was the last line of the poem you wrote?")
asyncio.run(Console(stream))
