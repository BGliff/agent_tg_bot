from langchain_openai import ChatOpenAI

from config import AGENT_CONFIG


llm = ChatOpenAI(
  api_key=AGENT_CONFIG.OPENROUTER_API_KEY,
  base_url=AGENT_CONFIG.OPENROUTER_BASE_URL,
  model=AGENT_CONFIG.OPENROUTER_MODEL_NAME,
)
