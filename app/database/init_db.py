from app.utils import get_logger

from .session import engine, Base
from . import models
from sqlalchemy import text

log = get_logger(__file__)

def init_db():
    try:
        with engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()
        Base.metadata.create_all(engine)  
        log.info(f"Initializing database connection successful") 
    except Exception as e:
        log.error(f"Error while Initializing database connection: {str(e)}")
        raise RuntimeError(f"Error while Initializing database connection: {str(e)}")