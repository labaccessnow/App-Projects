#!/usr/bin/env python3
"""A tiny MCP server — expose ops knowledge to an LLM as *tools* over stdio.

This is the shape behind my memory-rag MCP: instead of letting the model guess, it calls a
tool that returns real data. The @mcp.tool() decorator turns a plain typed function into a
tool the client can discover and invoke; the docstring becomes the tool description.

    pip install "mcp[cli]"
    python examples/mcp_server.py        # speaks MCP over stdio
"""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ops-tools")


@mcp.tool()
def search_runbooks(query: str, k: int = 5) -> list[str]:
    """Return the k most relevant runbook chunks for a query.

    Wire this to your vector store (see rag_search.py). Stubbed here for the example.
    """
    return [f"runbook hit {i} for {query!r}" for i in range(k)]


@mcp.tool()
def device_facts(hostname: str) -> dict:
    """Look up basic facts about a device from inventory."""
    # real impl: read your NetBox / inventory source of truth
    return {"hostname": hostname, "role": "leaf", "site": "lab"}


if __name__ == "__main__":
    mcp.run()  # stdio transport by default
