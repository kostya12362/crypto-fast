import asyncio
import uvicorn

from fastapi import FastAPI

from auth.settings import rb
from auth.resources.database import setup_database
from auth.routers import registration


app = FastAPI()
app.include_router(registration.router, prefix='/auth')


@app.on_event("startup")
async def startup_event():
    setup_database(app)
    loop = asyncio.get_event_loop()
    loop.create_task(rb.main_amqp(loop=loop))


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=5004, reload=True)
