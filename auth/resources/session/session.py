from uuid import (
    UUID,
    uuid4,
)
from typing import (
    Any,
    Tuple,
    Optional,
    Union,
)
from fastapi import (
    Response,
    Request,
)

from user_agents import parse

from resources.utils import utils
from schemas import SessionData, Device, GeoLocation


class ManagerSessionCookie:
    """
        this method class using only session_cookie middlewares
        1) method "_check" detect session and check in Redis
            if not in redis:
                create new session and save to Redis
                - user_id = None
        2) after get response in middleware call method "add_to_cookie"
        :return example in Redis
            uuid[key]: {
              "device":{
                "browser":"Other",
                "version":"",
                "os_system":"Other"
              },
              "location":{
                "country":"Ukraine",
                "city":"Kyiv",
                "lat":50.4333,
                "long":30.5167
              },
              "ip_address":"46.173.155.92",
              "init_datetime":1.655912078565081E9,
              "anonymous":false,
              "user_id":18
            }[value]
    """

    def __init__(self, request: Request):
        self.request: Request = request
        self.session: Optional[UUID] = None

    async def _check(self) -> bool:
        try:
            self.session = utils.cookie_session(self.request)
            if await utils.backend_memory.read(self.session):
                return True
        except Exception:
            return False

    async def check_or_create_session(self) -> Request:
        if not await self._check():
            await self._new_session_create()
        utils.cookie_session.attach_id_state(request=self.request, session_id=self.session)
        return self.request

    async def _new_session_create(self) -> Any:
        """
            :returns: - create new session
                      - save to Redis
            todo add logger and update request.client.host + Exception

        """
        device = await self.__detect_device(self.request)
        location, ip_address = await self.__detect_location(self.request)
        data = SessionData(
            device=device,
            ip_address=ip_address,
            location=location
        )
        if not self.session:
            self.session = uuid4()
        await utils.backend_memory.create(self.session, data)

    async def add_to_cookie(self, response: Response):
        if not await self._check():
            utils.cookie_session.attach_to_response(response, self.session)

    @staticmethod
    async def __detect_location(request: Request) -> Tuple[GeoLocation, str]:
        """
            detect IP address and geo location (using geoplugin)
            :param request:
            :returns: GeoLocation, ip_address
            todo update request.client.host
        """
        ip_address = '46.173.155.92'  # request.client.host,
        response = await utils.custom_make_request(endpoint='ip-detail', parameters={'ip_address': ip_address})
        return GeoLocation(
            country=response['geoplugin_countryName'],
            city=response['geoplugin_city'],
            lat=response['geoplugin_latitude'],
            long=response['geoplugin_longitude'],
        ), ip_address

    @staticmethod
    async def __detect_device(request: Request) -> Union[Device]:
        """
            :param request:
            :return: Device
        """
        user_agents = request.headers.get('user-agent')
        if user_agents:
            _ua = parse(user_agents)
            return Device(
                browser=_ua.browser.family,
                version=_ua.browser.version_string,
                os_system=_ua.os.family,
            )
