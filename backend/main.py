import uvicorn
from fastapi import FastAPI

from backend.api.user import u_router
from backend.redis.redis_config import init_redis, close_redis

app = FastAPI()

app.include_router(u_router, prefix='/api')

@app.on_event('startup')
async def startup():
    await init_redis()

@app.on_event('shutdown')
async def shutdown():
    await close_redis()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)