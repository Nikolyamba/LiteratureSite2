import uvicorn
from fastapi import FastAPI

from backend.api.user import u_router

app = FastAPI

app.include_router(u_router, prefix='/api')

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)