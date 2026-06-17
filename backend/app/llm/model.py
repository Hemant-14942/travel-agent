import os

from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel

from app.logger import get_logger

log = get_logger(__name__)


def get_llm() -> BaseChatModel:
    # Re-read .env on every call so that changing LLM_PROVIDER=groq/gemini
    # takes effect immediately without restarting the server.
    load_dotenv(override=True)

    provider = os.getenv("LLM_PROVIDER", "groq").strip().lower()

    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("LLM_PROVIDER=gemini but GEMINI_API_KEY is not set in .env")

        log.info("LLM provider: Gemini (gemini-2.5-flash)")
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3,
            google_api_key=api_key,
        )

    # Default → Groq
    from langchain_groq import ChatGroq

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("LLM_PROVIDER=groq but GROQ_API_KEY is not set in .env")

    log.info("LLM provider: Groq (llama-3.1-8b-instant)")
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3,
        api_key=api_key,
    )
