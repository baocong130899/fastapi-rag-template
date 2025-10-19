import uuid
from sqlalchemy import Column, String, Boolean, UUID, ForeignKey, TIMESTAMP, Text
from sqlalchemy.sql import func
from .base import Base, TimestampMixin


class RefreshTokenModel(Base, TimestampMixin):
    __tablename__ = "refresh_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    jti = Column(String(100), nullable=False, unique=True, index=True)
    token_hash = Column(String(255), nullable=False)
    issued_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    expires_at = Column(TIMESTAMP, nullable=False)
    used = Column(Boolean, nullable=False, default=False)
    revoked = Column(Boolean, nullable=False, default=False)
    revoked_at = Column(TIMESTAMP, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)