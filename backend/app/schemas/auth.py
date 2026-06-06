"""
Set Classes to validade the data coming from frontend, this way we can ensure that the data is in the correct format.
"""

from pydantic import BaseModel, Field, EmailStr

# EmailStr is a special type provided by Pydantic that validates that the input is a valid email address
# Set a minimum and maximum length for the password to ensure that it's not too short or too long
class RegisterInput(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)

class LoginInput(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    message: str