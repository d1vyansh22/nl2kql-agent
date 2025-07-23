from functools import lru_cache
from langchain_google_genai import ChatGoogleGenerativeAI
from .config import GOOGLE_API_KEY


@lru_cache(maxsize=3)
def get_llm(model: str = "gemini-pro", temperature: float = 0.0):
    """Singleton Gemini client; caching avoids multiple sockets."""
    print(f"--- Initializing Gemini LLM (temperature={temperature}) ---")
    return ChatGoogleGenerativeAI(model=model, temperature=temperature, google_api_key=GOOGLE_API_KEY)
