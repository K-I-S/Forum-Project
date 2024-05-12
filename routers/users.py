from fastapi import APIRouter, Header, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from data.models import LoginData, User
from services import user_service
from common import responses, auth


users_router = APIRouter(prefix='/users')
templates = Jinja2Templates(directory="templates")

@users_router.get("/register_login", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})



@users_router.post("/register")
async def register_user(user: User = Depends(User.from_form)):
    if user_service.check_if_username_exists(user.username):
        return responses.BadRequest("Username is taken")
    if user_service.check_if_email_exists(user.email):
        return responses.BadRequest("User with this email already exists")
    return user_service.create(user)


@users_router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@users_router.post('/login')
def login(username = Form(...), password= Form(...)):
    user = user_service.find_by_username_password(username, password)

    if user:
        token = auth.create_token(user)
        return {'token': token}
    else:
        return responses.BadRequest('Invalid login data')


@users_router.get('/info')
def user_info(x_token: str = Header()):
    return auth.get_user_or_raise_401(x_token)