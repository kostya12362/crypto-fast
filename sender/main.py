import uvicorn

from fastapi import FastAPI
from routers import sender

app = FastAPI()
app.include_router(sender.router, prefix='/send')


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=5005,
        reload=True
    )
