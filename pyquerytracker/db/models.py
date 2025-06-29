from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class TrackedQuery(Base):
    __tablename__ = "tracked_queries"

    id = Column(Integer, primary_key=True, index=True)
    function_name = Column(String)
    class_name = Column(String, nullable=True)
    duration_ms = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    event = Column(String)  # "slow_execution", "normal_execution", "error"
    func_args = Column(String)
    func_kwargs = Column(String)
    error = Column(String, nullable=True)
