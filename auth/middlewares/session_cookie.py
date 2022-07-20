from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from resources import ManagerSessionCookie


class SessionCookieMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        sc = ManagerSessionCookie(request)
        request = await sc.check_or_create_session()
        response = await call_next(request)
        await sc.add_to_cookie(response)
        return response
