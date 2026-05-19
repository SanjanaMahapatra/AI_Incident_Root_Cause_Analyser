import httpx
from typing import List, Dict, Any

INCIDENT_SERVICE = "http://localhost:8082"
LOG_SERVICE = "http://localhost:8084"

async def fetch_logs_by_incident(incident_id: int) -> List[Dict]:
    print(f"DEBUG: Calling {INCIDENT_SERVICE}/api/incidents/{incident_id}")
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{INCIDENT_SERVICE}/api/incidents/{incident_id}")
        print(f"DEBUG: Incident response status = {resp.status_code}")
        incident = resp.json()
        log_ids = incident.get("logIds", [])
        if not log_ids:
            return []
        logs = []
        for lid in log_ids:
            log_resp = await client.get(f"{LOG_SERVICE}/api/logs/{lid}")
            if log_resp.status_code == 200:
                logs.append(log_resp.json())
        return logs

async def fetch_metrics(service: str, time_range: str = "5m") -> Dict:
    # Placeholder – replace with real metrics call if needed
    return {"service": service, "cpu": 45, "memory": 62, "error_rate": 0.02}

async def fetch_alerts(incident_id: int) -> List[Dict]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{INCIDENT_SERVICE}/api/incidents/{incident_id}/alerts")
        if resp.status_code == 200:
            return resp.json()
        return []