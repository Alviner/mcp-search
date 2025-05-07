import logging

from aiomisc import Service
from mcp.server import Server as MCPApp
from mcp.server.stdio import stdio_server
from mcp.shared.exceptions import McpError
from mcp.types import (
    ErrorData,
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    Tool,
    INVALID_PARAMS,
    TextContent,
)
from pydantic import BaseModel
from langchain_core.runnables import Runnable

log = logging.getLogger(__name__)

class DocsQuery(BaseModel):
    q: str

class MCPServer(Service):
    __dependencies__ = ('chain',)

    chain: Runnable

    async def get_application(self) -> MCPApp:
        return MCPApp("mcp-search")

    async def start(self):
        log.info("Starting MCP Search server")
        app = await self.get_application()

        app.list_prompts()(self.list_prompts)
        app.get_prompt()(self.get_prompt)
        app.list_tools()(self.list_tools)
        app.call_tool()(self.call_tool)

        options  = app.create_initialization_options()
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, options, raise_exceptions=True)

    async def list_prompts(self) -> list[Prompt]:
        return [
            Prompt(
                name="docs",
                description="Query to a docs",
                arguments=[
                    PromptArgument(
                        name="q", description="Query to a docs", required=True
                    )
                ],
            )
        ]

    async def list_tools(self) -> list[Tool]:
        return [
            Tool(
                name="docs",
                description="Query to a docs",
                inputSchema=DocsQuery.schema(),
            ),
        ]

    async def get_prompt(self, name: str, arguments: dict | None) -> GetPromptResult:
        try:
           query = DocsQuery.parse_obj(arguments)
        except Exception as e:
            raise McpError(ErrorData(code=INVALID_PARAMS, message=str(e)))

        try:
            result = await self.chain.ainvoke({"input": query.q})
        except McpError as e:
            return GetPromptResult(
                description=f"Failed to query {query}",
                messages=[
                    PromptMessage(
                        role="user",
                        content=TextContent(type="text", text=str(e)),
                    )
                ],
            )
        return GetPromptResult(
            description=result["input"],
            messages=[
                PromptMessage(
                    role="user", content=TextContent(type="text", text=result["answer"])
                )
            ],
        )
    async def call_tool(self, name: str, arguments: dict) -> list[TextContent]:
        if name == "docs":
            return await self.call_docs(arguments)
        raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Unknown tool {name}"))

    async def call_docs(self, arguments: dict) -> list[TextContent]:
        try:
           query = DocsQuery.parse_obj(arguments)
        except Exception as e:
            raise McpError(ErrorData(code=INVALID_PARAMS, message=str(e)))
        try:
            result = await self.chain.ainvoke({"input": query.q})
        except McpError as e:
            return [TextContent(type="text", text=str(e))]
        return [TextContent(type="text", text=result["answer"])]
