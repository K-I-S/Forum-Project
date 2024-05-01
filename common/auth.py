from fastapi import HTTPException
from jwt import PyJWTError

from data.models import User
from services.user_service import is_authenticated, from_token


def get_user_or_raise_401(token: str) -> User:
    try:
        is_authenticated(token)
        return from_token(token)
    except HTTPException:
        raise HTTPException(status_code=401, detail=str("User doesn't exist"))
    except PyJWTError as ex:
        raise HTTPException(status_code=401, detail=str("Invalid token"))


# Login logic might go here
