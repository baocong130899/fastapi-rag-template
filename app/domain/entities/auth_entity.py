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
class RefreshToken:
    user_id: str
    jti: str
    token_hash: str
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
        token_hash: str,
        issued_at: datetime,
        expires_at: datetime,
        used: bool = False,
        revoked: bool = False,
        revoked_at: Optional[datetime] = None
    ) -> "RefreshToken":
        
        return cls(
            user_id=user_id,
            jti=jti,
            token_hash=token_hash,
            issued_at=issued_at,
            expires_at=expires_at,
            used=used,
            revoked=revoked,
            revoked_at=revoked_at
        )