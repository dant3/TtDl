import asyncio
from typing import Optional, Tuple

import aiohttp
from aiohttp import ClientResponse

import debugger
from FetchPageResult import FetchPageResult


class HttpClient:
    async def fetch_page(self, url: str) -> FetchPageResult:
        session: aiohttp.ClientSession
        debugger.print("fetch from url=", url)
        async with aiohttp.ClientSession() as session:
            # async with aiohttp.ClientTimeout(10):
            async with session.get(url) as response:
                if response.status != 200:
                    debugger.print("url ", url, "response code", response.status)
                    return None
                    # raise Exception("Url %s failed! Response code %s" % (url, response.status))
                return FetchPageResult(url, response, await response.text())
