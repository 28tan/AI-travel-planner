from .user import User

class AuthService:
    def generateAuthUrl(self, state: str) -> str:
        pass

    def handleCallback(self, code: str, state: str) -> User:
        pass

    def logout(self, userId: str):
        pass
