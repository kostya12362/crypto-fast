from schemas import (OpenID,)


class BaseAuth:

    def __init__(self, app_id: str = None, app_secret: str = None):
        self.app_id = app_id
        self.app_secret = app_secret

    def create(self, ):
        pass

    def verify(self):
        pass

    def login(self, data):
        pass

    def update(self):
        pass
