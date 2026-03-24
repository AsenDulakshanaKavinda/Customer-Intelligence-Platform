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

class Feedback(Base):
    """
    SQLAlchemy model representing user feedback.
    
    Attributes:
        id (int): Primary key.
        user_id (str): Identifier for the user providing feedback.
        sentiment (str): The sentiment classification of the feedback (e.g., "positive", "negative", "neutral").
        topic (str): The topic classification of the feedback (e.g., "product", "service", "delivery").
        content (str): The raw text of the feedback provided by the user.
    """
    
    __tablename__ = "feedback"

    id = Column(Text, primary_key=True)
    user_id = Column(Text)
    sentiment = Column(Text)
    topic = Column(Text)
    content = Column(Text)