"""
This file is responsible for handling the security token service of the application, it uses the jose library to create and verify JWT tokens
"""

import os
import datetime
import uuid
from jose import jwt
from jose.exceptions import JWTError
from fastapi import HTTPException
from app.config import settings

# Get to /backend/app where the .pem files are located
current_dir = os.path.dirname(os.path.abspath(__file__))
pem_dir = os.path.dirname(current_dir)


# Fail-fast if PEM paths are not configured
if not settings.PRIVATE_KEY_PATH or not settings.PUBLIC_KEY_PATH:
    raise RuntimeError("PRIVATE_KEY_PATH and PUBLIC_KEY_PATH must be set in .env")


# Read the PEM files
with open(os.path.join(pem_dir, settings.PRIVATE_KEY_PATH), "r") as f:
    private_key = f.read()

with open(os.path.join(pem_dir, settings.PUBLIC_KEY_PATH), "r") as f:
    public_key = f.read()

def load_private_key() -> str:
    return private_key

def load_public_key() -> str:
    return public_key

def create_access_token(data: dict) -> str:

    payload = data.copy()

    # Set the expiration time for the token (e.g., 15 minutes)
    now = datetime.datetime.utcnow()
    expire = now + datetime.timedelta(minutes=15)
    payload.update({
        "exp": expire,
        "iat": now,  # Issued at time
        "jti": str(uuid.uuid4()),  # Unique identifier for the token
        "type": "access"
        })

    # Create the JWT token using the private key and RS256 algorithm
    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token

def create_refresh_token(data: dict) -> str:
    
    # Load the private key from the .env file
    private_key = load_private_key()

    # Set the expiration time for the token (e.g., 15 minutes)
    now = datetime.datetime.utcnow()
    expire = now + datetime.timedelta(days=7)
    data.update({
        "exp": expire,
        "iat": now,  # Issued at time
        "jti": str(uuid.uuid4()),   # Unique identifier for the token
        "type": "refresh"
        })

    # Create the JWT token using the private key and RS256 algorithm
    token = jwt.encode(data, private_key, algorithm="RS256")
    return token

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, public_key, algorithms=["RS256"])
        return payload
    except JWTError:
        raise JWTError("Couldn't validate the token")