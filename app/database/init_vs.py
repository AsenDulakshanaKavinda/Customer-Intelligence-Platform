from app.utils import get_logger, cfg
from app.nlp import load_embedding
from .constants import *

from langchain_postgres import PGVector


log = get_logger(__file__)

def init_vector_store() -> PGVector:
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