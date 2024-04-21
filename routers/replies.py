from fastapi import APIRouter
from data.models import Reply
from services import reply_service as rs
from services import topic_service as ts


replies_router = APIRouter(prefix="/replies")


@replies_router.post("/", status_code=201)
def create_reply(reply: Reply):
    if not ts.exists(reply.topic_id):
        return f"Topic {reply.topic_id} does not exist!"

    rs.create(reply)

    return f"Reply {reply.id} created successfully"
