from fastapi import APIRouter, Query
from data.models import Category, CategoryResponseModel
from services import category_service as cs
from services import topic_service as ts


categories_router = APIRouter(prefix="/categories")


@categories_router.get("/")
def get_categories(
    name: str | None = None,
    privacy: str | None = Query(default=None, regex="^(public|private)$"),
    status: str | None = Query(default=None, regex="^(unlocked|locked)$"),
):

    return cs.all(name, privacy, status)


@categories_router.get("/{id}")
def get_category_by_id(id: int):
    category = cs.get_by_id(id)

    if category is None:
        return "there is no such category"
    else:
        return CategoryResponseModel(
            category=category, topics=ts.get_by_category(category.id)
        )


@categories_router.post("/", status_code=201)
def create_category(category: Category):
    cs.create(category)

    return f"Category {category.id} created successfully!"
