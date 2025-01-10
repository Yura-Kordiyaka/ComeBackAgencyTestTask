from bs4 import BeautifulSoup
from typing import List
from .page_fatcher import PageFetcher


class LinkFinder:
    def __init__(self, link_css_selector: str):
        self.link_css_selector = link_css_selector

    async def find_subpage_links(self, url: str, page_fetcher: PageFetcher) -> List[str]:
        html = await page_fetcher.fetch_page(url)
        soup = BeautifulSoup(html, 'html.parser')
        section = soup.find('section', class_=self.link_css_selector)

        if not section:
            print(f"Section with class {self.link_css_selector} not found on {url}")
            return []

        links = section.find_all('a', href=True)
        href_links = [link['href'] for link in links]

        return [self._get_full_url(link) for link in href_links]

    def _get_full_url(self, link: str) -> str:
        if link.startswith('https'):
            return link
        elif link.startswith('/'):
            return 'https://ndis.gov.au/' + link
        return link
