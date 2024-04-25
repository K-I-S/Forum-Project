from fastapi import APIRouter, Response
from services import message_services
from data.models import ViewMessage
from pydantic import BaseModel

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

@message_router.get('/{id}/conversations')
def get_conversations(id: int):
    return message_services.conversations_by_id(id)

@message_router.get('/{id}/conversations/{id2}')
def get_messages(id: int,id2: int):
    return message_services.conversation_between_ids(id,id2)

@message_router.post('/')
def create_message(message: ViewMessage):
    if not message_services.exists(message.receiver_id):
        return "No such recipient exists!"
    return message_services.create(message)