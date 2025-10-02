from pydantic import BaseModel, Field
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')

class PaginationRequest(BaseModel):
    page: int = Field(1, ge=1, description="Номер страницы")
    per_page: int = Field(10, ge=1, le=100, description="Количество элементов на странице")

class PaginationResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    per_page: int
    total_pages: int

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def has_prev(self) -> bool:
        return self.page > 1