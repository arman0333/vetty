"""Authentication router."""

from fastapi import APIRouter, HTTPException, status, Depends
from app.models import LoginRequest, Token
from app.auth import create_access_token, verify_password, get_password_hash
from datetime import timedelta
from app.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])

# In-memory user store (in production, use a database)
# Default test user: username=testuser, password=testpass
# Initialize lazily to avoid import-time hashing issues
USERS_DB = None


def get_users_db():
    """Get users database, initializing if necessary."""
    global USERS_DB
    if USERS_DB is None:
        USERS_DB = {
            "testuser": {
                "username": "testuser",
                "hashed_password": get_password_hash("testpass"),
            }
        }
    return USERS_DB


@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest):
    """
    Login endpoint to get JWT access token.

    Args:
        login_data: Login credentials (username and password)

    Returns:
        JWT access token
    """
    users_db = get_users_db()
    user = users_db.get(login_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if not verify_password(login_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": login_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

