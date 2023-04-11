from __future__ import annotations
import sys
import time
from scraper_factory import createScraperFactory, ScraperType

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("2 arguments required: (scraper_type, start_page_index)")
        exit()

    scraper_type = ScraperType(sys.argv[1])
    start_page_index = int(sys.argv[2])

    print("App: Launched")
    start = time.perf_counter()
    factory = createScraperFactory(scraper_type)
    scraper = factory.create()
    scraper.scrape(start_page_index)
    end = time.perf_counter()
    print(f"{end - start:0.4f} seconds")
