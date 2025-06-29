from pyquerytracker.db.session import SessionLocal
from pyquerytracker.db.models import TrackedQuery
from sqlalchemy.exc import SQLAlchemyError

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
            )
            session.add(entry)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"DBWriter error: {e}")
        finally:
            session.close()
