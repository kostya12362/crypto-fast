from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import json
from resources import ManagerSessionCookie
import pickle
from resources import utils
from settings import config

# class CheckOperationMiddleware(BaseHTTPMiddleware):
#     PATH_CHECK = (
#         '/auth/login/email',
#         '/send-to-wallet'
#     )
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.redis = config.redis_db
#
#     async def dispatch(self, request: Request, call_next):
#         if request.url.path and request.method in ('POST', 'DELETE', 'PUT'):
#             if not request.headers.get('authorization'):
#                 # await utils.backend_memory.update(session_id='123', data=request.__dict__)
#                 print(request.__dict__)
#                 await self.redis.set(1, request.__dict__, ex='1')
#                 response = await call_next(request)
#
#                 return response
            #         data = request.json()
        #         print(data)
        #         response = await call_next(request)
        #     else:
        #         response = await call_next(request)
        # else:
        #     response = await call_next(request)
        # return response

        # response = await call_next(request)
        # return response
