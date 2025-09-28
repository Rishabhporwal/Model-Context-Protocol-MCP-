import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import asyncio

load_dotenv()

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

async def main():
    """
        Summary
    """

    client = MultiServerMCPClient(
        {
            "calculator": {
                "command": "python",
                "args": ["calculator.py"],
                "transport": "stdio"
            },
            "weather":  {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http"
            }
        }
    )

    tools = await client.get_tools()

    model = ChatGroq(model="deepseek-r1-distill-llama-70b")

    agent = create_react_agent(model, tools)

    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in bangaluru?"}]}
        # {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
    )

    print(response['messages'][-1].content)


asyncio.run(main())