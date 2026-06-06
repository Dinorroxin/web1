"""
This file is responsible for handling the user registration process, including encrypting the password using bcrypt and inserting the new user into the database.
"""

import bcrypt
import pymongo.errors
from datetime import datetime, timezone
from app.database import getdatabase
from app.schemas.auth import RegisterInput

db = getdatabase()

def encrypt_password(password: str) -> str:

    # Convert the password to bytes for bcrypt
    password_bytes = password.encode('utf-8')

    # Add random salt
    salt = bcrypt.gensalt()

    # "Mix" the password with the salt and hash it
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    
    # Convert the password back to string with the salt
    return hashed_password.decode('utf-8')

async def register_user(front_data: RegisterInput):
    """
    Uses the Classes from schemas/auth.py to validate the data coming from the frontend, then encrypts the password and inserts the new user into the database, if the email 
    is already registered it will return an error message
    """
        
    today_date = datetime.now(timezone.utc)
    
    # Call the function to encrypt the password
    encrypted_password = encrypt_password(front_data.password)

    new_user = {
        "name": front_data.name,
        "email": front_data.email,
        "encrypted_password": encrypted_password,
        "created_at": today_date,            
        "active": True
    }

    try:
        result = await db.users.insert_one(new_user)
    except pymongo.errors.DuplicateKeyError:
        return {"status": "error", "message": "E-mail já registrado"}
    
    # It will insert id in the beginning of the user
    id_user = str(result.inserted_id)
    
    return {"status": "success",
            "message": "User registered successfully", 
            "user_id": id_user}