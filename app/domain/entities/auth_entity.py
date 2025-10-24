from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Auth:
    access_token: str
    refresh_token: str

@dataclass
class AuthRefresh:
    access_token: str


@dataclass
class Token:
    id: Optional[str]
    user_id: str
    jti: str
    type: str
    issued_at: datetime
    expires_at: datetime
    used: bool
    revoked: bool
    revoked_at: Optional[datetime]

    @classmethod
    def create(
        cls,
        user_id: str,
        jti: str,
        type: str,
        issued_at: datetime,
        expires_at: datetime,
        used: bool = False,
        revoked: bool = False,
        revoked_at: Optional[datetime] = None
    ) -> "Token":
        
        return cls(
            id=None,
            user_id=user_id,
            jti=jti,
            type=type,
            issued_at=issued_at,
            expires_at=expires_at,
            used=used,
            revoked=revoked,
            revoked_at=revoked_at
        )