from app.utils import get_logger, cfg

from sqlalchemy import Column, Integer, Text, String, ForeignKey
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import sessionmaker, relationship
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

class User(Base):
    """
    SQLAlchemy model representing a user in the system.

    Attributes:
        user_id (str): Primary key, unique identifier for the user.
        username (str): Unique username for the user.
        password_hash (str): Hashed password for authentication purposes.
    """
    __tablename__ = "users"

    user_id = Column(String, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)

    feedback = relationship("Feedback", back_populates="user")


class Item(Base):
    """
    SQLAlchemy model representing an item in the system.

    Attributes:
        item_id (int): Primary key.
        name (str): Name of the item.
        description (str): Description of the item.
    """
    __tablename__ = "items"

    item_id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)

    feedback = relationship("Feedback", back_populates="item")


class Feedback(Base):
    """
    SQLAlchemy model representing user feedback.
    
    Attributes:
        feedback_id (str): Primary key.
        user_id (str): Identifier for the user providing feedback.
        item_id (str): Identifier for the item the feedback is about.
        sentiment (str): The sentiment classification of the feedback (e.g., "positive", "negative", "neutral").
        topic (str): The topic classification of the feedback (e.g., "product", "service", "delivery").
        content (str): The raw text of the feedback provided by the user.
    """
    __tablename__ = "feedback"

    feedback_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    Item_id = Column(String, ForeignKey("items.item_id"))
    sentiment = Column(String)
    topic = Column(String)
    content = Column(String)

    user = relationship("User", back_populates="feedback")
    item = relationship("Item", back_populates="feedback")