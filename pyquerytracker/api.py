from collections import defaultdict

from fastapi import FastAPI, Query, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pyquerytracker.config import get_config
from pyquerytracker.tracker import get_tracked_queries  # ✅ real-time logs
from pyquerytracker.websocket import websocket_endpoint

app = FastAPI(title="Query Tracker API")

templates = Jinja2Templates(directory="templates")


if get_config().dashboard_enabled:

    @app.get("/dashboard", response_class=HTMLResponse)
    def dashboard(request: Request):
        return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/api/query-stats")
def get_query_stats(minutes: int = Query(5, ge=1, le=1440)):
    logs = get_tracked_queries(minutes)

    # You can change this list to match real endpoints you're tracking
    all_endpoints = ["GET /users", "POST /items", "GET /items", "DELETE /items"]
    durations_by_endpoint = defaultdict(list)

    for log in logs:
        # fallback if endpoint is not tracked explicitly
        endpoint = log.get("endpoint") or log.get("function_name") or "UNKNOWN"
        durations_by_endpoint[endpoint].append(log.get("duration_ms", 0))

    # Build chart-ready response
    return {
        "labels": all_endpoints,
        "durations": [
            round(
                sum(durations_by_endpoint.get(ep, []))
                / max(1, len(durations_by_endpoint.get(ep, []))),
                2,
            )
            for ep in all_endpoints
        ],
    }


@app.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    await websocket_endpoint(websocket)
