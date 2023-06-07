from image_download_api import NGCrawler

if __name__ == "__main__":
    crawler = NGCrawler(search_on_google=True,search_on_naver=True,limit=500)
    crawler.startToCrawl()
