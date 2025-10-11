import uuid
from sqlalchemy import Column, String, UUID, ForeignKey, Text, TIMESTAMP
from sqlalchemy.sql import func
from .base import Base, TimestampMixin


class Chat(Base, TimestampMixin):
    __tablename__ = "chat"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    knowledge_base_id = Column(UUID(as_uuid=True), ForeignKey("knowledge_base.id"))
    title = Column(String(255))


class ChatMessage(Base):
    __tablename__ = "chat_message"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chat.id", ondelete="CASCADE"))
    sender = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
