from app.utils import cfg, get_logger

from scripts import init_vector_store
from scripts import DocumentIngest

from pathlib import Path

log = get_logger(__file__)

class KnowledgeBase:
    """
    Manages the lifecycle of the vector database, including initialization 
    and document ingestion.

    Attributes:
        vector_store: The initialized vector database instance used for 
            storing and querying document embeddings.
    """

    def __init__(self):
        # Initializes the KnowledgeBase with a connection to the vector store
        self.vector_store = init_vector_store()
        
    def create_knowledge_base(self, source_filepath: Path):

        """
        Ingests documents from a file path and adds them to the vector store.

        This method handles the end-to-end flow of reading a file, splitting it into 
        chunks (via DocumentIngest), and committing those chunks to the database.

        Args:
            source_filepath (Path): The filesystem path to the document(s) to be ingested.

        Raises:
            ValueError: If the source_filepath is None or if no documents are 
                found within the file.
            RuntimeError: If the file does not exist or if an unexpected error 
                occurs during the vector store update.
        """

        if not source_filepath:
            log.error((f"source file missing or empty"))
            raise ValueError(f"source file missing or empty")

        try:
            doc_ingest = DocumentIngest(filepath=source_filepath)
            docs = doc_ingest.ingest_documents()

            if docs:
                log.info(f"Ingest {str(docs)} documents")
            else:
                log.error("documents are missing or empty")
                raise ValueError("documents are missing or empty")
            
            self.vector_store.add_documents(documents=docs)

        except FileNotFoundError as e:
            log.error(f"source file missing: {str(e)}")
            raise RuntimeError("source file missing")
        except Exception as e:
            log.error(f"Error while creating the knowledge base: {str(e)}")
            raise RuntimeError("Error while creating the knowledge base")

