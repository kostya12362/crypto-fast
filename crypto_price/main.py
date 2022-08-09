import uvicorn

from fastapi import FastAPI
from routers import price
from models import setup_database
from crawler import setup_crawler

app = FastAPI()
app.include_router(price.router, prefix='/price')


@app.on_event("startup")
async def startup_event():
    setup_database(app)
    setup_crawler()


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=5006,
        reload=True
    )
