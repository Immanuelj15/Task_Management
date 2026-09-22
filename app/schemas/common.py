import math
from datetime import datetime
from typing import Any, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """
    Standardized Generic API response wrapper demonstrating Pydantic generics and typing.
    """
    success: bool = True
    message: str = "Operation completed successfully"
    data: T | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class PaginationMeta(BaseModel):
    total_items: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool

    @classmethod
    def create(cls, total: int, skip: int, limit: int) -> "PaginationMeta":
        page_size = max(1, limit)
        current_page = (skip // page_size) + 1
        total_pages = max(1, math.ceil(total / page_size))
        return cls(
            total_items=total,
            page=current_page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=current_page < total_pages,
            has_prev=current_page > 1,
        )


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Standardized Generic Paginated container.
    """
    items: list[T]
    meta: PaginationMeta
