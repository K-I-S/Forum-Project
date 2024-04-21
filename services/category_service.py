from data.database import read_query, insert_query
from data.models import Category


def all(name: str = None, privacy: str = None, status: str = None):
    sql = "select id, name, description, is_locked, is_private from categories"

    where_clauses = []
    if name:
        where_clauses.append(f"name LIKE '%{name}%' ")
    if privacy:
        where_clauses.append(f"is_private = {1 if privacy == 'private' else 0}")
    if status:
        where_clauses.append(f"is_locked = {1 if status == 'locked' else 0}")

    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)

    return (Category.from_query_result(*row) for row in read_query(sql))


def get_by_id(id: int):
    data = read_query(
        "select id, name, description, is_locked, is_private from categories where id = ?",
        (id,),
    )

    return next((Category.from_query_result(*row) for row in data), None)


def exists(id: int):
    return any(
        read_query(
            "select id, name, description, is_locked, is_private from categories where id =?",
            (id,),
        )
    )
