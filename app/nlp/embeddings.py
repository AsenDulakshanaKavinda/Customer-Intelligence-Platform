from app.utils import get_logger, cfg

import os
from dotenv import load_dotenv; load_dotenv()
from langchain_mistralai import MistralAIEmbeddings

log = get_logger(__file__)


def load_embedding(provider: str):
    """
    Factory function to load an embedding model based on the specified provider.

    This function reads configuration from the Hydra 'cfg' object and 
    retrieves API keys from environment variables.

    Args:
        provider (str): The name of the embedding provider. 
            Supported: 'mistral', 'sentence-transformers'.

    Returns:
        MistralAIEmbeddings: An initialized LangChain embedding object.

    Raises:
        ValueError: If the provider is empty or not in the allowed list.
        RuntimeError: If there is an issue during model initialization (e.g: missing API key).
    
    Example:
        >>> model = load_embedding('mistral')
        >>> vector = model.embed_query("Hello world")
    """
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
