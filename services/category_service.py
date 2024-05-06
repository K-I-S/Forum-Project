from data.database import read_query, insert_query, update_query
from data.models import Category, UserAccess


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

def change_accessibility(id):
    category = get_by_id(id)
    if not category.is_locked():
        update_query("update categories set is_locked = 1 where id = ?", (id,))
        category.status = "locked"
    else:
        update_query("update categories set is_locked = 0 where id = ?", (id,))
        category.status = "unlocked"

    return category

def check_for_access(category_id, user_id):
    data = read_query("select categories_id, users_id, access_type from categories_access where categories_id = ? and users_id = ?", (category_id, user_id))

    return next((UserAccess.from_query_result(*row) for row in data), None)



def give_user_access(category_id: int, user_id: int, access_type: str = None):
    user_access = check_for_access(category_id, user_id)

    if access_type == "write" or access_type is None:
        access_type_value = 1
    elif access_type == "read":
        access_type_value = 0
    else:
        return f"Invalid access_type: please choose between read and write!"

    if user_access is None:
        
            insert_query("insert into categories_access (categories_id, users_id, access_type) values (?,?,?)", (category_id, user_id, access_type_value))
        
            insert_query("insert into categories_access (categories_id, users_id) values (?,?)", (category_id, user_id))
        

    update_query("update categories_access set access_type = ? where categories_id = ? and users_id = ?", ( access_type_value,category_id, user_id))

    return  f"User {user_id} has been granted '{"write" if access_type_value else "read"}' access!"



def revoke_user_access(category_id: int, user_id):
    user_access = check_for_access(category_id, user_id)

    if user_access is None:
        return f"The user does not have access to this category!"
    else: 
        update_query("delete from categories_access where categories_id = ? and users_id = ?", (category_id, user_id))

    return f"The access of user with ID {user_id} has been successfully revoked"

def user_has_read_access(category_id, user_id):
    return any(read_query("select categories_id, users_id, access_type from categories_access where categories_id = ? and users_id = ?", (category_id, user_id)))