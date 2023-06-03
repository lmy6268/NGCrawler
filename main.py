import naver_crawler as crawler

#초기화
driver = crawler.initDriver()
keywords = ["제주여행", "여행인물", "부산여행인물"]  # 검색할 키워드 목록을 작성
baseUrl = "https://search.naver.com/search.naver?where=image&sm=tab_jum&query="
FORDER_PATH = "/Users/kyuyeonlee/Desktop/naverImg"  # 사진을 저장할 경로

#크롤링 진행
crawler.doCrawl(driver,keywords,baseUrl,FORDER_PATH)