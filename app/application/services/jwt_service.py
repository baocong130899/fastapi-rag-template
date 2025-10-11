from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from jwt import PyJWTError
from app.infrastructure.enums.auth_enum import TokenType


class JwtService:

    def __init__(
        self,
        secret: str,
        algorithm: str,
        access_expires: int,
        refresh_expires: int,
    ):
        self.secret = secret
        self.algorithm = algorithm
        self.access_expires = access_expires
        self.refresh_expires = refresh_expires

    def create_access_token(
        self, subject: str, extra_claims: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create access token."""
        now = datetime.now()
        payload: Dict[str, Any] = {
            "sub": subject,
            "iat": now.timestamp(),
            "exp": now + timedelta(seconds=self.access_expires),
            "type": TokenType.ACCESS.value,
        }
        if extra_claims:
            payload.update(extra_claims)

        token = jwt.encode(payload=payload, key=self.secret, algorithm=self.algorithm)
        return token

    def create_refresh_token(
        self, subject: str, extra_claims: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create refresh token."""
        now = datetime.now()
        payload: Dict[str, Any] = {
            "sub": subject,
            "iat": now.timestamp(),
            "exp": now + timedelta(seconds=self.refresh_expires),
            "type": TokenType.REFRESH.value,
        }
        if extra_claims:
            payload.update(extra_claims)

        token = jwt.encode(payload=payload, key=self.secret, algorithm=self.algorithm)
        return token

    def decode_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(jwt=token, key=self.secret, algorithms=self.algorithm)
            return payload
        except PyJWTError as exc:
            raise ValueError("Invalid token") from exc

    def verify_access_token(self, token: str) -> Dict[str, Any]:
        payload = self.decode_token(token)
        if payload.get("type") != TokenType.ACCESS.value:
            raise ValueError("Token is not access token!.")
        return payload

    def verify_refresh_token(self, token: str) -> Dict[str, Any]:
        payload = self.decode_token(token)
        if payload.get("type") != TokenType.REFRESH.value:
            raise ValueError("Token is not refresh token!.")
        return payload
