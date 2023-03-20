from scraper_factory import TheChunkyChefScraperFactory

if __name__ == "__main__":
    print("App: Launched")
    factory = TheChunkyChefScraperFactory()
    scraper = factory.create()
    scraper.get_recipes()
    scraper.process_recipes(scraper.get_descriptions)
