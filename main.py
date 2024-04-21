from fastapi import FastAPI
from routers.message import message_router


app = FastAPI()
app.include_router(message_router)

# if __name__ == '__main__':
#     uvicorn.run(app='main:app', host='127.0.0.1', port=8001)