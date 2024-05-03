from fastapi import HTTPException
from jwt import PyJWTError
from data.database import read_query
from hashlib import sha256
import jwt
from data.models import User, UserView


_SECRET = "kisKIS123"


def hash_pass(password):
    hashed_password = sha256(password.encode("utf-8")).hexdigest()
    return hashed_password


def create_token(user: User) -> str:
    payload = {user.id: user.id, user.username: user.username, user.role: user.role}

    encoded = jwt.encode(payload, _SECRET, algorithm="HS256")
    return encoded


def is_authenticated(token: str) -> bool:
    user_id, username, role = jwt.decode(token, _SECRET, algorithms="HS256")

    user_data = read_query("select id, username, role from users where id = ? and username = ?",
                           (user_id, username))

    user = next((UserView.from_query_result(*row) for row in user_data), None)
    if user:
        return user
    else:
        raise HTTPException(status_code=401)


def from_token(token: str) -> User | None:
    user_id, username, role = jwt.decode(token, _SECRET, algorithms="HS256")
    user = read_query("select id, username, role from users where username = ?", (username,))
    return next((UserView.from_query_result(*row) for row in user), None)


def get_user_or_raise_401(token: str) -> User:
    try:
        is_authenticated(token)
        return from_token(token)
    except HTTPException:
        raise HTTPException(status_code=401, detail=str("User doesn't exist"))
    except PyJWTError:
        raise HTTPException(status_code=401, detail=str("Invalid token"))
