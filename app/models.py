"""Pydantic models for request/response validation."""

from typing import List
from pydantic import BaseModel


class Token(BaseModel):
    """JWT token response model."""

    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    """Login request model."""

    username: str
    password: str


class PaginatedResponse(BaseModel):
    """Paginated response model."""

    page: int
    per_page: int
    total: int
    total_pages: int
    data: List[dict]

