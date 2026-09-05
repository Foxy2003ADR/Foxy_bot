from openai import AsyncOpenAI

from .config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
)


_client = None


def get_openai_client():
    global _client

    if not OPENAI_API_KEY:
        raise RuntimeError(
            "Falta OPENAI_API_KEY."
        )

    if _client is None:
        _client = AsyncOpenAI(
            api_key=OPENAI_API_KEY
        )

    return _client


async def ask_openai(prompt: str) -> str:
    client = get_openai_client()

    response = await client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
    )

    return response.output_text