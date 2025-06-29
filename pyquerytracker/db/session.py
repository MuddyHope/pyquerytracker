from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pyquerytracker.config import get_config

engine = create_engine("sqlite:///pyquerytracker/db/querytracker.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
