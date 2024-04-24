from fastapi import APIRouter, Query, Body, Header
from data.models import Topic, TopicResponseModel
from services import topic_service as ts
from services import reply_service as rs
from services import category_service as cs
from datetime import datetime
from common.auth import get_user_or_raise_401


topics_router = APIRouter(prefix="/topics")


@topics_router.get("/")
def get_topics(
    title: str | None = None,
    status: str | None = Query(default=None, regex="^(unlocked|locked)$"),
):
    return ts.all(title, status)


@topics_router.get("/{id}")
def get_by_id(id: int):
    topic = ts.get_by_id(id)

    if topic is None:
        return "there is no such topic"

    return TopicResponseModel(topic=topic, replies=rs.get_by_topic(topic.id))


@topics_router.post("/", status_code=201)
def create_topic(topic: Topic, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    topic.user_id = user.id
    if not cs.exists(topic.category_id):
        return f"Category {topic.category_id} does not exist!"

    ts.create(topic)

    return f"Topic {topic.id} created successfully!"


@topics_router.put("/{topic_id}/bestreply")
def choose_best_reply(topic_id: int, reply_id: int = Body(...)):
    if not ts.exists(topic_id):
        return "No such Topic exists!"
    if not rs.exists(reply_id):
        return "No such reply exists!"

    # check if reply.topic_id = topic_id

    ts.choose_best_reply(topic_id, reply_id)

    return f"You have successfully chosen the best reply {reply_id}!"
