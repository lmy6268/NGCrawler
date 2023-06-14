from image_download_api import NGCrawler
import separate

if __name__ == "__main__":
    crawler = NGCrawler(search_on_google=False,search_on_naver_full=True,limit=450)
    crawler.startToCrawl()
    separate.do_seperate()
    