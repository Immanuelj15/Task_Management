from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from app.utils.validators import validate_email_format, validate_username


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=30, description="Unique username")
    email: str = Field(..., description="Valid email address")
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
    password: str = Field(..., min_length=6, max_length=100, description="User password (min 6 characters)")


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


class UserLogin(BaseModel):
    username: str
    password: str
