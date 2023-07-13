import asyncio
import aiohttp
import uuid
import random
from string import digits, ascii_letters
import ds

cookies = {
    "ltoken_v2": "v2_WZtZFQX7zMfTkct6X3SJnXbEiI8P80zNKprnU5LeYn4xcJ3Z8j3BpqPL6rxMX71zCnnXUhQEKxlUJj0pDoxkTJnxbOeDKPAESA==",
    "ltmid_v2": "0atbtlb27b_mhy"
}


async def main():
    # device_id: str = "".join(str(uuid.uuid4()).split("-")).upper() # str(uuid.uuid4()).upper() # "".join(str(uuid.uuid4()).split("-")).upper()
    device_id: str = ''.join(random.choices(ascii_letters + digits, k=32))
    print(device_id)
    print(len(device_id))
    post_data = {
        "role_id": "117373444",
        "server": "prod_gf_cn"
    }
    headers = {
        "x-rpc-app_version": "2.44.1",
        "x-rpc-client_type": "5",
        "x-rpc-device_id": device_id,
        "X-Requested-With": "com.mihoyo.hyperion",
        "Origin": "https://api-takumi-record.mihoyo.com",
        "Host": "api-takumi.mihoyo.com",
        "Referer": "https://webstatic.mihoyo.com",
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; M2101K9C Build/TKQ1.220829.002; wv) " +
            "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/108.0.5359.128 Mobile Safari/537.36 miHoYoBBS/2.44.1",
        "DS": ds.get_ds(post_data)
    }
    async with aiohttp.ClientSession(cookies=cookies) as session:  # type: ignore
        async with session.get('https://api-takumi-record.mihoyo.com/game_record/app/hkrpg/api/index', params=post_data, headers=headers) as response:
            data = await response.text()
            print(data)
    

asyncio.run(main())
