from app.utils import get_logger, cfg

import os
from dotenv import load_dotenv; load_dotenv()
from langchain_mistralai import MistralAIEmbeddings

log = get_logger(__file__)


def load_embedding(provider: str):
    allowed_models = ['mistral', 'sentence-transformers']
    
    if not provider:
        raise ValueError("parameter is missing or empty")
    
    if provider not in allowed_models:
        log.error(f"provider: {provider} is not allowed")
        raise ValueError(f"provider: {provider} is not allowed")

    try:
        if provider == 'mistral':
            log.info(f"Using {provider} embedding model")
            return MistralAIEmbeddings(
                model=cfg.embeddings.model_name,
                api_key=os.getenv(cfg.embeddings.api_key),
                timeout=cfg.embeddings.timeout,
                max_retries=cfg.embeddings.max_retries,
            )
        
        if provider == 'sentence-transformers':
            log.info(f"Using {provider} embedding model")
            # todo - add sentence-transformers/all-minilm-l6-v2
        
    except Exception as e:
        log.error(f"Error while loading embedding model: {str(e)}")
        raise RuntimeError(f"Error while loading embedding model: {str(e)}")
