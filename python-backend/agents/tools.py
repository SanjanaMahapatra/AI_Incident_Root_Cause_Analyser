import httpx
from typing import List, Dict, Any

INCIDENT_SERVICE = "http://localhost:8082"
LOG_SERVICE = "http://localhost:8084"

async def fetch_logs_by_incident(incident_id: int) -> List[Dict]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{INCIDENT_SERVICE}/api/incidents/{incident_id}")
        incident = resp.json()
        log_ids = incident.get("logIds", [])
        logs = []
        for lid in log_ids:
            log_resp = await client.get(f"{LOG_SERVICE}/api/logs/{lid}")
            if log_resp.status_code == 200:
                logs.append(log_resp.json())
        return logs

async def fetch_metrics(service: str) -> Dict:
    # Placeholder – replace with real metrics call
    return {"service": service, "cpu": 45, "memory": 62, "error_rate": 0.02}

async def fetch_alerts(incident_id: int) -> List[Dict]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{INCIDENT_SERVICE}/api/incidents/{incident_id}/alerts")
        if resp.status_code == 200:
            return resp.json()
        return []

# Synchronous wrappers for LangGraph nodes (since nodes are called synchronously)
async def log_search_tool(incident_id: int) -> str:
    logs = await fetch_logs_by_incident(incident_id)
    if not logs:
        return "No logs found."
    return "\n".join([
        f"{l.get('timestamp')} [{l.get('logLevel')}] {l.get('serviceName')}: {l.get('message')}" 
        for l in logs
    ])


async def metric_query_tool(service: str) -> str:
    metrics = await fetch_metrics(service)
    return f"CPU: {metrics['cpu']}%, Memory: {metrics['memory']}%, Error Rate: {metrics['error_rate']}"

async def alert_lookup_tool(incident_id: int) -> str:
    alerts = await fetch_alerts(incident_id)
    if not alerts:
        return "No alerts."
    return "\n".join([f"{a['severity']}: {a['message']}" for a in alerts])