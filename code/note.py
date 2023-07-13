import asyncio
import aiohttp

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://bbs-api.miyoushe.com/post/wapi/getNewsList?gids=6&type=3') as response:
            data = await response.json()
            print(data)
loop = asyncio.get_event_loop()
res = loop.run_until_complete(main())