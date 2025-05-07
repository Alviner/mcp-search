# MCP Search

MCP Search is a Python project that provides a simple search interface for querying documentation.

## Configuration

MCP Search can be configured using the following environment variables:
```(bash)
options:
  -h, --help            show this help message and exit
  --docs-path DOCS_PATH
  --cache-folder CACHE_FOLDER
                        (default: /tmp/mcp-search)
  --embedding-model EMBEDDING_MODEL
                        (default: sentence-transformers/all-MiniLM-L6-v2)
  --chunk-size CHUNK_SIZE
                        (default: 5096)
  --chunk-overlap CHUNK_OVERLAP
                        (default: 1024)

Logs options:
  --logs-format {color,disabled,journald,json,plain,rich,rich_tb,stream,syslog}
                        (default: color)
  --logs-level {critical,debug,error,info,notset,warning}
                        (default: info)

OpenAI options:
  --openai-api-key OPENAI_API_KEY
  --openai-base-url OPENAI_BASE_URL
                        (default: https://api.studio.nebius.com/v1/)
  --openai-model OPENAI_MODEL
                        (default: meta-llama/Meta-Llama-3.1-70B-Instruct-fast)
```
## Contributing

To contribute to MCP Search, please fork the repository and submit a pull request with your changes.

## License

MCP Search is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).
