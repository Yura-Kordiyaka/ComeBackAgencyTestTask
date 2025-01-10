from pathlib import Path
from settings import settings
from scrapper.csv_writer import CSVWriter
from .link_filter import LinkFinder
from .page_fatcher import PageFetcher
from .content_parser import ContentParser


class Scraper:
    def __init__(self, base_url: str, link_css_selector: str):
        self.base_url = base_url
        self.link_css_selector = link_css_selector
        self.visited_links = set()
        self.page_fetcher = PageFetcher()
        self.link_finder = LinkFinder(link_css_selector)
        self.content_parser = ContentParser()

    async def scrape(self):
        self.visited_links.add(self.base_url)
        sub_pages = await self.link_finder.find_subpage_links(self.base_url, self.page_fetcher)
        if not sub_pages:
            print("No subpages found.")
            return

        output_dir = Path(settings.PATH_OUTPUT_FILE)
        output_dir.mkdir(parents=True, exist_ok=True)
        for idx, sub_page in enumerate(sub_pages):
            print(f"Processing subpage {sub_page}")
            parsed_data = await self.content_parser.parse_page_content(sub_page, self.page_fetcher)

            if not parsed_data:
                print(f"No data parsed from {sub_page}")
                continue

            file_name = output_dir / f"page_{sub_page.split('/')[-1]}.csv"
            csv_writer = CSVWriter(file_name)
            csv_writer.save_to_csv(parsed_data)
            print(f"Data from {sub_page} saved to {file_name}")

        print("All subpages processed.")
