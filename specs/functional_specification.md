# Functional Specification: Cocktail MCP Server

## 1. Overview
This document defines the functional behavior of the Cocktail MCP Server, including its tool definitions, inputs, outputs, and integration logic.

## 2. API Interface (MCP Tools)

### 2.1 `get_cocktail_instructions`
**Description**: Retrieves step-by-step instructions for making a specific cocktail.

- **Inputs**:
  - `cocktail_name` (String, Required): The name of the cocktail (e.g., "Margarita", "Old Fashioned").
- **Outputs**:
  - A text response containing the preparation instructions.
  - If no recipe is found, a descriptive error message: "No recipe found for [name]".
- **Logic**: Calls `https://www.thecocktaildb.com/api/json/v1/1/search.php?s={name}` and extracts `strInstructions`.

### 2.2 `explain_ingredient`
**Description**: Explains the characteristics and usage of a specific cocktail ingredient.

- **Inputs**:
  - `ingredient_name` (String, Required): The name of the ingredient (e.g., "Vodka", "Triple Sec").
- **Outputs**:
  - A text response containing the ingredient's description.
  - If no information is found, a descriptive error message.
- **Logic**: Calls `https://www.thecocktaildb.com/api/json/v1/1/search.php?i={name}` and extracts `strDescription`.

## 3. Communication Protocol
The server implements the Model Context Protocol (MCP) using the following endpoints:
- `GET /sse`: Establishes the SSE connection for downstream messages.
- `POST /messages/`: Handles tool calls and protocol messages via HTTP POST.

## 4. Error Handling
- **API Failures**: If the upstream CocktailDB API is unreachable, the server returns a 500 status or a descriptive MCP error.
- **Invalid Tool**: Requests for non-existent tools result in a `ValueError`.
- **Validation**: FastAPI handles basic schema validation for inputs.
