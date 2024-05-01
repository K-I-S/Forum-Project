from fastapi import APIRouter, Header

from common.auth import get_user_or_raise_401
from data.models import Reply
from services import reply_service as rs
from services import topic_service as ts
from common.responses import NotFound


replies_router = APIRouter(prefix="/replies")


@replies_router.post(
    "/",
    status_code=201,
)
def create_reply(reply: Reply, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    reply.user_id = user.id

    if not ts.exists(reply.topic_id):
        return NotFound("This topic does not exist!")

    rs.create(reply)

    return f"Reply {reply.id} created successfully"


@replies_router.put("/{id}/vote/{vote_type}")  # or Body; 1
def vote_for_reply(id: int, vote_type: str):

    if vote_type == "up":
        pass
    else:
        pass

    # reply = rs.get_by_id(id)
