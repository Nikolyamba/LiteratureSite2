import uvicorn
from fastapi import FastAPI

from backend.api.author import a_router
from backend.api.book import b_router
from backend.api.comment import c_router
from backend.api.genre import g_router
from backend.api.user import u_router
from backend.logs_api.log import setup_logging
from backend.redis_dir.redis_config import init_redis, close_redis

# setup_logging()

app = FastAPI()

app.include_router(u_router, prefix='/api')
app.include_router(b_router, prefix='/api')
app.include_router(g_router, prefix='/api')
app.include_router(a_router, prefix='/api')
app.include_router(c_router, prefix='/api')

@app.on_event('startup')
async def startup():
    await init_redis()

@app.get('/healthcheck')
async def healthcheck():
    return {'success': True}

@app.on_event('shutdown')
async def shutdown():
    await close_redis()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)