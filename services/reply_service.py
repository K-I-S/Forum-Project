from data.database import read_query, insert_query, update_query
from data.models import Reply, ReplyResponseModel
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


def create_user_vote(user_id: int, vote_type: str, reply_id: int):

    insert_query(
        "insert into user_votes (user_id, vote_type, replies_id) values (?,?,?)",
        (user_id, {1 if vote_type == "up" else 0}, reply_id),
    )


# def vote_exists(user_id: int, reply_id: int):
#     """Checks if the user has already voted on this reply -> returns bool"""
#     return any(
#         read_query(
#             "select id, user_id, vote_type, replies_id from user_votes where user_id = ? and replies_id = ?",
#             (user_id, reply_id),
#         )
#     )


def get_user_vote(user_id: int, reply_id: int):

    data = read_query(
        "select id, user_id, vote_type, replies_id from user_votes where user_id = ? and replies_id = ?",
        (user_id, reply_id),
    )

    return (Reply.from_query_result(*row) for row in data)


def update_vote(id: int, vote_type: str):
    return update_query(
        "update user_votes set vote_type = ? where id = ?",
        ({1 if vote_type == "up" else 0}, id),
    )
