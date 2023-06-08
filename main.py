from image_download_api import NGCrawler
import separate

if __name__ == "__main__":
    crawler = NGCrawler(limit=450)
    crawler.startToCrawl()
    separate.do_seperate()
    