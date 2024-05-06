from fastapi import APIRouter, Query, Header, Body
from data.models import Category, CategoryResponseModel
from services import category_service as cs
from services import topic_service as ts
from common.auth import get_user_or_raise_401
from common.responses import Forbidden, NotFound, BadRequest, Unauthorized


categories_router = APIRouter(prefix="/categories")


@categories_router.get("/")
def get_categories(
    name: str | None = None,
    privacy: str | None = Query(default=None, regex="^(public|private)$"),
    status: str | None = Query(default=None, regex="^(unlocked|locked)$"),
):

    return cs.all(name, privacy, status)


@categories_router.get("/{id}")
def get_category_by_id(id: int, x_token: str = Header()):
    category = cs.get_by_id(id)
    user = get_user_or_raise_401(x_token)

    if category is None:
        return NotFound("This category does not exist!")
    
    if not category.is_private() or cs.user_has_read_access(id, user.id):
        return CategoryResponseModel(
        category=category, topics=ts.get_by_category(category.id)
        )
    else: 
        return Unauthorized("You don't have access to this category!")
    


@categories_router.post("/", status_code=201)
def create_category(category: Category, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if not user.is_admin():
        return Forbidden("You are not admin!")

    cs.create(category)

    return f"Category {category.id} created successfully!"

@categories_router.put("/{id}/privacy")
def change_privacy_status(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if not user.is_admin():
        return Forbidden("You are not admin!")
    category = cs.get_by_id(id)
    if category is None:
        return NotFound("This category does not exist!")

    category = cs.change_privacy(id)

    return f"Privacy status changed to {category.privacy} for category {category.name}!"


@categories_router.put("/{id}/status")
def change_accessibility_status(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if not user.is_admin():
        return Forbidden("You are not admin!")
    category = cs.get_by_id(id)
    if category is None:
        return NotFound("This category does not exist!")

    category = cs.change_accessibility(id)

    return f"Status changed to {category.status} for category {category.name}!"

@categories_router.put("/{category_id}/users/{user_id}")
def give_user_access(category_id:int, user_id:int, x_token: str = Header(), access_type: str | None = Body(...)):
    user = get_user_or_raise_401(x_token)

    if not user.is_admin():
        return Forbidden("You are not admin!")
    
    category = cs.get_by_id(category_id)
    if category is None:
        return NotFound("This category does not exist!")
    
    if not category.is_private():
        return BadRequest("The category is public! No need to give explicit access.")
    
    result = cs.give_user_access(category_id, user_id, access_type)

    return result

@categories_router.delete("/{category_id}/users/{user_id}")
def revoke_user_access(category_id: int, user_id: int, x_token: str = Header()):

    user = get_user_or_raise_401(x_token)

    if not user.is_admin():
        return Forbidden("You are not admin!")
    
    category = cs.get_by_id(category_id)
    if category is None:
        return NotFound("This category does not exist!")
    
    return cs.revoke_user_access(category_id, user_id)

    







