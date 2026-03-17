from app.utils import cfg, get_logger
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

log = get_logger(__file__)


class DocumentIngest:
    """
    
    """
    def __init__(self, filepath: Path):
        self.filepath: Path = filepath
        self.chunk_size: int = cfg.documents.chunk_size
        self.chunk_overlap: int = cfg.documents.chunk_overlap


    def _read_docs(filepath: Path) -> List[Document]:
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

        if not docs:
            log.error(f"Docs are missing or empty")
            ValueError(f"Docs are missing or empty")

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
        
        try:
            raw_docs = self._read_docs(self.filepath)
            chunks = self._split_docs(raw_docs)
            log.info("Document ingest completed")
            return chunks
        except Exception as e:
            log.error(f"Error while ingesting documents: {str(e)}")
            raise RuntimeError("Error while ingesting documents")