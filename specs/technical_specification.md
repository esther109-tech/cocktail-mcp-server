# Technical Specification: Cocktail MCP Server

## 1. System Architecture
The Cocktail MCP Server is a Python-based web service utilizing the FastAPI framework and the `mcp` SDK. It is designed to run as a stateless container.

### 1.1 Technology Stack
- **Language**: Python 3.10+
- **Framework**: FastAPI
- **Transport**: MCP over Server-Sent Events (SSE)
- **HTTP Client**: `httpx` (Asynchronous)
- **Server**: `uvicorn` / `hypercorn`

## 2. Deployment Details
- **Platform**: Google Cloud Run
- **Region**: `europe-west1`
- **Service URL**: `https://cocktail-mcp-server-593899410363.europe-west1.run.app`
- **Containerization**: Docker (see `Dockerfile` in root)
- **Access Control**: Publicly accessible.

## 3. API Endpoints
### 3.1 Health Check
- **Path**: `/`
- **Method**: `GET`
- **Response**: `{"message": "Cocktail MCP Server is running"}`

### 3.2 SSE Connection
- **Path**: `/sse`
- **Method**: `GET`
- **Function**: Initiates the MCP session.

### 3.3 Message Processing
- **Path**: `/messages/`
- **Method**: `POST`
- **Function**: Receives MCP JSON-RPC messages.

## 4. Integration Logic
The server acts as a proxy to `TheCocktailDB` public API.
- **Search Logic**: Uses the `s` query parameter for cocktails and `i` for ingredients.
- **Concurrency**: Leverages Python's `asyncio` to handle multiple concurrent SSE connections efficiently.

## 5. Security
- **Authentication**: Currently open for public access as per requirements.
- **Traffic Management**: Cloud Run provides auto-scaling and basic DDoS protection.
