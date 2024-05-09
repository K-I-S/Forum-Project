from fastapi import APIRouter, Query, Body, Header
from data.models import Topic, TopicResponseModel
from services import topic_service as ts
from services import reply_service as rs
from services import category_service as cs
from datetime import datetime
from common.auth import get_user_or_raise_401
from common.responses import Forbidden, NotFound, Unauthorized, BadRequest

topics_router = APIRouter(prefix="/topics")


@topics_router.get("/")
def get_topics(
    title: str | None = None,
    status: str | None = Query(default=None, regex="^(unlocked|locked)$"),
):
    return ts.all(title, status)


@topics_router.get("/{id}")
def get_by_id(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    topic = ts.get_by_id(id)
    if topic is None:
        return NotFound("There is no such topic!")
    
    category = cs.get_by_id(topic.category_id)

    if not category.is_private() or cs.user_has_read_access(category.id, user.id):
        return TopicResponseModel(topic=topic, replies=rs.get_by_topic(topic.id))

    else: 
        return Unauthorized("You don't have access to the category this topic belongs to!")    

    

@topics_router.post("/", status_code=201)
def create_topic(topic: Topic, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    topic.user_id = user.id
    category = cs.get_by_id(topic.category_id)

    if category is None:
        return NotFound("This category does not exist!")
    
    if category.is_locked():
        return Forbidden("The category is locked and does not accept any further topics!")
    
    if not category.is_private() or cs.user_has_write_access(category.id, user.id):
        ts.create(topic)
        return f"Topic {topic.id} created successfully!"
    else:
        return Forbidden("You don't have writing access for the category of this topic!")


    
@topics_router.post("/{topic_id}/replies",status_code=201)
def create_reply(topic_id: int, x_token: str = Header(), content: str = Body(...)):
    user = get_user_or_raise_401(x_token)
    topic = ts.get_by_id(topic_id)

    if topic is None:
        return NotFound("This topic does not exist!")
   
    category = cs.get_by_id(topic.category_id)

    if category.is_locked() or topic.is_locked():
        return Forbidden("The topic is locked and does not accept any further replies!")
    
    if not category.is_private() or cs.user_has_write_access(category.id, user.id):
        reply_id = rs.create(topic_id, user.id, content)
        return f"Reply {reply_id} created successfully"
    else:
        return Forbidden("You don't have writing access for the category of this topic!")


@topics_router.put("/{topic_id}/bestreply")
def choose_best_reply(
    topic_id: int, reply_id: int = Body(...), x_token: str = Header()
):
    user = get_user_or_raise_401(x_token)
    topic = ts.get_by_id(topic_id)
    
    if user.id != topic.user_id:
        return Forbidden(
            "You are not the author of this topic and can't choose the best reply!"
        )
    

    if not ts.exists(topic_id):
        return NotFound("This topic does not exist!")
    
    reply = rs.get_by_id(reply_id)
    if not reply:
        return NotFound("This reply does not exist!")
    
    if reply.topic_id != topic_id:
        return BadRequest("This reply is not part of this topic!")
    else:
        ts.choose_best_reply(topic_id, reply_id)

    return f"You have successfully chosen the reply ID{reply_id} as the best!"


@topics_router.put("/{id}/status")
def change_status(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if not user.is_admin():
        return Forbidden("You are not admin!")
    if not ts.exists(id):
        return NotFound("This topic does not exist!")

    topic = ts.change_status(id)

    return f"Topic {id} is {topic.status}."
