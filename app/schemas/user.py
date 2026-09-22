from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field, computed_field, field_validator, model_validator
from app.utils.validators import validate_email_format, validate_username

UsernameStr = Annotated[str, Field(min_length=3, max_length=30, description="Unique username")]
EmailStr = Annotated[str, Field(description="Valid email address")]
PasswordStr = Annotated[str, Field(min_length=6, max_length=100, description="User password (min 6 characters)")]


class UserBase(BaseModel):
    username: UsernameStr
    email: EmailStr
    full_name: str | None = Field(None, max_length=100, description="User's full name")

    @field_validator("email")
    @classmethod
    def check_email(cls, v: str) -> str:
        if not validate_email_format(v):
            raise ValueError("Invalid email format")
        return v.lower().strip()

    @field_validator("username")
    @classmethod
    def check_username(cls, v: str) -> str:
        is_valid, msg = validate_username(v)
        if not is_valid:
            raise ValueError(msg)
        return v.strip()


class UserCreate(UserBase):
    password: PasswordStr

    @model_validator(mode="after")
    def check_password_complexity(self) -> "UserCreate":
        if self.password.lower() == self.username.lower():
            raise ValueError("Password cannot be identical to username.")
        return self


class UserUpdate(BaseModel):
    full_name: str | None = Field(None, max_length=100)
    is_active: bool | None = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str | None = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

    @computed_field  # type: ignore[misc]
    @property
    def display_name(self) -> str:
        """Display friendly name defaulting to username if full_name is absent."""
        return self.full_name or self.username


class UserLogin(BaseModel):
    username: str
    password: str

