from collections.abc import AsyncIterable
from pydantic_ai import Agent, RunContext
from pydantic_ai.mcp import MCPServerStreamableHTTP
from pydantic_ai.messages import AgentStreamEvent, FunctionToolCallEvent, FunctionToolResultEvent
import json
import asyncio


async def print_tool_events(ctx: RunContext, stream: AsyncIterable[AgentStreamEvent]):
    async for ev in stream:
        if isinstance(ev, FunctionToolCallEvent):
            print(f"\n[tool ▶] {ev.part.tool_name} args={json.dumps(ev.part.args)}")


async def main():

    server = MCPServerStreamableHTTP('http://localhost:8002/v1/leads/mcp/')
    agent = Agent('openai:gpt-4.1-mini', toolsets=[server])
    message_history = []
    while True:
        user_input = input("User: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Exiting...")
            break
        response = await agent.run(user_input, message_history=message_history, event_stream_handler=print_tool_events)
        print(f"Agent: {response.output}")
        message_history = response.all_messages()


if __name__ == '__main__':
    asyncio.run(main())
