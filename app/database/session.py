from app.utils import get_logger, cfg
from .constants import DATABASE_URL

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_session():
    """
    Dependency generator for database sessions.
    
    Yields:
        SessionLocal: A transactional database session.
    
    Note:
        Ensures the session is closed even if an error occurs during the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()