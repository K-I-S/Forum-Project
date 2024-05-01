from fastapi import APIRouter, Response, Header
from services import message_services
from data.models import ViewMessage
from common.auth import get_user_or_raise_401


message_router = APIRouter(prefix='/messages')

@message_router.get('/')
def get_messages():
    return message_services.get_all()

@message_router.get('/{id}')
def get_message_by_id(id: int):
    message = message_services.get_by_id(id)
    if message is None:
        return Response(status_code=404) # Change to our responses, from Common folder
    else:
        return message

@message_router.get('/conversations')
def get_conversations(x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    return message_services.conversations_by_id(user.id)

@message_router.get('/conversations/{id2}')
def get_messages(id2: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    return message_services.conversation_between_ids(user.id,id2)


@message_router.post('/')
def create_message(message: ViewMessage, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    message.sender_id = user.id
    if not message_services.exists(message.receiver_id):
        return "No such recipient exists!"
    return message_services.create(message)