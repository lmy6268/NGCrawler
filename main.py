import naver_crawler as crawler
import os 

"""
실제로 크롤링이 진행되는 파이썬 파일
"""

driver = crawler.initDriver()
keywords = [f"{i} 인생샷" for i in ["해운대", "부산 카페", "광안리", "서울 카페", "제주 카페",
                                 "남산", "경주", "제주 오름",  "부산 여행", "강릉 여행", "태안 여행", "경주 여행", 
                                 "제주도 인스타", "부산 인스타", "경주 인스타", "서울 인스타",
                                 "파리 인스타", "에펠탑", "서울숲", "뉴욕 인스타", "일본 인스타"
                                 ]]  # 검색할 키워드 목록을 작성
baseUrl = "https://search.naver.com/search.naver?where=image&sm=tab_jum&query="

FORDER_PATH = "./naverImg"  # 사진을 저장할 경로

#다운받을 폴더 생성
if not os.path.exists(FORDER_PATH):
    os.mkdir(FORDER_PATH)

#크롤링 진행
crawler.doCrawl(driver,keywords,baseUrl,FORDER_PATH)