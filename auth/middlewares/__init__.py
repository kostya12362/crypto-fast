from fastapi import FastAPI
from .response_time import ResponseTimeMiddleware
# from .check_operation import CheckOperationMiddleware
from .session_cookie import SessionCookieMiddleware
from fastapi.middleware.cors import CORSMiddleware


def setup_middlewares(app: FastAPI):
    app.add_middleware(SessionCookieMiddleware)
    app.add_middleware(ResponseTimeMiddleware)
    # app.add_middleware(CheckOperationMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
