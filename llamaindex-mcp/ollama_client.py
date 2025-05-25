import nest_asyncio
from llama_index.core import Settings
from llama_index.core.agent.workflow import (FunctionAgent, ToolCall,
                                             ToolCallResult)
from llama_index.core.workflow import Context
from llama_index.llms.ollama import Ollama
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec

# Step 1: Apply nest_asyncio
nest_asyncio.apply()

# Step 2: Setup a local LLM
llm = Ollama(model="llama3.2", request_timeout=120.0)
Settings.llm = llm

# Step 3: Initialize the MCP client and build the agent
mcp_client = BasicMCPClient("http://127.0.0.1:8000/sse")
mcp_tools = McpToolSpec(client=mcp_client)  # you can also pass list of allowed tools

tools = None
async def list_tools():
    global tools
    tools = await mcp_tools.to_tool_list_async()
    for tool in tools:
        print(tool.metadata.name, tool.metadata.description)

# Step 4: Define the system prompt
SYSTEM_PROMPT = """\
You are an AI assistant for Tool Calling.

Before you help a user, you need to work with tools to interact with Our Database.

Always use the available tools to answer user questions. Do not make up information or answer from memory—only use the results returned by the tools.
"""

# Step 5: Helper function: get_agent()
async def get_agent(tools: McpToolSpec):
    tools = await tools.to_tool_list_async()
    agent = FunctionAgent(
        name="Agent",
        description="An agent that can work with Our Database software.",
        tools=tools,
        #llm=OpenAI(model="gpt-4"),
        llm=Settings.llm,
        system_prompt=SYSTEM_PROMPT,
    )
    return agent

# Step 6: Helper function: handle_user_message()
async def handle_user_message(
    message_content: str,
    agent: FunctionAgent,
    agent_context: Context,
    verbose: bool = False,
):
    handler = agent.run(message_content, ctx=agent_context)
    async for event in handler.stream_events():
        if verbose and isinstance(event, ToolCall):
            print(f"Calling tool {event.tool_name} with kwargs {event.tool_kwargs}")
            # Print the actual tool call for LLM quality assessment
            print(f"[MCP AGENT TOOL CALL] Tool: {event.tool_name}, Arguments: {event.tool_kwargs}")
        elif verbose and isinstance(event, ToolCallResult):
            print(f"Tool {event.tool_name} returned {event.tool_output}")
    response = await handler
    return str(response)

# Step 7: Initialize the MCP client and build the agent
async def main():
    mcp_client = BasicMCPClient("http://127.0.0.1:8000/sse")
    mcp_tool = McpToolSpec(client=mcp_client)
    agent = await get_agent(mcp_tool)
    agent_context = Context(agent)
    while True:
        user_input = input("Enter your message: (type exit to quit) ")
        if user_input == "exit":
            break
        print("User: ", user_input)
        response = await handle_user_message(user_input, agent, agent_context, verbose=True)
        print("Agent: ", response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
