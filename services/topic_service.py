from data.database import read_query, insert_query, update_query
from data.models import Topic
from datetime import datetime


def all(title: str = None, status: str = None):
    sql = "select id, title, category_id, user_id, date, description, is_locked, best_reply from topics"

    where_clauses = []
    if title:
        where_clauses.append(f"title LIKE '%{title}%' ")
    if status:
        where_clauses.append(f"is_locked = {1 if status == 'locked' else 0}")

    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)

    return (Topic.from_query_result(*row) for row in read_query(sql))


def get_by_id(id: int):
    data = read_query(
        "select id, title, category_id, user_id, date, description, is_locked, best_reply from topics where id = ?",
        (id,),
    )

    return next((Topic.from_query_result(*row) for row in data), None)


def get_by_category(category_id: int):

    data = read_query(
        "select id, title, category_id, user_id, date, description, is_locked, best_reply from topics where category_id = ?",
        (category_id,),
    )

    return (Topic.from_query_result(*row) for row in data)


def exists(id: int):
    return any(
        read_query(
            "select id, title, category_id, user_id, date, description, is_locked, best_reply from topics where id = ?",
            (id,),
        )
    )


def create(topic: Topic):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    generated_id = insert_query(
        "insert into topics (title, category_id, user_id, date,  description) values(?,?,?,?,?)",
        (
            topic.title,
            topic.category_id,
            topic.user_id,
            current_time,
            topic.description,
        ),
    )

    topic.id = generated_id

    return topic


def choose_best_reply(topic_id: int, reply_id: int):
    return update_query(
        "update topics set best_reply = ? where id = ?", (reply_id, topic_id)
    )
