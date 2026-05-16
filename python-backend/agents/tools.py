from langchain.tools import tool
import asyncio
from utils.clients import fetch_logs_by_incident, fetch_metrics, fetch_alerts

@tool
def log_search_tool(incident_id: int) -> str:
    """Retrieve logs for a given incident ID."""
    try:
        # Run async function in sync context
        logs = asyncio.run(fetch_logs_by_incident(incident_id))
        if not logs:
            return "No logs found."
        return "\n".join([f"{l['timestamp']} [{l['logLevel']}] {l.get('serviceName', '?')}: {l.get('message', '')}" for l in logs[:20]])
    except Exception as e:
        return f"Error fetching logs: {e}"

@tool
def metric_query_tool(service: str) -> str:
    """Get CPU, memory, error rate for a service."""
    try:
        metrics = asyncio.run(fetch_metrics(service))
        return f"CPU: {metrics.get('cpu',0)}%, Memory: {metrics.get('memory',0)}%, Error Rate: {metrics.get('error_rate',0)}"
    except Exception as e:
        return f"Error fetching metrics: {e}"

@tool
def alert_lookup_tool(incident_id: int) -> str:
    """Retrieve alerts linked to an incident."""
    try:
        alerts = asyncio.run(fetch_alerts(incident_id))
        if not alerts:
            return "No alerts."
        return "\n".join([f"{a['severity']}: {a['message']}" for a in alerts])
    except Exception as e:
        return f"Error fetching alerts: {e}"

tools = [log_search_tool, metric_query_tool, alert_lookup_tool]