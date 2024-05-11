from fastapi import APIRouter, Response, Header
from services import message_services
from data.models import ViewMessage
from common.auth import get_user_or_raise_401
from common.responses import NotFound, Unauthorized


message_router = APIRouter(prefix='/conversations')

@message_router.get('/')
def get_conversations(x_token: str = Header(None)):
    if x_token is None:
        return Unauthorized("Token header is missing! You need to log in first!")
    
    user = get_user_or_raise_401(x_token)

    return message_services.conversations_by_id(user.id)

@message_router.get('/{id2}')
def get_messages(id2: int, x_token: str = Header(None)):
    if x_token is None:
        return Unauthorized("Token header is missing! You need to log in first!")
    
    user = get_user_or_raise_401(x_token)
    return message_services.conversation_between_ids(user.id,id2)


@message_router.post('/', status_code=201)
def create_message(message: ViewMessage, x_token: str = Header(None)):
    if x_token is None:
        return Unauthorized("Token header is missing! You need to log in first!")
    
    user = get_user_or_raise_401(x_token)
    message.sender_id = user.id
    if not message_services.exists(message.receiver_id):
        return NotFound("No such recipient exists!")
    return message_services.create(message)