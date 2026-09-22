import threading
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.security import hash_password, verify_password


class UserService:
    def __init__(self) -> None:
        self._users: dict[int, User] = {}
        self._id_counter: int = 1
        self._lock = threading.Lock()

    def create_user(self, user_in: UserCreate) -> User:
        with self._lock:
            # Check unique username
            for existing in self._users.values():
                if existing.username.lower() == user_in.username.lower():
                    from app.exceptions import UserAlreadyExistsException
                    raise UserAlreadyExistsException("username", user_in.username)
                if existing.email.lower() == user_in.email.lower():
                    from app.exceptions import UserAlreadyExistsException
                    raise UserAlreadyExistsException("email", user_in.email)


            new_user = User(
                id=self._id_counter,
                username=user_in.username,
                email=user_in.email,
                hashed_password=hash_password(user_in.password),
                full_name=user_in.full_name,
                is_active=True,
            )
            self._users[new_user.id] = new_user
            self._id_counter += 1
            return new_user

    def get_user_by_id(self, user_id: int) -> User | None:
        return self._users.get(user_id)

    def get_user_by_username(self, username: str) -> User | None:
        for u in self._users.values():
            if u.username.lower() == username.lower():
                return u
        return None

    def get_user_by_email(self, email: str) -> User | None:
        for u in self._users.values():
            if u.email.lower() == email.lower():
                return u
        return None

    def list_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        users = list(self._users.values())
        return users[skip : skip + limit]

    def update_user(self, user_id: int, update_data: UserUpdate) -> User | None:
        with self._lock:
            user = self._users.get(user_id)
            if not user:
                return None
            if update_data.full_name is not None:
                user.full_name = update_data.full_name
            if update_data.is_active is not None:
                user.is_active = update_data.is_active
            return user

    def delete_user(self, user_id: int) -> bool:
        with self._lock:
            if user_id in self._users:
                del self._users[user_id]
                return True
            return False

    def authenticate_user(self, username: str, password: str) -> User | None:
        user = self.get_user_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def clear(self) -> None:
        """Reset internal store, helpful for unit testing."""
        with self._lock:
            self._users.clear()
            self._id_counter = 1


user_service = UserService()
