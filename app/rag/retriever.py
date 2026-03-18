from app.utils import cfg, get_logger

from scripts import init_vector_store

from langchain_core.documents import Document
from typing import List


log = get_logger(__file__)


class Retrievers:
    def __init__(self):
        self.vector_store = init_vector_store()
        self.k = 10

    def similarity_search_with_filter(self, query: str, filter: dict | None) -> List[Document]:
        if not query:
            log.error("query is missing")
            raise ValueError("query is missing")

        try:    
            result = self.vector_store.similarity_search(
                query=query,
                k=self.k,
                filter=filter
            )
            log.info("similarity search with filters completed")
            return result
        
        except Exception as e:
            log.error(f"Error while similarity search with filter: {str(e)}")
            raise RuntimeError(f"Error while similarity search with filter")
        
    def search_as_retriever(self, query: str) -> List[Document]:
        if not query:
            log.error("query is missing")
            raise ValueError("query is missing")

        try:
            retriever = self.vector_store.as_retriever(search_type="mmr", search_kwargs={"k": self.k})
            result = retriever.invoke(input=query)
            log.info("search as retriever completed")
            return result

        except Exception as e:
            log.error(f"Error while search as retriever: {str(e)}")
            raise RuntimeError(f"Error while search as retriever")

