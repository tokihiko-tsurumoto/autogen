import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient

assistant_agent = AssistantAgent(
    name="assistant_agent",
    system_message="You are a helpful assistant",
    model_client=OpenAIChatCompletionClient(
        model="gpt-4o-2024-08-06",
        # api_key="YOUR_API_KEY",
    ),
)

# Use asyncio.run(...) when running in a script.
response = asyncio.run(
    assistant_agent.on_messages(
        [TextMessage(content="Write a 3 line poem on lake tangayika", source="user")],
        CancellationToken(),
    )
)
print(response.chat_message.content)

agent_state = asyncio.run(assistant_agent.save_state())
print(agent_state)

new_assistant_agent = AssistantAgent(
    name="assistant_agent",
    system_message="You are a helpful assistant",
    model_client=OpenAIChatCompletionClient(
        model="gpt-4o-mini",
    ),
)
asyncio.run(new_assistant_agent.load_state(agent_state))

# Use asyncio.run(...) when running in a script.
response = asyncio.run(
    new_assistant_agent.on_messages(
        [
            TextMessage(
                content="What was the last line of the previous poem you wrote",
                source="user",
            )
        ],
        CancellationToken(),
    )
)
print(response.chat_message.content)
