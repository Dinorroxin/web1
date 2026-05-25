import bcrypt 
from app.database import getdatabase

db = getdatabase()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Convert string credentials to bytes for bcrypt processing
    plain_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')

    # Compare plain text password against stored hash
    return bcrypt.checkpw(plain_bytes, hashed_bytes)

async def login_user(front_data: dict):
    # Fetch user document from database by email
    user = await db.users.find_one({"email": front_data["email"]})
    
    # Return error if user does not exist
    if not user:
        return {"status": "error", "message": "E-mail ou senha incorretos"}

    # Check if the user account is active   
    if not user.get("active", True):
        return {"status": "error", "message": "Email ou senha incorretos"}
    
    # Validate the provided password against the stored encrypted password
    password_match = verify_password(front_data["password"], user["encrypted_password"])

    # Return error if password does not match
    if not password_match:
        return {"status": "error", "message": "E-mail ou senha incorretos"}

    return {"status": "success", 
            "message": "Login bem-sucedido", 
            "user_name": str(user["name"]),
            "user_email": str(user["email"]),}