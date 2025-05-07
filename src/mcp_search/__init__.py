import logging

from aiomisc import entrypoint
from aiomisc_log import LogLevel, LogFormat, basic_config

from mcp_search.server import MCPServer
from mcp_search.deps import configure_dependecies
from mcp_search.args import Args

log = logging.getLogger(__name__)

def main() -> None:
    basic_config(level=LogLevel.info, format=LogFormat.color)

    args = Args(
        auto_env_var_prefix="MCP_"
    )
    args = args.parse_args()

    log.info("initializing MCP Search")
    configure_dependecies(args)

    logs = args.logs
    with entrypoint(MCPServer(), log_level=logs.level, log_format=logs.format) as loop:
        loop.run_forever()


if __name__ == "__main__":
    main()
