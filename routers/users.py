from fastapi import APIRouter, Header
from data.models import LoginData, User
from services import user_service
from common import responses, auth


users_router = APIRouter(prefix='/users')


@users_router.post("/register")
def register_user(user: User):
    if user_service.check_if_username_exists(user.username):
        return responses.BadRequest("Username is taken")
    if user_service.check_if_email_exists(user.email):
        return responses.BadRequest("User with this email already exists")
    return user_service.create(user)


@users_router.post('/login')
def login(data: LoginData):
    user = user_service.find_by_username_password(data.username, data.password)

    if user:
        token = auth.create_token(user)
        return {'token': token}
    else:
        return responses.BadRequest('Invalid login data')


@users_router.get('/info')
def user_info(x_token: str = Header()):
    return auth.get_user_or_raise_401(x_token)
