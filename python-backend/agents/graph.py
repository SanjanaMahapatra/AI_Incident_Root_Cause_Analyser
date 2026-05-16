from langgraph.graph import StateGraph, END
from langgraph.checkpoint import MemorySaver
from typing import TypedDict, Optional
from agents.nodes import *

class GraphState(TypedDict):
    incident_id: int
    service: Optional[str]
    log_analysis: Optional[str]
    anomaly_analysis: Optional[str]
    correlation: Optional[str]
    rag_suggestion: Optional[str]
    summary: Optional[str]
    human_feedback: Optional[str]   # for human-in-loop

def create_agent_graph():
    workflow = StateGraph(GraphState)
    
    workflow.add_node("log_analysis", log_analysis_node)
    workflow.add_node("anomaly_detection", anomaly_detection_node)
    workflow.add_node("metric_correlation", metric_correlation_node)
    workflow.add_node("rag_retrieval", rag_node)
    workflow.add_node("summarizer", summarizer_node)
    workflow.add_node("human_review", lambda state: state)   # placeholder for interrupt
    
    workflow.set_entry_point("log_analysis")
    workflow.add_edge("log_analysis", "anomaly_detection")
    workflow.add_edge("anomaly_detection", "metric_correlation")
    workflow.add_edge("metric_correlation", "rag_retrieval")
    workflow.add_edge("rag_retrieval", "summarizer")
    workflow.add_edge("summarizer", "human_review")
    workflow.add_edge("human_review", END)
    
    # Add checkpointing for human review
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)