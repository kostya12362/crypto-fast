import json
import re
import os
from auth.settings import rb
from auth.schemas.user import UserCreate

from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from tortoise.transactions import in_transaction
from core.RMQ.models import HeaderRMQ, Message
router = InferringRouter()


@cbv(router)
class AuthViewAPI:

    @router.post('/register')
    async def create_user(self, user: UserCreate):
        async with in_transaction("default") as tconn:
            val = await tconn.execute_query_dict(f'''
                INSERT INTO "user" (email, phone) VALUES ($1, $2) RETURNING email;
            ''', [user.email, '123'])
            print(val)
            message = Message
            message.headers = {'call_task': 'email', 'send_queue': 'sender.settings'}
            message.body = {"kwargs": {"email": "rota199804@gmail.com"}}
            # await rb.send(message=message)
            return val
