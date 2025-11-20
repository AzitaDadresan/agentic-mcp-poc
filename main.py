# FastAPI + LangGraph MCP for quant query orchestration
# Author: Azita Dadresan | Fidelity anomaly detection + CQF AI methods

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
from guardrails import validate_ip, get_current_user

app = FastAPI(title="Agentic MCP PoC", version="1.0.0")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "quant_user": {
        "username": "quant_user",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

class AnalyzerAgent:
    """Agent for computing risk metrics (VaR, Sharpe, etc.)."""
    def analyze(self, query: str) -> Dict[str, Any]:
        if "var" in query.lower():
            return {"metric": "95% VaR", "value": -12500.75, "unit": "USD"}
        elif "sharpe" in query.lower():
            return {"metric": "Sharpe Ratio", "value": 1.85}
        return {"error": "Unknown query"}

class RetrieverAgent:
    """Agent for fetching historical PnL data."""
    def retrieve(self, query: str) -> Dict[str, Any]:
        return {
            "data": [
                {"date": "2025-01-01", "pnl": 15000},
                {"date": "2025-01-02", "pnl": -8000},
                {"date": "2025-01-03", "pnl": 22000}
            ],
            "source": "portfolio_db"
        }

analyzer = AnalyzerAgent()
retriever = RetrieverAgent()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: Dict[str, Any]
    agent: str

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """OAuth2 password flow for token generation."""
    user = fake_users_db.get(form_data.username)
    if not user or form_data.password != "secret":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return {"access_token": "fake-token", "token_type": "bearer"}

@app.post("/query", response_model=QueryResponse)
async def query_mcp(
    request: Request,
    query: QueryRequest,
    token: str = Depends(oauth2_scheme),
    user: dict = Depends(get_current_user)
):
    """Main MCP query endpoint with agent orchestration."""
    client_ip = request.client.host
    validate_ip(client_ip)
    
    question = query.question.lower()
    if any(kw in question for kw in ["var", "sharpe", "risk"]):
        result = analyzer.analyze(query.question)
        agent_name = "AnalyzerAgent"
    elif any(kw in question for kw in ["pnl", "history", "data"]):
        result = retriever.retrieve(query.question)
        agent_name = "RetrieverAgent"
    else:
        raise HTTPException(status_code=400, detail="Unknown query type")
    
    return QueryResponse(answer=result, agent=agent_name)

@app.get("/")
async def root():
    return {"message": "Agentic MCP PoC - Secure LangGraph Orchestration"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
