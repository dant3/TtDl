from asyncio import Queue, Semaphore
from asyncio.futures import Future
from typing import Any

import PageParser
import debugger
from FetchPageResult import FetchPageResult
from HttpClient import HttpClient
from VisitedUrlCache import VisitedUrlCache


class Crawler:
    def __init__(self):
        self.visited: VisitedUrlCache = VisitedUrlCache()
        self.httpClient: HttpClient = HttpClient()
        self.semaphore = Semaphore(10)

    async def run(self, initialUrl: str):
        await self.fetch_urls([initialUrl])

    async def fetch_urls(self, urls: list):
        from asyncio import create_task, gather, as_completed
        debugger.print("Processing new url hunk: ", urls)
        tasks = [create_task(self.__visit_task(url)) for url in urls]
        for task_outcome in as_completed(tasks):
            result = await task_outcome  # The 'await' may raise.
            debugger.print("next hunk: ", result)
            if len(result) != 0:
                await self.fetch_urls(result)

    @staticmethod
    def __analyze_outcomes(outcomes: list) -> list:
        flat_list = []
        for outcome in outcomes:
            if isinstance(outcome, Exception):
                raise outcome
            else:
                for item in outcome:
                    flat_list.append(item)
        return flat_list

    async def __visit_task(self, url: str) -> list:
        async with self.semaphore:
            return await self.__visit_url_impl(url)

    async def __visit_url_impl(self, url: str) -> list:
        debugger.print("visiting url=", url)
        self.visited.add(url)
        return self.visited.filter(await self.__fetch_url_links(url))

    async def __fetch_url_links(self, url: str) -> list:
        result: FetchPageResult = await self.httpClient.fetch_page(url)
        if result is None:
            return []
        else:
            return PageParser.parse_links(result.html, result.getUrl())

