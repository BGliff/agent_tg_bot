from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from agent.llm_connection import llm


async def analyze(html: str) -> str:
    chain = (
            ChatPromptTemplate.from_template(
                "Проанализируй эту страницу и расскажи кратко о компании: {html}"
            )
            | llm
            | StrOutputParser()
    )
    return await chain.ainvoke({"html": html})


async def ask_llm(query: str) -> str:
    chain = (
            ChatPromptTemplate.from_template("{query}")
            | llm
            | StrOutputParser()
    )
    return await chain.ainvoke({"query": query})
