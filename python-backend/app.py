import os

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, ConfigDict
from agents.graph import create_agent_graph
from retrieval.ingestion import ingest_runbook
import uvicorn
from utils.clients import fetch_logs_by_incident
from json import JSONDecodeError
from pydantic.alias_generators import to_camel

from dotenv import load_dotenv
load_dotenv()

# import requests
# response = requests.get("http://localhost:8082/api/incidents")
# print(response.status_code)

# Debug: verify API key is loaded (remove after testing)
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("WARNING: OPENAI_API_KEY not set. The LLM will not work.")

app = FastAPI(title="GenAI Root Cause Analysis")

class AnalysisRequest(BaseModel):
    # analysis_id: int

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )
    incident_id: int
    analysis_type: str


class AnalysisResponse(BaseModel):

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )

    # analysis_id: int
    result_text: str
class RunbookIngest(BaseModel):
    title: str
    content: str

# Graph instance
graph = create_agent_graph()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_incident(req: AnalysisRequest):
         
    try:
        logs = await fetch_logs_by_incident(req.incident_id)
        service = logs[0].get("serviceName") if logs else "unknown"
        
        state = {
            "incident_id": req.incident_id,
            "service": service,
            "logs": logs,
            "analysis_type": req.analysis_type
        }
        final_state = await graph.ainvoke(state)
        result_text = final_state.get("summary", "{}")
        return AnalysisResponse(resultText=result_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest-runbook")
async def ingest_runbook_endpoint(rb: RunbookIngest):
    ingest_runbook(rb.title, rb.content)
    return {"status": "ingested"}

@app.post("/feedback/{analysis_id}")
async def submit_human_feedback(analysis_id: int, feedback: str):
    # Placeholder for feedback handling
    return {"status": "feedback recorded (not implemented)"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))