import httpx
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

import mcp.types as types
import uvicorn
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cocktail-server")

# Create MCP server
server = Server("cocktail-server")

@server.list_tools()
async def list_tools():
    """List available tools."""
    return [
        types.Tool(
            name="get_cocktail_instructions",
            description="Get making instructions for a given cocktail",
            inputSchema={
                "type": "object",
                "properties": {
                    "cocktail_name": {
                        "type": "string",
                        "description": "The name of the cocktail (e.g., margarita)"
                    }
                },
                "required": ["cocktail_name"]
            }
        ),
        types.Tool(
            name="explain_ingredient",
            description="Explain what an ingredient is and its characteristics",
            inputSchema={
                "type": "object",
                "properties": {
                    "ingredient_name": {
                        "type": "string",
                        "description": "The name of the ingredient (e.g., vodka)"
                    }
                },
                "required": ["ingredient_name"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """Handle tool calls."""
    if name == "get_cocktail_instructions":
        cocktail_name = arguments.get("cocktail_name")
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={cocktail_name}"
            )
            data = response.json()
            
            if not data.get("drinks"):
                return [
                    {
                        "type": "text",
                        "text": f"No recipe found for {cocktail_name}"
                    }
                ]
            
            # Extract instructions from the first match
            drink = data["drinks"][0]
            instructions = drink.get("strInstructions", "No instructions available.")
            
            return [
                {
                    "type": "text",
                    "text": instructions
                }
            ]
    elif name == "explain_ingredient":
        ingredient_name = arguments.get("ingredient_name")
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://www.thecocktaildb.com/api/json/v1/1/search.php?i={ingredient_name}"
            )
            data = response.json()
            
            if not data.get("ingredients"):
                return [
                    {
                        "type": "text",
                        "text": f"No information found for {ingredient_name}"
                    }
                ]
            
            # Extract description from the first match
            ingredient = data["ingredients"][0]
            description = ingredient.get("strDescription", "No description available.")
            
            return [
                {
                    "type": "text",
                    "text": description
                }
            ]
    raise ValueError(f"Tool {name} not found")

# Expose via SSE on FastAPI
# Disable redirect_slashes to prevent POST body loss during redirects
app = FastAPI(redirect_slashes=False)
sse = SseServerTransport("/messages/")

@app.get("/")
async def root():
    return {"message": "Cocktail MCP Server is running"}

@app.get("/sse")
async def handle_sse(request: Request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )
    return Response()

# Using Mount is the recommended way to bridge the MCP ASGI handler into FastAPI/Starlette.
# This prevents response state conflicts by giving the MCP SDK full control over the sub-path.
app.mount("/messages/", sse.handle_post_message)


