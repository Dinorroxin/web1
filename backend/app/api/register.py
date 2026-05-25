import bcrypt
from datetime import datetime, timezone
from app.database import getdatabase

db = getdatabase()

def encrypt_password(password: str) -> str:

    # Get the bytes of the password
    password_bytes = password.encode('utf-8')

    # Add random salt
    salt = bcrypt.gensalt()

    # Convert the password back to string with the salt
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password.decode('utf-8')

async def register_user(front_data):
    today_date = datetime.now(timezone.utc)

    encrypted_password = encrypt_password(front_data["password"])

    new_user = {
        "name": front_data["name"],
        "email": front_data["email"],
        "encrypted_password": encrypted_password,
        "created_at": today_date,
        "active": True
    }

    result = await db.users.insert_one(new_user)
    id_user = str(result.inserted_id)
    
    return {"status": "success",
            "message": "User registered successfully", 
            "user_id": id_user}