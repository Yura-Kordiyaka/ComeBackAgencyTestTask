from bs4 import BeautifulSoup
from .page_fatcher import PageFetcher
from typing import List, Dict
from .link_filter import LinkFinder
from settings import settings


class ContentParser:
    def __init__(self):
        self.parsed_data = []

    async def parse_page_content(self, url: str, page_fetcher: PageFetcher) -> List[Dict[str, str]]:
        data = await page_fetcher.fetch_page(url)
        soup = BeautifulSoup(data, 'html.parser')
        content_div = soup.find('div', class_='field field-name-body')

        if content_div is None:
            return await self._handle_no_content_div(url)

        parsed_data = self._parse_content_div(url, content_div)
        return parsed_data

    async def _handle_no_content_div(self, url: str) -> List[Dict[str, str]]:
        page_fetcher = PageFetcher()
        link_finder = LinkFinder(settings.CSS_SELECTOR)

        links = await link_finder.find_subpage_links(url, page_fetcher)
        print(f"Found links: {links}")

        return [{'url': url, 'heading': 'unknown', 'text': [], 'links': [link]} for link in links]

    def _parse_content_div(self, url: str, content_div) -> List[Dict[str, str]]:
        parsed_data = []
        self._remove_toc(content_div)

        unknown_texts, unknown_links = [], []
        current_heading = None

        def add_unknown_section():
            nonlocal unknown_texts, unknown_links
            if unknown_texts:
                parsed_data.append({'url': url, 'heading': 'unknown', 'text': unknown_texts, 'links': unknown_links})
                unknown_texts, unknown_links = [], []

        def extract_links(tag):
            return [link['href'] for link in tag.find_all('a', href=True)]

        def process_list(tag):
            items_text = []
            items_links = []
            for li in tag.find_all('li'):
                item_text = li.get_text(strip=True)
                links = extract_links(li)
                if item_text:
                    items_text.append(f"- {item_text}")
                items_links.extend(links)
            return "\n".join(items_text), items_links

        for tag in content_div.find_all(recursive=False):
            if tag.name in ['h2', 'h3']:
                if current_heading:
                    parsed_data.append(current_heading)
                add_unknown_section()

                current_heading = {'url': url, 'heading': tag.get_text(strip=True), 'text': [], 'links': []}

            elif tag.name == 'p':
                text = tag.get_text(strip=True)
                links = extract_links(tag)
                if current_heading:
                    current_heading['text'].append(text)
                    current_heading['links'].extend(links)
                else:
                    unknown_texts.append(text)
                    unknown_links.extend(links)

            elif tag.name == 'ul':
                list_text, list_links = process_list(tag)
                if list_text:
                    if current_heading:
                        current_heading['text'].append(list_text)
                    else:
                        unknown_texts.append(list_text)

                if list_links:
                    if current_heading:
                        current_heading['links'].extend(list_links)
                    else:
                        unknown_links.extend(list_links)

            elif tag.name == 'a':
                href = tag.get('href')
                if href:
                    if current_heading:
                        current_heading['links'].append(href)
                    else:
                        unknown_links.append(href)

        if current_heading:
            parsed_data.append(current_heading)
        add_unknown_section()
        return parsed_data

    def _remove_toc(self, content_div):
        for toc in content_div.find_all(['div', 'form'], class_=['toc', 'toc-responsive', 'toc-desktop', 'toc-menu']):
            toc.decompose()
