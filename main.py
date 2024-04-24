from fastapi import FastAPI
from routers.users import users_router
from routers.categories import categories_router
from routers.topics import topics_router
from routers.replies import replies_router
from routers.message import message_router
import uvicorn

app = FastAPI()
app.include_router(users_router)
app.include_router(categories_router)
app.include_router(topics_router)
app.include_router(replies_router)
app.include_router(message_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8001)