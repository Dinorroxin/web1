from pydantic import BaseModel, Field, EmailStr

class RegisterInput(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)

class LoginInput(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    message: str