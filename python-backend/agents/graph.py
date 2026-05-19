from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional, Literal
from agents.nodes import *

class GraphState(TypedDict):
    incident_id: int
    service: Optional[str]
    log_analysis: Optional[str]
    anomaly_analysis: Optional[str]
    correlation: Optional[str]
    rag_suggestion: Optional[str]
    summary: Optional[str]
    human_feedback: Optional[str]
    analysis_type: Optional[str]

def decide_route(state: GraphState) -> Literal["root_cause", "short_description"]:
    if state["analysis_type"] == "ROOT_CAUSE":
        return "root_cause"
    elif state["analysis_type"] == "SHORT_DESCRIPTION":
        return "short_description"
    else:
        return "root_cause"

def create_agent_graph():
    workflow = StateGraph(GraphState)
    
    workflow.add_node("log_analysis", log_analysis_node)
    workflow.add_node("anomaly_detection", anomaly_detection_node)
    workflow.add_node("metric_correlation", metric_correlation_node)
    workflow.add_node("rag_retrieval", rag_node)
    workflow.add_node("summarizer", summarizer_node)

    workflow.add_node("root_cause", root_cause_analysis_node)
    workflow.add_node("short_description", short_description_node)
    
    workflow.set_entry_point("log_analysis")
    workflow.add_edge("log_analysis", "anomaly_detection")
    workflow.add_edge("anomaly_detection", "metric_correlation")
    workflow.add_edge("metric_correlation", "rag_retrieval")
    workflow.add_conditional_edges("rag_retrieval", decide_route)
    workflow.add_edge("root_cause", END)
    workflow.add_edge("short_description", END)
    
    return workflow.compile()