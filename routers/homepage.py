from fastapi import APIRouter, Header, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from data.models import LoginData, User
from services import user_service
from common import responses, auth


home_router = APIRouter(prefix='/home')
templates = Jinja2Templates(directory="templates")

@home_router.get("/", response_class=HTMLResponse)
async def get_home_page(request: Request):
    return templates.TemplateResponse("home_page.html", {"request":request})
