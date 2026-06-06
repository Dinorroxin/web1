from fastapi import APIRouter, status
from app.api.register import register_user
from app.api.login import login_user
from app.schemas.auth import RegisterInput, LoginInput

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(data: RegisterInput):
    return await register_user(data)

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(data: LoginInput):
    return await login_user(data)