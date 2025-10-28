from agent import tools
from agent.llm_connection import llm
from agent.chains import ask_llm
from exceptions import BaseBotError


llm_with_tools = llm.bind_tools(
    [
        tools.multiply,
        tools.add,
        tools.get_page,
        tools.get_weather,
        tools.fallback,
    ]
)


async def main_fallback(query: str) -> str:
    return await ask_llm(query)


async def agent_main(message: str) -> str:
    response = await llm_with_tools.ainvoke(message)
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        try:
            return str(
                await getattr(
                    tools, tool_call.get("name", "fallback")
                ).ainvoke(tool_call["args"])
            )
        except BaseBotError as err:
            return str(err)
    else:
        return await main_fallback(message)

