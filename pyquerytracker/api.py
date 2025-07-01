from datetime import datetime, timedelta

from fastapi import FastAPI, Query, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pyquerytracker.config import get_config
from pyquerytracker.db.models import TrackedQuery
from pyquerytracker.db.session import SessionLocal
from pyquerytracker.websocket import websocket_endpoint

app = FastAPI(title="Query Tracker API")

templates = Jinja2Templates(directory="templates")


if get_config().dashboard_enabled:

    @app.get("/dashboard", response_class=HTMLResponse)
    def dashboard(request: Request):
        return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/api/query-stats")
def get_query_stats(minutes: int = Query(5, ge=1, le=1440)):
    cutoff = datetime.utcnow() - timedelta(minutes=minutes)
    print(f"[DEBUG] Cutoff: {cutoff}")

    session = SessionLocal()
    try:
        logs = (
            session.query(TrackedQuery)
            .filter(TrackedQuery.timestamp >= cutoff)  # Now comparing text to text
            .order_by(TrackedQuery.timestamp)
            .all()
        )
        print(f"[DEBUG] Matching logs: {len(logs)}")
        return {
            "labels": [q.timestamp for q in logs],
            "durations": [q.duration_ms for q in logs],
            "events": [q.event for q in logs],
            "function_names": [q.function_name for q in logs],
        }
    finally:
        session.close()


@app.get("/debug/queries")
def debug_queries():
    session = SessionLocal()
    try:
        rows = (
            session.query(TrackedQuery)
            .order_by(TrackedQuery.timestamp.desc())
            .limit(5)
            .all()
        )
        return [
            {
                "timestamp": r.timestamp,
                "duration_ms": r.duration_ms,
                "event": r.event,
            }
            for r in rows
        ]
    finally:
        session.close()


@app.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    await websocket_endpoint(websocket)
