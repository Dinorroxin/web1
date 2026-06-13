from bson import ObjectId
from jose.exceptions import JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.security import verify_token
from app.database import getdatabase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
db = getdatabase()

async def get_current_user(token: str = Depends(oauth2_scheme)):


    try:
        payload = verify_token(token)
    except JWTError:
        raise HTTPException(status_code=401, detail="couldn't validate the token", headers={"WWW-Authenticate": "Bearer"})

    if payload["type"] == "access":

        user_id = payload["sub"]
        user = await db.users.find_one({"_id": ObjectId(user_id)})

        if not user:
            raise HTTPException(status_code=401, detail="Couldn't validate the token", headers={"WWW-Authenticate": "Bearer"})
        return user
    else:
        raise HTTPException(status_code=401, detail="couldn't validate the token", headers={"WWW-Authenticate": "Bearer"})