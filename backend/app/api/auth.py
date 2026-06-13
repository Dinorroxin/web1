"""
This file defines the API routes for user authentication.
Uses the prefix "/auth" for all routes related to authentication.
Also uses the tags "auth" to group these routes in the API documentation.
Uses HTTP_201_CREATED for the register route to indicate that a new resource has been added.
Uses HTTP_200_OK for the login route to indicate a successful login request.
"""

from fastapi import APIRouter, Depends, status
from app.api.register import register_user
from app.api.login import login_user
from app.schemas.auth import RegisterInput, LoginInput
from app.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(data: RegisterInput):
    return await register_user(data)

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(data: LoginInput):
    return await login_user(data)

@router.get("/me", status_code=status.HTTP_200_OK)
async def me(current_user = Depends(get_current_user)):
    return  {"name": current_user["name"], "email": current_user["email"]}