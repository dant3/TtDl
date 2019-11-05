import asyncio

import aiohttp

import debugger


class HttpClient:
    async def fetch_page(self, url: str) -> str:
        session: aiohttp.ClientSession
        debugger.print("fetch from url=", url)
        async with aiohttp.ClientSession() as session:
            # async with aiohttp.ClientTimeout(10):
            async with session.get(url) as response:
                if response.status != 200:
                    debugger.print("url ", url, "response code", response.status)
                    raise Exception("Url %s failed! Response code %s" % (url, response.status))
                return await response.text()
