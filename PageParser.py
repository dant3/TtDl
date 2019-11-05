from bs4 import BeautifulSoup as bS
from requests.compat import urljoin

def parse_links(html: str, baseUrl: str) -> list:
    soup = bS(html, 'html.parser')
    dirs = soup.find_all('tr', class_='litem dir')

    return [urljoin(baseUrl, td.find('a').get('href')) for td in dirs]
