#!/usr/bin/python
from asyncio import *

import debugger
from Crawler import Crawler

debugger.enabled = True
startUrl = 'https://thetrove.net/index.html'


async def main(initialUrl):
    crawler = Crawler()
    await crawler.run(initialUrl)


if __name__ == '__main__':
    run(main(startUrl))