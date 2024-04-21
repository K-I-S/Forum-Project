from data.database import read_query, insert_query
from data.models import Reply
from datetime import datetime


def get_by_topic(topic_id: int):
    data = read_query(
        "select id, user_id, date, topic_id, content from replies where topic_id = ?",
        (topic_id,),
    )

    return (Reply.from_query_result(*row) for row in data)


def get_by_id(id: int):
    data = read_query(
        "select id, user_id, date, topic_id, content from replies where id = ?", (id,)
    )

    return next((Reply.from_query_result(*row) for row in data), None)


def exists(id: int):
    return any(
        read_query(
            "select id, user_id, date, topic_id, content from replies where id = ?",
            (id,),
        )
    )


def create(reply: Reply):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    generated_id = insert_query(
        "insert into replies (user_id, date, topic_id, content) values(?,?,?,?)",
        (reply.user_id, current_time, reply.topic_id, reply.content),
    )

    reply.id = generated_id

    return reply
