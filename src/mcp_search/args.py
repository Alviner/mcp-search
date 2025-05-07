import argclass
from aiomisc_log import LogFormat, LogLevel
from pathlib import Path

class LogsGroup(argclass.Group):
    format: LogFormat = argclass.EnumArgument(LogFormat, default="color")
    level: LogLevel = argclass.EnumArgument(LogLevel, default="info")

class OpenAIGroup(argclass.Group):
    api_key: str = argclass.Secret(required=True)
    base_url: str = "https://api.studio.nebius.com/v1/"
    model: str = "meta-llama/Meta-Llama-3.1-70B-Instruct-fast"

class Args(argclass.Parser):
    logs: LogsGroup = LogsGroup(title="Logs options")

    docs_path: Path
    cache_folder: Path = Path("/tmp/mcp-search")
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    openai: OpenAIGroup = OpenAIGroup(title="OpenAI options")

    chunk_size: int = 5096
    chunk_overlap: int = 1024
