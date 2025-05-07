# MCP Search

MCP Search is a Python project that provides a simple search interface for querying documentation.

## Installation

Can be installed with uv
```(bash)
  uv pip install "git+https://github.com/Alviner/mcp-search@main"
```


## Configuration

MCP Search can be configured using the following environment variables:
```(bash)
usage: mcp-search [-h] --docs-path DOCS_PATH [--cache-folder CACHE_FOLDER] [--embedding-model EMBEDDING_MODEL] [--chunk-size CHUNK_SIZE] [--chunk-overlap CHUNK_OVERLAP]
                  [--logs-format {color,disabled,journald,json,plain,rich,rich_tb,stream,syslog}] [--logs-level {critical,debug,error,info,notset,warning}] --openai-api-key
                  OPENAI_API_KEY [--openai-base-url OPENAI_BASE_URL] [--openai-model OPENAI_MODEL]

options:
  -h, --help            show this help message and exit
  --docs-path DOCS_PATH
                        [ENV: MCP_DOCS_PATH]
  --cache-folder CACHE_FOLDER
                        (default: /tmp/mcp-search) [ENV: MCP_CACHE_FOLDER]
  --embedding-model EMBEDDING_MODEL
                        (default: sentence-transformers/all-MiniLM-L6-v2) [ENV: MCP_EMBEDDING_MODEL]
  --chunk-size CHUNK_SIZE
                        (default: 5096) [ENV: MCP_CHUNK_SIZE]
  --chunk-overlap CHUNK_OVERLAP
                        (default: 1024) [ENV: MCP_CHUNK_OVERLAP]

Logs options:
  --logs-format {color,disabled,journald,json,plain,rich,rich_tb,stream,syslog}
                        (default: color) [ENV: MCP_LOGS_FORMAT]
  --logs-level {critical,debug,error,info,notset,warning}
                        (default: info) [ENV: MCP_LOGS_LEVEL]

OpenAI options:
  --openai-api-key OPENAI_API_KEY
                        [ENV: MCP_OPENAI_API_KEY]
  --openai-base-url OPENAI_BASE_URL
                        (default: https://api.studio.nebius.com/v1/) [ENV: MCP_OPENAI_BASE_URL]
  --openai-model OPENAI_MODEL
                        (default: meta-llama/Meta-Llama-3.1-70B-Instruct-fast) [ENV: MCP_OPENAI_MODEL]
```
## Zed Configuration

```(json)
{
"context_servers": {
    "mcp-search": {
      "command": {
        "path": "mcp-search",
        "env": {
          "MCP_OPENAI_API_KEY": "<OPENAI_API_KEY>"
        },
        "args": [
          "--docs-path",
          "<DOCS_PATH>"
        ]
      }
    }
  }
}
```

## Contributing

To contribute to MCP Search, please fork the repository and submit a pull request with your changes.

## License

MCP Search is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).
