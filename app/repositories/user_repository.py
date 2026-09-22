import threading
from app.models.user import User
from app.repositories.base import IUserRepository


class InMemoryUserRepository(IUserRepository):
    """
    In-memory implementation of IUserRepository.
    Thread-safe storage dedicated strictly to persistence operations (SRP).
    """

    def __init__(self) -> None:
        self._users: dict[int, User] = {}
        self._id_counter: int = 1
        self._lock = threading.RLock()

    def get_by_id(self, user_id: int) -> User | None:
        return self._users.get(user_id)

    def get_by_username(self, username: str) -> User | None:
        for u in self._users.values():
            if u.username.lower() == username.lower():
                return u
        return None

    def get_by_email(self, email: str) -> User | None:
        for u in self._users.values():
            if u.email.lower() == email.lower():
                return u
        return None

    def list_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        users = list(self._users.values())
        return users[skip : skip + limit]

    def add(self, user: User) -> User:
        with self._lock:
            user.id = self._id_counter
            self._users[user.id] = user
            self._id_counter += 1
            return user

    def update(self, user: User) -> User | None:
        with self._lock:
            if user.id in self._users:
                self._users[user.id] = user
                return user
            return None

    def delete(self, user_id: int) -> bool:
        with self._lock:
            if user_id in self._users:
                del self._users[user_id]
                return True
            return False

    def clear(self) -> None:
        with self._lock:
            self._users.clear()
            self._id_counter = 1
