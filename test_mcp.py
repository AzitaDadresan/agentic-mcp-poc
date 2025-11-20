# Unit tests for MCP agents and API endpoints

import pytest
from fastapi.testclient import TestClient
from main import app, AnalyzerAgent, RetrieverAgent

client = TestClient(app)

def test_analyzer_var():
    """Test AnalyzerAgent VaR computation."""
    agent = AnalyzerAgent()
    result = agent.analyze("What is the portfolio VaR?")
    assert "value" in result
    assert result["metric"] == "95% VaR"

def test_retriever_pnl():
    """Test RetrieverAgent data fetch."""
    agent = RetrieverAgent()
    result = agent.retrieve("Get PnL history")
    assert "data" in result
    assert len(result["data"]) > 0

def test_query_endpoint_unauthorized():
    """Test query endpoint without auth token."""
    response = client.post("/query", json={"question": "What is VaR?"})
    assert response.status_code == 401

def test_query_endpoint_authorized():
    """Test query endpoint with valid token."""
    response = client.post(
        "/query",
        json={"question": "What is the Sharpe ratio?"},
        headers={"Authorization": "Bearer fake-token"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["agent"] == "AnalyzerAgent"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
