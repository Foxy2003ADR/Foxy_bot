import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5-mini"
)


def openai_config_ok() -> bool:
    return bool(OPENAI_API_KEY)