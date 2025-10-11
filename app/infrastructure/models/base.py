from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, TIMESTAMP
from sqlalchemy.sql import func


Base = declarative_base()


class TimestampMixin:
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
