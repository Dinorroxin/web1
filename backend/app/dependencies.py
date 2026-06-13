"""
    This file handles the dependency injection using the payload give by the security.py, If the signature its from and access_token and not from a refresh, fetches for the 
    corresponding user from the database
"""
from bson import ObjectId
from jose.exceptions import JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.security import verify_token
from app.database import getdatabase

# Extracts the JWT token from the "Authorization: Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
db = getdatabase()

async def get_current_user(token: str = Depends(oauth2_scheme)):

    # Verify the token signature and expiration. If its not valid, raise an JWTError
    try:
        payload = verify_token(token)
    except JWTError:
        # Same as JWTError but its better because it avoids leaking information about the token
        raise HTTPException(status_code=401, detail="couldn't validate the token", headers={"WWW-Authenticate": "Bearer"})

    if payload["type"] == "access":
        # If the token is valid, gets the user id from the token analyzed as string
        user_id = payload["sub"]

        # Convert the string back to ObjectId for MongoDB query
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            # Edge case: user was deleted after the token was issued
            raise HTTPException(status_code=401, detail="Couldn't validate the token", headers={"WWW-Authenticate": "Bearer"})
        
        # Success — returns the user document to the endpoint
        return user
    
    else:
        # Rejects refresh tokens — only access tokens authenticate endpoints
        raise HTTPException(status_code=401, detail="couldn't validate the token", headers={"WWW-Authenticate": "Bearer"})