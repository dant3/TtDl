from asyncio import Queue, Semaphore

import PageParser
import debugger
from HttpClient import HttpClient
from VisitedUrlCache import VisitedUrlCache


class Crawler:
    def __init__(self):
        self.visited: VisitedUrlCache = VisitedUrlCache()
        self.httpClient: HttpClient = HttpClient()
        self.semaphore = Semaphore(10)

    async def run(self, initialUrl: str):
        from asyncio import create_task, gather

        urls = [initialUrl]
        while not len(urls) == 0:
            debugger.print("Processing new url hunk: ", urls)
            tasks = [create_task(self.__visit_task(url)) for url in urls]
            urls = Crawler.__analyze_outcomes(await gather(*tasks, return_exceptions=True))
            debugger.print("new url bunch: ", urls)

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
        html = await self.httpClient.fetch_page(url)
        return PageParser.parse_links(html, url)

