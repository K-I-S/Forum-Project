from fastapi import APIRouter, Response
# from fastapi.responses import JSONResponse
from services import message_services
from data.models import Message

message_router = APIRouter(prefix='/messages')




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
def get_messages():
    return message_services.get_all()
    

