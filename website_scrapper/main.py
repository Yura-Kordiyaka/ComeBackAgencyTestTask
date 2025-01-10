import asyncio
from scrapper.main_scrapper import Scraper
from settings import settings


async def main():
    scraper = Scraper(settings.BASE_URL, settings.CSS_SELECTOR)
    try:
        await scraper.scrape()
    except Exception as e:
        print(f"Scraping failed: {e}")


if __name__ == '__main__':
    asyncio.run(main())
