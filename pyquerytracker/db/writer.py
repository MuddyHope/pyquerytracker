from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from pyquerytracker.db.models import TrackedQuery
from pyquerytracker.db.session import SessionLocal


class DBWriter:
    @staticmethod
    def save(log_data: dict):
        session = SessionLocal()
        try:
            entry = TrackedQuery(
                function_name=log_data.get("function_name"),
                class_name=log_data.get("class_name"),
                duration_ms=log_data.get("duration_ms"),
                event=log_data.get("event"),
                func_args=log_data.get("func_args"),
                func_kwargs=log_data.get("func_kwargs"),
                error=log_data.get("error"),
                timestamp=log_data.get("timestamp")
                or datetime.now(timezone.utc),  # Ensure timestamp is set
            )
            session.add(entry)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"DBWriter error: {e}")
        finally:
            session.close()

    @staticmethod
    def fetch_all(minutes: int = 5):
        session = SessionLocal()
        try:
            cutoff = datetime.utcnow() - timedelta(minutes=minutes)
            stmt = (
                select(TrackedQuery)
                .where(TrackedQuery.timestamp >= cutoff)
                .order_by(TrackedQuery.timestamp.desc())
            )
            results = session.execute(stmt).scalars().all()

            return [
                {
                    "function_name": row.function_name,
                    "class_name": row.class_name,
                    "duration_ms": row.duration_ms,
                    "timestamp": row.timestamp,
                    "event": row.event,
                    "error": row.error,
                    "func_args": row.func_args,
                    "func_kwargs": row.func_kwargs,
                }
                for row in results
            ]

        except SQLAlchemyError as e:
            print(f"DB fetch error: {e}")
            return []
        finally:
            session.close()
