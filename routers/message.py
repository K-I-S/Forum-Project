from fastapi import APIRouter, Response
from services import message_services
from data.models import Message, ViewMessage
from pydantic import BaseModel

message_router = APIRouter(prefix='/messages')

class ConversationResponseModel(BaseModel):
      messages: list[Message]

@message_router.get('/')
def get_messages():
    return message_services.get_all()

@message_router.get('/{id}')
def get_message_by_id(id: int):
    message = message_services.get_by_id(id)
    if message is None:
        return Response(status_code=404)
    else:
        return message

@message_router.get('users/{id}/conversations')
def get_conversations(id: int):
    return message_services.conversations_by_id(id)

@message_router.get('users/{id}/conversation/{id2}')
def get_messages(user_id_1: int,user_id_2: int):
    return message_services.conversation_between_ids(user_id_1,user_id_2)

@message_router.post('/')
def create_message(message: ViewMessage):
    return message_services.create(message)


