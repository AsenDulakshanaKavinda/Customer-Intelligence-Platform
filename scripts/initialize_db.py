    
from app.utils import get_logger, cfg
from app.nlp import load_embedding
from app.database.session import engine, Base
from app.database import models
from scripts.constants import *

from sqlalchemy import text

from langchain_postgres import PGVector


log = get_logger(__file__)

def init_db():
    """
    Bootstraps the database by enabling pgvector and creating tables.
    
    Warning:
        This requires the DB user to have permission to install extensions.
    """
    try:
        with engine.connect() as conn:
            # pgvector MUST be enabled before the Document table is created.
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()
        Base.metadata.create_all(engine)  
        log.info(f"Initializing database connection successful") 
    except Exception as e:
        log.error(f"Error while Initializing database connection: {str(e)}")
        raise RuntimeError(f"Error while Initializing database connection: {str(e)}")


def init_vector_store() -> PGVector:
    """
    Initializes a LangChain-compatible vector store instance.
    
    This is used when you need to integrate with LangChain chains or agents.
    """
    try:
        vector_store = PGVector(
            embeddings=load_embedding('mistral'),
            collection_name=COLLECTION_NAME,
            connection=DATABASE_URL,
            use_jsonb=True,
        ) 
        log.info(f"Initializing vs connection successful") 
        return vector_store
        
    except Exception as e:
        log.error(f"Error while Initializing vs connection: {str(e)}")
        raise RuntimeError(f"Error while Initializing vs connection: {str(e)}")   