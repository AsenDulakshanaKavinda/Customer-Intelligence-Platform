from app.utils import get_logger, cfg

from sqlalchemy import Column, Integer, Text
from pgvector.sqlalchemy import Vector
from .session import Base

TABLE_NAME = cfg.db.TABLE_NAME
VECTOR_SIZE = cfg.db.VECTOR_SIZE


class Document(Base):
    """
    SQLAlchemy model representing a vectorized text document.
    
    Attributes:
        id (int): Primary key.
        content (str): The raw text of the document.
        embedding (Vector): A vector representation of the content, 
            sized according to VECTOR_SIZE (usually 768 or 1024).
    """
    
    __tablename__ = TABLE_NAME

    id = Column(Integer, primary_key=True)
    content = Column(Text)

    # embedding vector
    embedding = Column(Vector(VECTOR_SIZE))