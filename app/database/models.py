from app.utils import get_logger, cfg

from sqlalchemy import Column, Integer, Text
from pgvector.sqlalchemy import Vector
from .session import Base

TABLE_NAME = cfg.db.TABLE_NAME
VECTOR_SIZE = cfg.db.VECTOR_SIZE


class Document(Base):
    __tablename__ = TABLE_NAME

    id = Column(Integer, primary_key=True)
    content = Column(Text)

    # embedding vector
    embedding = Column(Vector(VECTOR_SIZE))