import asyncio
from crawler.base import CoinMarketCapExtract


async def async_main():
    count = 0
    while True:
        await CoinMarketCapExtract()()
        # count += 1
        # print(count)


def setup_crawler():
    asyncio.create_task(async_main())
    # asyncio.run(async_main())
