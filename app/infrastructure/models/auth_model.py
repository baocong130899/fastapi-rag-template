import uuid
from typing import Any, List
from sqlalchemy import Column, String, Boolean, UUID, ForeignKey, TIMESTAMP, Text
from sqlalchemy.sql import func
from app.infrastructure.enums.auth_enum import TokenType
from .base import Base, TimestampMixin


class TokenModel(Base, TimestampMixin):
    __tablename__ = "tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    jti = Column(String(100), nullable=False, unique=True, index=True)
    type = Column(String(45), nullable=True, default=TokenType.ACCESS.value, comment="Type: access_token, refresh_token")
    issued_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    expires_at = Column(TIMESTAMP, nullable=False)
    used = Column(Boolean, nullable=False, default=False)
    revoked = Column(Boolean, nullable=False, default=False)
    revoked_at = Column(TIMESTAMP, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)

