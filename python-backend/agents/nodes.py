from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langgraph.prebuilt import ToolExecutor, ToolInvocation
from agents.tools import tools
from retrieval.vectorstore import retrieve_context
import os

llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"), temperature=0)
tool_executor = ToolExecutor(tools)

# Bind tools to LLM for automatic tool calling (optional)
llm_with_tools = llm.bind_tools(tools)

def log_analysis_node(state):
    incident_id = state["incident_id"]
    # Use tool manually
    result = tool_executor.invoke(ToolInvocation(tool="log_search_tool", tool_input={"incident_id": incident_id}))
    prompt = f"Analyze the following logs and list error patterns, anomalies, and suspicious timestamps:\n{result}"
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"log_analysis": response.content}

def anomaly_detection_node(state):
    service = state.get("service", "unknown")
    result = tool_executor.invoke(ToolInvocation(tool="metric_query_tool", tool_input={"service": service}))
    prompt = f"Based on metrics: {result}, identify any anomalies (spikes, degradation, or unusual patterns)."
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"anomaly_analysis": response.content}

def metric_correlation_node(state):
    logs = state.get("log_analysis", "")
    anomalies = state.get("anomaly_analysis", "")
    prompt = f"Correlate the following logs and anomalies to find possible root cause. Logs:\n{logs}\nAnomalies:\n{anomalies}"
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"correlation": response.content}

def rag_node(state):
    query = state.get("correlation", state.get("log_analysis", ""))
    docs = retrieve_context(query)
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = f"Using knowledge base, suggest root cause and remediation. Context:\n{context}\nIncident analysis: {state}"
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"rag_suggestion": response.content}

def summarizer_node(state):
    from schemas.output import IncidentSummary
    parser = PydanticOutputParser(pydantic_object=IncidentSummary)
    format_instructions = parser.get_format_instructions()
    prompt = f"""
    Based on all analysis:
    Log analysis: {state.get('log_analysis', '')}
    Anomaly detection: {state.get('anomaly_analysis', '')}
    Correlation: {state.get('correlation', '')}
    RAG suggestion: {state.get('rag_suggestion', '')}
    {format_instructions}
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    try:
        summary = parser.parse(response.content)
    except:
        summary = IncidentSummary(root_cause="Unknown", impact="Unknown", recommended_actions="Check logs", confidence_score=0.5)
    return {"summary": summary.json()}