from app.utils import cfg, get_logger
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

log = get_logger(__file__)


class DocumentIngest:
    """
    Handles the end-to-end ingestion process for PDF documents.
    This class manages loading raw PDF files from disk and splitting them into 
    smaller, overlapping chunks suitable for vector embedding and retrieval.
    """
    def __init__(self, filepath: Path):
        """
        Initializes the DocumentIngest instance.

        Args:
            filepath (Path): The filesystem path to the PDF document.
        """
        self.filepath: Path = filepath
        self.chunk_size: int = cfg.documents.chunk_size
        self.chunk_overlap: int = cfg.documents.chunk_overlap


    def _read_docs(filepath: Path) -> List[Document]:
        """
        Reads a PDF file and extracts its content into LangChain Documents.

        Args:
            filepath (Path): Path to the target PDF file.

        Returns:
            List[Document]: A list of documents containing the raw text from the PDF.

        Raises:
            ValueError: If the filepath is missing or empty.
            FileNotFoundError: If the file does not exist at the specified path.
            RuntimeError: If an unexpected error occurs during PDF loading.
        """
        if not filepath:
            log.error((f"Filepath missing or empty"))
            raise ValueError(f"Filepath missing or empty")
        
        try:
            loader = PyPDFLoader(file_path=filepath)
            raw_docs = loader.load()
            log.info(f"File {str(filepath)} loaded")
            return raw_docs
        except FileNotFoundError as e:
            log.error(f"File {str(filepath)} not found")
            raise FileNotFoundError(f"File not found")
        except Exception as e:
            log.info(f"Error while reading document: {str(e)}")
            raise RuntimeError("Error while reading document")

    def _split_docs(self, docs: Document) -> List[Document]:
        """
        Splits raw documents into smaller chunks based on class configuration.

        Args:
            docs (List[Document]): The list of raw documents to be split.

        Returns:
            List[Document]: A list of document chunks.

        Raises:
            ValueError: If the input document list is empty.
            RuntimeError: If an error occurs during the splitting process.
        """

        if not docs:
            log.error(f"Docs are missing or empty")
            raise ValueError(f"Docs are missing or empty")

        try:
            spitter = RecursiveCharacterTextSplitter(
                chunk_size = self.chunk_size,
                chunk_overlap = self.chunk_overlap
            )
            chunks = spitter.split_documents(docs)
            log.info(f"Create {len(chunks)} chunks")
            return chunks
        except Exception as e:
            log.error(f"Error while splitting documents: {str(e)}")
            raise RuntimeError("Error while splitting documents")

        
    def ingest_documents(self) -> List[Document]:
        """
        Executes the full ingestion pipeline: reading and then splitting the file.

        This is the main entry point for processing a document.

        Returns:
            List[Document]: The final list of processed document chunks.

        Raises:
            RuntimeError: If any part of the ingestion pipeline fails.
        """
        
        try:
            raw_docs = self._read_docs(self.filepath)
            chunks = self._split_docs(raw_docs)
            log.info("Document ingest completed")
            return chunks
        except Exception as e:
            log.error(f"Error while ingesting documents: {str(e)}")
            raise RuntimeError("Error while ingesting documents")
        
    