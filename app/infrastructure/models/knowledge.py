import uuid
from sqlalchemy import Column, String, UUID, ForeignKey, ARRAY, BigInteger, Text, JSON
from pgvector.sqlalchemy import Vector
from .base import Base, TimestampMixin


class KnowledgeBase(Base, TimestampMixin):
    __tablename__ = "knowledge_base"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    type = Column(String(50), nullable=False)  # 'basic' or 'folder'
    document_ids = Column(ARRAY(UUID(as_uuid=True)))


class Document(Base, TimestampMixin):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    file_name = Column(String(255), nullable=False)
    file_size = Column(BigInteger)
    file_hash = Column(String(255))


class DocumentEmbeddingsStatus(Base, TimestampMixin):
    __tablename__ = "document_embeddings_status"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(
        UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE")
    )
    status = Column(String(50), nullable=False)
    error = Column(Text)

class Embeddings(Base):
    __tablename__ = "embeddings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    embed = Column(Vector(), nullable=False)
    content = Column(Text, nullable=False)
    cmetadata = Column(JSON, nullable=True)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"))
