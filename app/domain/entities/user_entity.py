from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.application.services.hasher_service import HasherService


@dataclass
class User:
    id: Optional[UUID]
    email: str
    name: str
    is_active: bool
    hashed_password: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def create(
        cls,
        hasher_svc: HasherService,
        email: str,
        name: str,
        is_active: bool,
        password: str,
    ) -> "User":
        hashed = hasher_svc.hash_password(password)

        return cls(
            id=None,
            email=email,
            name=name,
            is_active=is_active,
            hashed_password=hashed,
        )
