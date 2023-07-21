from image_download_api import NGCrawler
import sys
import separate
import time

if __name__ == "__main__":
    startTime = time.time()
    crawler = NGCrawler()
    crawler.startToCrawl()
    separate.do_seperate()

    print(f"elapse time for processing: {time.time()-startTime} ms")