from sqlalchemy import select
from .models import Document
from .session import SessionLocal


class PGVectorClient:

    def __init__(self):
        self.db = SessionLocal()

    def add_document(self, text, embedding):

        doc = Document(
            content=text,
            embedding=embedding
        )

        self.db.add(doc)
        self.db.commit()

    def similarity_search(self, query_embedding, k=5):

        stmt = (
            select(Document)
            .order_by(Document.embedding.l2_distance(query_embedding))
            .limit(k)
        )

        results = self.db.execute(stmt).scalars().all()

        return results