from pydantic import BaseModel, EmailStr
from fastapi import Form


class AuthLogin(BaseModel):
    username: EmailStr
    password: str

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        password: str = Form(...),
    ):
        return cls(username=username, password=password)


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
