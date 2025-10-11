from pwdlib import PasswordHash


class HasherService:

    def __init__(self):
        self.pwd = PasswordHash.recommended()

    def hash_password(self, plain: str) -> str:
        return self.pwd.hash(plain)

    def verify_password(self, plain: str, hashed: str) -> bool:
        return self.pwd.verify(plain, hashed)
