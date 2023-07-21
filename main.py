from image_download_api import NGCrawler
import sys
import getopt
import separate
import time

#Translate Cmd line
def translateAndRun(cmd):
    shortOpts = "gnfl:S"
    longOpts = ["Google", "Naver", "Full_Resolution", "Limit", "Show"]
    args, vals = getopt.getopt(cmd, shortOpts, longOpts)
    sog = True
    son = True
    gf = False
    nf = False
    head = True
    limit = 500
    try:
        for arg, val in args:
            if arg in ("-g", "--Google"):  # 구글 안받음.
                sog = False
            if arg in ("-n", "--Naver"):  # 네이버 안받음.
                son = False
            if arg in ("-f", "--Full_Resolution"):  # 고해상도 이미지 다운로드
                gf = True
                nf = True
            if arg in ("-l", "--Limit"):  # 개수 제한
                limit = int(val)
            if arg in ("-S", "--Show"):  # 헤드리스 모드 끄기
                head = False

    except getopt.error:
        print(args)
    if sog!=False or son!=False:
        startTime = time.time()
        crawler = NGCrawler(search_on_google=sog,
                            search_on_naver=son,
                            search_on_google_full=gf,
                            search_on_naver_full=nf,
                            limit=limit,
                            headless = head
                            )
        crawler.startToCrawl()
        separate.do_seperate()
        print(f"elapse time for processing: {time.time()-startTime} ms")

if __name__ == "__main__":
    translateAndRun(sys.argv[1:])
    
