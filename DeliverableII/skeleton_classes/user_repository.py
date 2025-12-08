from .user import User

class UserRepository:
    def upsertUser(self, profile: User) -> User:
        pass

    def findUser(self, userId: str) -> User:
        pass
