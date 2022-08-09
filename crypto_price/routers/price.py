import json

import requests
import asyncio
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from crawler.base import CoinMarketCapExtract

router = InferringRouter()


@cbv(router)
class SendAPIView:
    cmc = CoinMarketCapExtract()
    # binacne = BinanceExtract()

    @router.get('/list')
    async def get_price(self):
        # data = requests.get(url='https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH&tsyms=USD,EUR')
        # headers = {
        #     "authority": "http-api.livecoinwatch.com",
        #     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        #     "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6",
        #     "Postman-Token": "c8884bf6-3dd9-4036-87a4-6914ce1d471e",
        #     "Host": "http-api.livecoinwatch.com",
        # }
        # headers = {
        #     'authority': 'http-api.livecoinwatch.com',
        #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        #     'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6',
        #     'cache-control': 'no-cache',
        #     'cookie': '_ga=GA1.2.1009516577.1658785134; _gid=GA1.2.144224379.1658785134',
        #     'pragma': 'no-cache',
        #     'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        #     'sec-ch-ua-mobile': '?0',
        #     'sec-ch-ua-platform': '"macOS"',
        #     'sec-fetch-dest': 'document',
        #     'sec-fetch-mode': 'navigate',
        #     'sec-fetch-site': 'none',
        #     'sec-fetch-user': '?1',
        #     'upgrade-insecure-requests': '1',
        #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        # }
        # url = "https://http-api.livecoinwatch.com/coins?offset=10000&limit=100&sort=rank&order=ascending&currency=USD&platforms="
        # data = requests.get(url=url, headers=headers)
        data = await self.cmc()
        return data

    @router.get('/price/binance')
    async def get_price_binance(self):
        return True