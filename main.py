from image_download_api import NGCrawler


if __name__ == "__main__":
    crawler = NGCrawler(limit=100)
    crawler.startToCrawl()


    