import httpx
import json
from typing import Optional
from models.coin import Coin
from tortoise import transactions
from pydantic import BaseModel
from datetime import datetime


class CoinMarketCapExtract:
    class Item(BaseModel):
        id: int = None
        name: str
        symbol: str
        slug: str
        tags: Optional[str] = None
        cmc_rank: int
        date_added: Optional[datetime]
        is_active: int
        prices: Optional[str]

    def __init__(self):
        self.start_url = 'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?' \
                         'start=1&limit=10000&sortBy=market_cap&' \
                         'sortType=desc&convert=USD&cryptoType=all&tagType=all&audited=false' \
                         '&aux=ath,atl,high24h,low24h,num_market_pairs,cmc_rank,date_added,max_supply,' \
                         'circulating_supply,total_supply,volume_7d,volume_30d,volume_60d'

    async def __call__(self, *args, **kwargs):
        return await self.get_data()

    async def get_data(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(url=self.start_url)
            return await self.save_data(json.loads(response.text)['data']['cryptoCurrencyList'])

    async def save_data(self, data: list):
        async with transactions.in_transaction('default') as conn:
            _d = list()
            for item in data:
                _i = self.Item(**{
                    'id': None,
                    'name': item['name'],
                    'symbol': item['symbol'],
                    'slug': item['slug'],
                    'tags': None,
                    'cmc_rank': item['cmcRank'],
                    'date_added': datetime.strptime(item['dateAdded'], "%Y-%m-%dT%H:%M:%S.%fZ"),
                    'is_active': item['isActive'],
                    'prices': json.dumps(item['quotes'][0])
                })
                _d.append(tuple(_i.dict().values()))
            start = datetime.now()
            val = await conn.execute_query_dict('''
                INSERT INTO "coin" (
                    name, symbol, slug, tags, cmc_rank, date_added, is_active, prices
                )
                (SELECT
                    r.name, r.symbol, r.slug, r.tags, r.cmc_rank, r.date_added, r.is_active, r.prices
                 FROM
                    unnest($1::coin[]) as r
                )
                RETURNING id
            ''', (_d,))
            print((datetime.now() - start).total_seconds())