import json
from typing import List, Union
from fastapi import Depends, Response, status, Request, WebSocket, WebSocketDisconnect

from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

from schemas import (
    SessionData,
    HistoryLoginSchema,
    # PhoneSchema,
    # AddAntiPhishingSchema,
    # UpdateAntiPhishingSchema,
)

from resources import utils

from models.history_login import HistoryLogin
from models.user import User

router = InferringRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        print(self.active_connections)
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@cbv(router)
class SecurityAPIView:

    @router.get('/history_login',)
    async def history_login(self, user: SessionData = Depends(utils.verifier_cookie)) -> List:
        result = await HistoryLogin.select_history_login(user[0].user_id)
        _result = list()
        for item in result:
            _hl = HistoryLoginSchema(**item)
            if await utils.backend_memory.read(_hl.detail[0].session_id):
                _hl.detail[0].active = True
            _result.append(_hl)
        return _result

    @router.get("/add_operation")
    async def check_operation(self, id_operation: int, secret_operation: Union[str, None]):
        if not secret_operation:
            # todo create new operation
            print('CREATE secret')
        else:
            print("Check valid ")
        return True