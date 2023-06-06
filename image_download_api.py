#셀레니움 관련
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#오류 처리
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, StaleElementReferenceException
#enum
from enum import Enum
#딜레이
import time
#이미지 변환
import base64
#이미지 다운로드
import urllib

import os
from multiprocessing import Pool

LAST_NODE_NAVER = None  # 이전 노드
LAST_NODE_GOOGLE = None  # 이전 노드
NAVER_IMG_CNT = 0 
GOOGLE_IMG_CNT = 0 


class EngineType(Enum):
    """
    검색엔진 타입결정
    """
    Google = 1
    Naver = 2




def initDriver():
    """ 셀레니움 드라이버 초기화 """
    userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('no-sandbox')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('window-size=1920x1080')
    options.add_argument(f"user-agent={userAgent}")
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()  # 만약 드라이버가 없다면 자동으로 설치해줌
    ), options=options)
    return driver


def scrollDown(engineType:EngineType,driver:webdriver.Chrome):
    """ 화면 끝까지 스크롤 함 """
    body = driver.find_element(By.TAG_NAME, 'body')

    if engineType == EngineType.Google:  # 구글 이미지 검색
        while True:
            loadingState = int(driver.find_elements(
                By.XPATH, '//div[contains(@class,"DwpMZe")]')[0].get_attribute("data-status"))
            btnMore = driver.find_elements(
                By.XPATH, '//div[contains(@class,"YstHxe")]')[0]
            if loadingState == 3:   # 끝까지 도달한 경우
                break
            # 더 로딩할 수 있는 버튼이 있는 경우
            elif loadingState == 5 and btnMore.get_attribute("style") == "":
                #버튼을 누른다
                btnMore.click()
            else:  # 현재 페이지 까지 로딩한 경우
                body.send_keys(Keys.END)
    else:
        while True:
            body.send_keys(Keys.END)
            if driver.find_elements(By.XPATH, '//div[contains(@class,"photo_loading")]')[0].get_attribute('style') == '':
                time.sleep(1)
            else:
                break
            
def saveImage(engineType:EngineType,src:str,keyword:str,idx:int,savePath:str):
    """ 이미지 소스에 있는 사진을 저장함"""
    if engineType == EngineType.Google:
        imgName = f"google_{keyword}_{idx}.jpg"  # 파일명 지정
        if src[:4] == 'data':  # Base64 형식
            with open(f"{savePath}/{imgName}", 'wb') as file:
                encoded_data = src[src.find(","):]
                file.write(base64.b64decode(encoded_data))
                file.close()
        else:  # URL 형식
            urllib.request.urlretrieve(src, f"{savePath}/{imgName}")  # 사진을 저장
    else:
        imgName = f"naver_{keyword}_{idx}.jpg"  # 파일명 지정
        urllib.request.urlretrieve(src, f"{savePath}/{imgName}")  # 사진을 저장

def getImgs(engineType:EngineType,driver:webdriver.Chrome,imgTag,keyword:str,idx:int,savePath:str):
    """
    이미지 소스를 가져오고, 
    이미지를 다운받는 로직을 수행한다. 
    """
    global LAST_NODE_GOOGLE,LAST_NODE_NAVER
    if engineType == EngineType.Google:
        body = driver.find_element(By.TAG_NAME, 'body')
        while True:
            try:
                imgTag.click()
                try:
                    if imgTag.get_attribute("data-src") != None:
                        time.sleep(.5)
                    else:
                        break
                except StaleElementReferenceException:
                    time.sleep(1)
            except StaleElementReferenceException:
                time.sleep(1)
            except ElementClickInterceptedException:
                body.send_keys(Keys.DOWN)
            except ElementNotInteractableException:
                body.send_keys(Keys.DOWN)
        image_src = imgTag.get_attribute("src")
        #4. 수집된 URL을 이용하여 사진 저장
         #4-1. 구글 이미지 다운로드
        saveImage(engineType,image_src, keyword, idx, savePath)
        LAST_NODE_GOOGLE = imgTag #지금까지 저장된 노드까지 기억해둠
    
    else: #4-2. 네이버 이미지 다운로드
        image_src =imgTag.get_property('src')
        saveImage(engineType,image_src,keyword,idx,savePath)
        LAST_NODE_NAVER = imgTag




def crawlImg(engineType:EngineType, driver: webdriver.Chrome, keyword: str, query: str, savePath: str, limit: int = 1000): 
    """ 이미지를 가져오고 저장함 \n
        [parameters]:
            driver - 웹드라이버 \n
            limit - 가져올 사진의 최대량\n
    """
    #변수
    global LAST_NODE_GOOGLE,LAST_NODE_NAVER, GOOGLE_IMG_CNT,NAVER_IMG_CNT #전역 변수 사용 -> 이전 노드 기억
    
    idx = 0 #이미지 인덱스
    engineString = "Google" if engineType == EngineType.Google else "Naver"
    searchQuery = f"{query}{keyword}&tbm=isch" if engineType == EngineType.Google else f"{query}{keyword}"

    #2.웹페이지 로딩 
    driver.get(searchQuery)
    print(f"LoadPage Start: Search {keyword} from {engineString}")
    scrollDown(engineType,driver)  # 스크롤을 끝까지 내린다.
    print(f"LoadPage Done : Search {keyword} from {engineString}")
    
    #3. 이미지 URL 수집 
    imgTags = driver.find_elements(By.CLASS_NAME, "Q4LuWd") if engineType == EngineType.Google else driver.find_elements(By.CLASS_NAME, "_listImage")  # 이미지가 있는 태그로 이동
    imgTags = imgTags[:limit] if len(imgTags) > limit else imgTags #특정 길이 만큼만 다운로드
    for imgTag in imgTags:
        idx+=1
        getImgs(engineType,driver,imgTag,keyword,idx,savePath)
        print(f"{keyword} 이미지 저장 작업 from {engineString} : {idx}")
    GOOGLE_IMG_CNT += idx
    NAVER_IMG_CNT += idx


def startToCrawl(tasks:list):
    start = time.time()
    pool = Pool(len(tasks) if len(tasks)<=4 else 4)
    try:
        pool.map(doCrawl,tasks)
    except KeyboardInterrupt:
        pool.terminate()
        pool.join()
    else:
        pool.terminate()
        pool.join()
    print('Task ended. Pool join.')
    print(f"elapse time : {time.time()-start}")


def doCrawl(args):
    engineName = args[0]; limit = args[1]
    engineType = EngineType.Google if engineName == "Google" else EngineType.Naver
    FORDER_PATH = "./googleImg" if engineType==EngineType.Google else "./naverImg"
    baseUrl = "https://www.google.com/search?q="  if engineType == EngineType.Google else "https://search.naver.com/search.naver?where=image&sm=tab_jum&query=" #이미지 검색 쿼리 기본 URL
    #검색 키워드 가져오기
    with open("./keyword.txt",'rt') as f:
        keywords = [line.rstrip() for line in f.readlines()[1:]]
        f.close()

    #다운받을 폴더 생성
    if not os.path.exists(FORDER_PATH):
        os.mkdir(FORDER_PATH)
    
    driver = initDriver()

    # 각 키워드별로 쿼리 실행
    for keyword in keywords:
        print(f"Start to search {keyword} image from {engineName}")
        crawlImg(engineType,driver, keyword, baseUrl,FORDER_PATH, limit) 
        print(f"Done to search {keyword} image from {engineName}")

    print(f"total downlaod from {engineName} : {GOOGLE_IMG_CNT if engineType == EngineType.Google else NAVER_IMG_CNT}")
    
    driver.close()
    

