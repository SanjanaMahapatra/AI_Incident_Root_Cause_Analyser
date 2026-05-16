import httpx
from typing import List, Dict, Any
import os

LOG_SERVICE = os.getenv("LOG_SERVICE_URL")
INCIDENT_SERVICE = os.getenv("INCIDENT_SERVICE_URL")

async def fetch_logs_by_incident(incident_id: int) -> List[Dict]:
    """Get logs associated with an incident (via incident's log_ids)."""
    async with httpx.AsyncClient() as client:
        # First get incident to retrieve log_ids
        resp = await client.get(f"{INCIDENT_SERVICE}/api/incidents/{incident_id}")
        incident = resp.json()
        log_ids = incident.get("logIds", [])
        if not log_ids:
            return []
        logs = []
        for lid in log_ids:
            resp_log = await client.get(f"{LOG_SERVICE}/api/logs/{lid}")
            if resp_log.status_code == 200:
                logs.append(resp_log.json())
        return logs

async def fetch_metrics(service: str, time_range: str = "5m") -> Dict:
    """Placeholder: query metrics from a monitoring system (Prometheus etc.)."""
    # In real implementation, call your metrics service.
    return {"service": service, "cpu": 45, "memory": 62, "error_rate": 0.02}

async def fetch_alerts(incident_id: int) -> List[Dict]:
    """Get alerts linked to an incident."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{INCIDENT_SERVICE}/api/incidents/{incident_id}/alerts")
        if resp.status_code == 200:
            return resp.json()
        return []