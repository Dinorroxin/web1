"""
This file contains the logic for handling user login, including password verification and response generation. 
The implementation also includes measures to mitigate timing attacks by using a dummy hash when a user is not found.
"""

import bcrypt 
from app.database import getdatabase
from app.schemas.auth import LoginInput

db = getdatabase()

# The dummy hash it's nos inside the function to avoid the bcrypt processing when the user is not found, this way we can mitigate timing attacks by equalizing the response time 
# for both cases (user found and user not found) and prevent attackers from inferring valid emails based on response times.
# The dummy hash is a valid bcrypt hash that will be used to perform a password check even when the user does not exist, ensuring that the time taken to respond is consistent
# regardless of whether the email is registered or not.
DUMMY_HASH = "$2b$12$wpxhnxhlzX0CM.XcwXvtg.3oKQzzdkCHtWYe/XWwjvpklvFx4OREe"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Convert string credentials to bytes for bcrypt processing
    plain_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')

    # Compare plain text password against stored hash
    return bcrypt.checkpw(plain_bytes, hashed_bytes)

async def login_user(front_data: LoginInput):
    # Fetch user document from database by email
    user = await db.users.find_one({"email": front_data.email})
    
    # Return error if user does not exist
    if not user:
        # Fake hash to mitigate timing attacks when user is not found
        verify_password(front_data.password, DUMMY_HASH)  # Perform dummy check to equalize response time
        return {"status": "error", "message": "E-mail ou senha incorretos"}

    # Check if the user account is active   
    if not user.get("active", True):
        return {"status": "error", "message": "Email ou senha incorretos"}
    
    # Validate the provided password against the stored encrypted password
    password_match = verify_password(front_data.password, user["encrypted_password"])

    # Return error if password does not match
    if not password_match:
        return {"status": "error", "message": "E-mail ou senha incorretos"}

    return {"status": "success", 
            "message": "Login bem-sucedido", 
            "name": str(user["name"]),
            "email": str(user["email"])}