import naver_image_api as api
import os 

"""
실제로 크롤링이 진행되는 파이썬 파일
"""

driver = api.initDriver()

keywords = [
    "부산 여행 인생샷", "광안리 혼자 인스타", "용산공원 인스타 사진", "강릉 여행 인스타 사진",
    "행궁동 인스타 사진", "제주 오름 인스타 사진", "해운대 인스타 사진", "제주 인생샷 인스타 사진",
    "성수 인스타 사진", "서울숲 인스타 사진", "에펠탑 인스타 사진", "경주 인스타 사진", "파리 인스타 사진"
]# 검색할 키워드 목록을 작성

baseUrl = "https://search.naver.com/search.naver?where=image&sm=tab_jum&query="
FORDER_PATH = "./naverImg"  # 사진을 저장할 경로

#다운받을 폴더 생성
if not os.path.exists(FORDER_PATH):
    os.mkdir(FORDER_PATH)

#크롤링 진행
api.doCrawl(driver,keywords,baseUrl,FORDER_PATH)