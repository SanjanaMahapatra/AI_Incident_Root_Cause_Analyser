import requests
from collections import defaultdict
import os

BASE_URL_LOG = "http://localhost:8084"
BASE_URL_INCIDENT = "http://localhost:8082"

# Your ingested logs (replace with actual GET or use hardcoded IDs)
# In real scenario, you'd GET /api/logs or use the IDs from ingestion response.
logs = [
    {"id": 1, "serviceName": "ServiceA", "logLevel": "WARNING", "message": "Performance Warnings"},
    {"id": 2, "serviceName": "ServiceA", "logLevel": "DEBUG", "message": "File I/O"},
    {"id": 3, "serviceName": "ServiceA", "logLevel": "WARNING", "message": "Performance Warnings"},
    {"id": 4, "serviceName": "ServiceA", "logLevel": "ERROR", "message": "Critical Errors"},
    {"id": 5, "serviceName": "ServiceB", "logLevel": "ERROR", "message": "Critical Errors"},
    {"id": 6, "serviceName": "ServiceA", "logLevel": "FATAL", "message": "Crashes"},
    {"id": 7, "serviceName": "ServiceD", "logLevel": "WARNING", "message": "Performance Warnings"},
    {"id": 8, "serviceName": "ServiceB", "logLevel": "WARNING", "message": "Performance Warnings"},
    {"id": 9, "serviceName": "ServiceD", "logLevel": "ERROR", "message": "Critical Errors"},
    {"id": 10, "serviceName": "ServiceB", "logLevel": "ERROR", "message": "Database Errors"},
    {"id": 11, "serviceName": "ServiceD", "logLevel": "WARNING", "message": "Resource Warnings"},
]

# Group logs by service
service_to_logs = defaultdict(list)
for log in logs:
    service_to_logs[log["serviceName"]].append(log)

def severity_from_levels(levels):
    if "FATAL" in levels:
        return "CRITICAL"
    if "ERROR" in levels:
        return "HIGH"
    if "WARNING" in levels:
        return "MEDIUM"
    return "LOW"

for service, service_logs in service_to_logs.items():
    log_ids = [log["id"] for log in service_logs]
    levels = [log["logLevel"] for log in service_logs]
    severity = severity_from_levels(levels)

    # Create incident
    incident_data = {
        "title": f"Auto incident for {service}",
        "description": f"Created automatically from {len(log_ids)} logs with levels {', '.join(levels)}",
        "severity": severity,
        "status": "OPEN",
        "logIds": log_ids
    }
    resp = requests.post(f"{BASE_URL_INCIDENT}/api/incidents", json=incident_data)
    if resp.status_code == 200:
        incident = resp.json()
        print(f"✅ Created incident {incident['id']} for {service} (severity {severity})")
        
        # Optionally: create alerts for ERROR/FATAL logs
        for log in service_logs:
            if log["logLevel"] in ("ERROR", "FATAL"):
                alert_data = {
                    "ruleName": f"Auto-alert for {log['logLevel']}",
                    "severity": log["logLevel"],
                    "message": f"Log ID {log['id']} triggered this alert",
                    "triggeredAt": "2023-11-20T08:40:50"
                }
                alert_resp = requests.post(f"{BASE_URL_INCIDENT}/api/incidents/{incident['id']}/alerts", json=alert_data)
                if alert_resp.status_code == 200:
                    print(f"   ↳ Added alert for log {log['id']}")
    else:
        print(f"❌ Failed for {service}: {resp.text}")
