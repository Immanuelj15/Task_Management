from app.exceptions import UserAlreadyExistsException
from app.models.user import User
from app.repositories.base import IUserRepository
from app.repositories.user_repository import InMemoryUserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.utils.security import hash_password, verify_password


class UserService:
    """
    Business Logic Layer for User Management.
    Adheres to SOLID:
    - SRP: Only business rules and workflow orchestration.
    - DIP: Relies on IUserRepository abstraction instead of concrete storage.
    - OCP: Storage backend can be changed without modifying UserService.
    """

    def __init__(self, repository: IUserRepository | None = None) -> None:
        self.repository = repository or InMemoryUserRepository()

    def create_user(self, user_in: UserCreate) -> User:
        # Check unique username
        if self.repository.get_by_username(user_in.username):
            raise UserAlreadyExistsException("username", user_in.username)

        # Check unique email
        if self.repository.get_by_email(user_in.email):
            raise UserAlreadyExistsException("email", user_in.email)

        new_user = User(
            id=0,  # Will be assigned by repository
            username=user_in.username,
            email=user_in.email,
            hashed_password=hash_password(user_in.password),
            full_name=user_in.full_name,
            is_active=True,
        )
        return self.repository.add(new_user)

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.repository.get_by_id(user_id)

    def get_user_by_username(self, username: str) -> User | None:
        return self.repository.get_by_username(username)

    def get_user_by_email(self, email: str) -> User | None:
        return self.repository.get_by_email(email)

    def list_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        return self.repository.list_all(skip=skip, limit=limit)

    def update_user(self, user_id: int, update_data: UserUpdate) -> User | None:
        user = self.repository.get_by_id(user_id)
        if not user:
            return None
        if update_data.full_name is not None:
            user.full_name = update_data.full_name
        if update_data.is_active is not None:
            user.is_active = update_data.is_active
        return self.repository.update(user)

    def delete_user(self, user_id: int) -> bool:
        return self.repository.delete(user_id)

    def authenticate_user(self, username: str, password: str) -> User | None:
        user = self.get_user_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def clear(self) -> None:
        """Reset internal store for test isolation."""
        self.repository.clear()


# Default singleton instance for application use
user_service = UserService()
