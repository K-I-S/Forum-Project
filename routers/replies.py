from fastapi import APIRouter, Header, Body, Response

from common.auth import get_user_or_raise_401
from data.models import Reply
from services import reply_service as rs
from services import topic_service as ts
from common.responses import NotFound


replies_router = APIRouter(prefix="/replies")




@replies_router.put("/{id}/vote")
def vote_for_reply(id: int, vote_type: str = Body(...), x_token: str = Header()):

    user = get_user_or_raise_401(x_token)

    if not rs.exists(id):
        return NotFound("This reply does not exist!")

    vote = rs.get_user_vote(user.id, id)
    if vote is None:
        rs.create_user_vote(user.id, vote_type, id)
        return Response(status_code=201)
    else:
        rs.update_vote(id, vote_type)
        return Response(status_code=200)
