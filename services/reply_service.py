from data.database import read_query, insert_query, update_query
from data.models import Reply, ReplyView, UserVote
from datetime import datetime


def get_by_topic(topic_id: int):
    data = read_query(
        """
    SELECT 
        r.id, r.user_id, r.date, r.topic_id, r.content,
        COUNT(CASE WHEN uv.vote_type = 1 THEN 1 END) AS upvotes,
        COUNT(CASE WHEN uv.vote_type = 0 THEN 1 END) AS downvotes
    FROM 
        replies r
    LEFT JOIN 
        user_votes uv ON r.id = uv.replies_id
    WHERE 
        r.topic_id = ?
    GROUP BY 
        r.id
    """,
        (topic_id,),
    )
    return (ReplyView.from_query_result(*row) for row in data)


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


def create(topic_id: int, user_id: int, content: str):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    reply_id = insert_query(
        "insert into replies (user_id, date, topic_id, content) values(?,?,?,?)",
        (user_id, current_time, topic_id, content),
    )


    return reply_id


def create_user_vote(user_id: int, vote_type: str, reply_id: int):
    vote_value = 1 if vote_type == "up" else 0

    insert_query(
        "insert into user_votes (user_id, vote_type, replies_id) values (?,?,?)",
        (user_id, vote_value, reply_id),
    )


def get_user_vote(user_id: int, reply_id: int):

    data = read_query(
        "select id, user_id, vote_type, replies_id from user_votes where user_id = ? and replies_id = ?",
        (user_id, reply_id),
    )

    return next((UserVote.from_query_result(*row) for row in data), None)


def update_vote(id: int, vote_type: str):
    vote_value = 1 if vote_type == "up" else 0

    return update_query(
        "update user_votes set vote_type = ? where replies_id = ?",
        (vote_value, id),
    )
