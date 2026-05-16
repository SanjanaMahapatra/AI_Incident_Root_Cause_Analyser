from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from agents.graph import create_agent_graph
from retrieval.ingestion import ingest_runbook
from langgraph.checkpoint import BaseCheckpointSaver
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="GenAI Root Cause Analysis")

class AnalysisRequest(BaseModel):
    analysis_id: int   # from Java service
    incident_id: int
    analysis_type: str

class AnalysisResponse(BaseModel):
    analysis_id: int
    result_text: str

class RunbookIngest(BaseModel):
    title: str
    content: str

# Graph instance (singleton)
graph = create_agent_graph()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_incident(req: AnalysisRequest):
    try:
        from utils.clients import fetch_logs_by_incident
        logs = await fetch_logs_by_incident(req.incident_id)
        service = logs[0].get("serviceName") if logs else "unknown"
        
        state = {
            "incident_id": req.incident_id,
            "service": service
        }
        config = {"configurable": {"thread_id": req.analysis_id}}  # checkpoint thread
        final_state = graph.invoke(state, config=config)
        result_text = final_state.get("summary", "{}")
        return AnalysisResponse(analysis_id=req.analysis_id, result_text=result_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest-runbook")
async def ingest_runbook_endpoint(rb: RunbookIngest):
    ingest_runbook(rb.title, rb.content)
    return {"status": "ingested"}

@app.post("/feedback/{analysis_id}")
async def submit_human_feedback(analysis_id: int, feedback: str):
    """Submit human feedback to a previous analysis (resume from checkpoint)."""
    config = {"configurable": {"thread_id": analysis_id}}
    # Update state with human feedback and resume (simplified)
    state = graph.get_state(config)
    if state:
        state.values["human_feedback"] = feedback
        graph.update_state(config, state.values)
    return {"status": "feedback recorded"}