from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from agents.tools import log_search_tool, metric_query_tool, alert_lookup_tool
from retrieval.vectorstore import retrieve_context
import os
from schemas.output import IncidentSummary, ShortDescription
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage


llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"), temperature=0)

async def log_analysis_node(state):
    incident_id = state["incident_id"]
    logs_text = await log_search_tool(incident_id)
    prompt = f"Analyze the following logs and list error patterns, anomalies, and suspicious timestamps:\n{logs_text}"
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"log_analysis": response.content}

async def anomaly_detection_node(state):
    service = state.get("service", "unknown")
    metrics_text = await metric_query_tool(service)
    prompt = f"Based on metrics: {metrics_text}, identify any anomalies (spikes, degradation, or unusual patterns)."
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


async def root_cause_analysis_node(state: dict) -> dict:
    """
    Produces a detailed root cause analysis using logs, anomalies, metrics, and RAG context.
    """

    parser = PydanticOutputParser(pydantic_object=IncidentSummary)
    format_instructions = parser.get_format_instructions()

    # Extract data from state (assuming these keys exist from previous nodes)
    logs_summary = state.get("logs_summary", "No logs available.")
    anomalies = state.get("anomalies", "No anomalies detected.")
    metrics = state.get("metrics", "No metrics available.")
    rag_context = state.get("rag_context", "No historical data found.")
    
    # Build a prompt for the LLM
    prompt = f"""
        You are an expert incident analyst. Given the following information, identify the root cause of the incident.
        Provide a clear, structured explanation covering:
        - What happened
        - Why it happened (root cause)
        - Evidence supporting your conclusion
        Based on all analysis, identify the root cause of the incident.

        Logs summary:
        {logs_summary}

        Detected anomalies:
        {anomalies}

        Metrics (CPU, memory, error rate):
        {metrics}

        Historical context from RAG:
        {rag_context}

        {format_instructions}

        Root cause analysis:
    """

    response = await llm.ainvoke([HumanMessage(content=prompt)])

    try:
        summary = parser.parse(response.content)
    except Exception:
        summary = IncidentSummary(
            root_cause="Unknown",
            impact="Unknown",
            recommended_actions=["Check logs manually"],
            confidence_score=0.5
        )
    
    # Return the result – the summarizer expects a "summary" or "result" field
    return {"summary": summary.json()}

async def short_description_node(state: dict) -> dict:
    """
    Produces a one‑sentence short description of the incident.
    """

    parser = PydanticOutputParser(pydantic_object=IncidentSummary)
    format_instructions = parser.get_format_instructions()

    logs_summary = state.get("logs_summary", "No logs available.")
    anomalies = state.get("anomalies", "")
    metrics = state.get("metrics", "")
    rag_context = state.get("rag_context", "")
    
    prompt = f"""
        Based on the incident data below, write a single, concise sentence that describes what happened and its impact.
        
        Logs summary:
        {logs_summary}

        Anomalies:
        {anomalies}

        Metrics:
        {metrics}

        Historical context:
        {rag_context}

        {format_instructions}

        Short description (one sentence):
    """
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    try:
        short = parser.parse(response.content)
    except Exception:
        short = ShortDescription(short_description="Incident occurred, further analysis required.")
    
    return {"summary": short.json()}


def summarizer_node(state):
    from schemas.output import IncidentSummary
    from langchain_core.output_parsers import PydanticOutputParser
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
    except Exception:
        summary = IncidentSummary(root_cause="Unknown", impact="Unknown", recommended_actions=["Check logs manually"], confidence_score=0.5)
    return {"summary": summary.json()}