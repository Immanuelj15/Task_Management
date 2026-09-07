from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    id: int
    username: str
    email: str
    hashed_password: str
    full_name: str | None = None
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
