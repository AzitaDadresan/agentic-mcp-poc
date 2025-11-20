# Agentic MCP PoC

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**Secure LangGraph MCP proof-of-concept for quantitative query orchestration with OAuth/IP guardrails.**

## Features
- LangGraph agents (Analyzer, Retriever)
- FastAPI backend with /query endpoint
- OAuth2 authentication
- IP whitelist validation
- Mock PnL data

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Start server
uvicorn main:app --reload

# Test endpoint
curl -X POST "http://localhost:8000/query" \
  -H "Authorization: Bearer fake-token" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the portfolio VaR?"}'
```

Visit http://localhost:8000/docs for API docs.

## Run Tests

```bash
pytest test_mcp.py -v
```

## Author
Azita Dadresan | CQF, JHU TA

## License
MIT
