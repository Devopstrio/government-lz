import logging
import time
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from pythonjsonlogger import jsonlogger

# Logger setup
logger = logging.getLogger("gov-lz-api")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = FastAPI(title="Government Landing Zone API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Path: {request.url.path} Duration: {duration:.4f}s Status: {response.status_code}")
    return response

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/agencies/status")
def get_agencies_status():
    return [
        {"id": "health", "name": "Ministry of Health", "status": "Healthy", "readiness": 0.98},
        {"id": "justice", "name": "Ministry of Justice", "status": "Healthy", "readiness": 0.95},
        {"id": "education", "name": "Ministry of Education", "status": "Warning", "readiness": 0.72},
        {"id": "transport", "name": "Ministry of Transport", "status": "Healthy", "readiness": 0.90}
    ]

@app.post("/landingzone/provision")
def provision_lz(data: dict):
    logger.info(f"Provisioning landing zone for agency: {data.get('agency')}")
    return {"status": "PROVISIONING", "request_id": f"GOV-{int(time.time())}"}

@app.get("/identity/summary")
def get_identity_summary():
    return {
        "total_officials": 450000,
        "mfa_adoption": 0.99,
        "privileged_accounts": 1250,
        "active_citizen_identities": 12500000
    }

@app.get("/costs/summary")
def get_costs_summary():
    return {
        "total_spend_mtd": 12500000,
        "forecast_mtd": 13000000,
        "savings_identified": 850000,
        "top_agency": "Ministry of Health"
    }

@app.get("/compliance/status")
def get_compliance_status():
    return [
        {"standard": "NIST 800-53", "status": "Compliant", "score": 98},
        {"standard": "ISO 27001", "status": "Compliant", "score": 96},
        {"standard": "National Sovereignty", "status": "Partial", "score": 75}
    ]

@app.get("/scores/summary")
def get_scores_summary():
    return {
        "overall_readiness": 0.92,
        "security_posture": 0.95,
        "cost_efficiency": 0.88,
        "sovereign_compliance": 0.85
    }

@app.get("/dashboard/summary")
def get_dashboard_summary():
    return {
        "active_landing_zones": 42,
        "pending_provisions": 3,
        "policy_drift_detected": 1,
        "last_audit_date": "2026-04-20"
    }
