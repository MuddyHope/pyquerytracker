from fastapi import APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session

from pyquerytracker.db.models import TrackedQuery
from pyquerytracker.db.session import SessionLocal

router = APIRouter()


@router.get("/metrics")
def get_metrics():
    """
    Get aggregated query tracking metrics.
    
    Returns:
        dict: JSON object containing:
            - total_queries: Total number of tracked queries
            - average_execution_time_ms: Average execution time in milliseconds
            - slowest_query: Information about the slowest query
    """
    session = SessionLocal()
    try:
        # Get total number of queries
        total_queries = session.query(func.count(TrackedQuery.id)).scalar()
        
        # Get average execution time
        avg_duration = session.query(func.avg(TrackedQuery.duration_ms)).scalar()
        
        # Get slowest query
        slowest_query = (
            session.query(TrackedQuery)
            .order_by(TrackedQuery.duration_ms.desc())
            .first()
        )
        
        # Prepare response
        response = {
            "total_queries": total_queries or 0,
            "average_execution_time_ms": round(avg_duration, 2) if avg_duration else 0,
        }
        
        # Add slowest query info if available
        if slowest_query:
            response["slowest_query"] = {
                "function_name": slowest_query.function_name,
                "execution_time_ms": slowest_query.duration_ms,
                "timestamp": slowest_query.timestamp.isoformat(),
                "event": slowest_query.event,
            }
        else:
            response["slowest_query"] = None
            
        return response
        
    finally:
        session.close() 