from aiohttp import ClientResponse

import debugger


class FetchPageResult:
    def __init__(self, url: str, response: ClientResponse, responseText: str):
        self.initialUrl = url
        self.originUrl = str(response.url)
        self.html = responseText

    def getUrl(self) -> str:
        return self.originUrl if self.originUrl is not None else self.initialUrl
