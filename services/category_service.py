from data.database import read_query, insert_query, update_query
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


def create(category: Category):
    generated_id = insert_query(
        "insert into categories (name, description) values(?,?)",
        (category.name, category.description),
    )

    category.id = generated_id

    return category

def change_privacy(id: int):
    category = get_by_id(id)
    if not category.is_private():
        update_query("update categories set is_private = 1 where id = ?", (id,))
        category.privacy = "private"
    else:
        update_query("update categories set is_private = 0 where id = ?", (id,))
        category.privacy = "public"
    return category

