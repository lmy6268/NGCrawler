#셀레니움 관련
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
#오류 처리
from selenium.common.exceptions import StaleElementReferenceException
#enum
from enum import Enum
#딜레이
import time
#이미지 변환
import base64,io
from image_duplication_check import get_image_hash
#이미지 다운로드
import json
import os
from requests import get
from multiprocessing import Pool


class EngineType(Enum):
    """
    검색엔진 타입결정
    """
    Google = 0
    Naver = 1

ROOT_PATH = "images"

class NGCrawler:
    """
    네이버, 구글 동시에 검색, 다운로드 가능한 크롤러
    """

    def duplication_check_image(self, src, keyword, engineType: EngineType,imageDetails:dict):
        """ [이미지 중복 체크] \n
            이미지가 중복인 경우 -> return True \n 
            이미지가 중복이 아닌 경우 -> return False
        """
        # 이미지 소스 비교
        if keyword in imageDetails[ROOT_PATH]: #해당 키워드가 데이터에 있는 경우
            return src in imageDetails[ROOT_PATH][keyword]["urls"] 
        
        else:
            return False

    def init_detail_data(self,engineType:EngineType) -> dict:
        """
        기존에 저장되어있던 데이터 불러오기 
        """

        if os.path.exists(f"./crawledData/image{engineType.name}Details.json"):
            with open(f"./crawledData/image{engineType.name}Details.json") as file:
                dictionary= json.load(file)
                file.close()
        else:
            #기본으로 초기화
            dictionary = {
                    ROOT_PATH: {

                    }
            }
        return dictionary

    def save_detail_data(self,engineType:EngineType,imageDetails:dict):
        #json파일로 저장하는 작업
        with open(f"./crawledData/image{engineType.name}Details.json", "w") as f:
            json.dump(imageDetails, f,
                      indent=2, ensure_ascii=False)
            f.close()

    def __init__(self, search_on_google: bool = True, search_on_naver: bool = True, limit=1000,try_cnt:int = 5):
        """ 크롤러 초기화 """
        #Variable
        self.imgCntNaver = 0
        self.imgCntGoogle = 0
        self.driver = None
        self.try_cnt = try_cnt

        #on/off
        self.search_on_google = search_on_google
        self.search_on_naver = search_on_naver
        self.limit = limit

       

    def init_driver(self):
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

    @staticmethod
    def scroll_down(engineType: EngineType, driver: webdriver.Chrome):
        """ 화면 끝까지 스크롤 함 """
        body = driver.find_element(By.TAG_NAME, 'body')

        if engineType == EngineType.Google:  # 구글 이미지 검색
            while True:
                loadingState = int(driver.find_elements(
                    By.XPATH, '//div[contains(@class,"DwpMZe")]')[0].get_attribute("data-status"))
                btnMore = driver.find_elements(
                    By.XPATH, '//div[contains(@class,"YstHxe")]')[0]
                notNeedMoreLoad = True if len(driver.find_elements(
                    By.XPATH, '//div[contains(@class,"WYR1I")]'))>0 else False
                # 더 로딩할 수 있는 버튼이 있는 경우
                if loadingState == 5 and btnMore.get_attribute("style") == "":
                    #버튼을 누른다
                    btnMore.click()
                elif loadingState == 3 or (loadingState == 5 and notNeedMoreLoad):   
                    try:
                        driver.find_element(By.CLASS_NAME,"r0zKGf").click()  #더이상 관련없는 이미지인 경우
                        break
                    except Exception:# 끝까지 도달한 경우
                        break
                else:  # 현재 페이지 까지 로딩한 경우
                    body.send_keys(Keys.END)
        else:  # 네이버 이미지 검색
            while True:
                body.send_keys(Keys.END)
                if driver.find_elements(By.XPATH, '//div[contains(@class,"photo_loading")]')[0].get_attribute('style') == '':
                    time.sleep(1)
                else:
                    break

    #이미지 관련

    def save_image(self, engineType: EngineType, src: str, keyword: str, idx: int, savePath: str,imageDetails:dict):
        """ 이미지 소스에 있는 사진을 저장함"""
        if engineType == EngineType.Google:
            res = get(src).content if not src[:4] == 'data' else base64.b64decode(src[src.find(","):])
        else:
            res = get(src).content
        imgName = f"{engineType.name[0]}_{get_image_hash(10,io.BytesIO(res))}.jpg"  # 파일명 지정
        with open(f"{savePath}/{imgName}", 'wb') as file:
            file.write(res)# 사진을 저장
            file.close()
        imageDetails[ROOT_PATH][keyword]["files"].append(
            imgName)
        return imageDetails

    def get_image_src(self, engineType: EngineType, driver: webdriver.Chrome, imgTag):
        """
        이미지 소스를 가져온다.
        """
        if engineType == EngineType.Google:
            
            while True:
                try:
                    if imgTag.get_attribute("data-src") != None:
                        ActionChains(driver).move_to_element(imgTag).click().perform()
                    else:
                        break
                except StaleElementReferenceException:
                    time.sleep(.5)
            image_src = imgTag.get_attribute("src")
            #4. 수집된 URL을 이용하여 사진 저장
            #4-1. 구글 이미지 다운로드

            self.lastNodeGoogle = imgTag  # 지금까지 저장된 노드까지 기억해둠

        else:  # 4-2. 네이버 이미지 다운로드
            while True:
                image_src = imgTag.get_property('src')
                if image_src[:4] == "data":  # 로딩이 덜됨::
                        ActionChains(driver).move_to_element(imgTag).click().perform()
                else:
                    image_src = imgTag.get_property('src')
                    self.lastNodeNaver = imgTag
                    break
        return image_src
    
  
    def get_image_tags_from_page(self, engineType: EngineType, driver: webdriver.Chrome, keyword: str, query: str, savePath: str, limit: int = 1000):
        """ 이미지를 가져오고 저장함 \n
            [parameters]:
                driver - 웹드라이버 \n
                limit - 가져올 사진의 최대량\n
        """

        #초기화 작업

        searchQuery = f"{query}{keyword}&tbm=isch" if engineType == EngineType.Google else f"{query}{keyword}"

        #2.웹페이지 로딩
        driver.get(searchQuery)
        print(f"LoadPage Start: Search {keyword} from {engineType.name}")
        self.scroll_down(engineType, driver)  # 스크롤을 끝까지 내린다.
        print(f"LoadPage Done : Search {keyword} from {engineType.name}")

        #3. 이미지 URL 수집
        imgTags = driver.find_elements(By.CLASS_NAME, "Q4LuWd") if engineType == EngineType.Google else driver.find_elements(
            By.CLASS_NAME, "_listImage")  # 이미지가 있는 태그로 이동
        imgTags = imgTags[:limit] if len(
            imgTags) > limit else imgTags  # 특정 길이 만큼만 다운로드
        
        return imgTags

    def download_image_from_tags(self,imgTags,engineType:EngineType,driver:webdriver.Chrome,keyword:str,savePath:str,imageDetails:dict) -> dict:
        """
        이미지 태그로부터 실질적인 이미지를 다운로드 받는 프로세스를 진행
        """
        idx = 0
        for imgTag in imgTags:
            imgSrc = self.get_image_src(
                engineType, driver, imgTag)  # 이미지 소스 가져옴

            #이미지 중복 다운로드 우회
            if not self.duplication_check_image(imgSrc, keyword, engineType,imageDetails):
                #데이터 저장
                if not keyword in imageDetails[ROOT_PATH]:
                    imageDetails[ROOT_PATH][keyword] = {"urls":[],"files":[]}
                idx+=1
                imageDetails[ROOT_PATH][keyword]["urls"].append(imgSrc)
                imageDetails = self.save_image(engineType, imgSrc, keyword, idx, savePath,imageDetails)
                print(f"{keyword} 이미지 저장 작업 from {engineType.name} : {idx}")
            else:
                print(
                    f"{keyword} 이미지 저장 작업 from {engineType.name} : {idx} skipped")

        self.imgCntGoogle += idx
        self.imgCntNaver += idx
        return imageDetails
        

    def crawl(self, args):
        self.driver = self.init_driver()
        self.doCrawl(keywords=args[0], engineType=args[1])

    def doCrawl(self, engineType: EngineType, keywords):
        FORDER_PATH = "./crawledData/googleImg" if engineType == EngineType.Google else "./crawledData/naverImg"
        baseUrl = "https://www.google.com/search?q=" if engineType == EngineType.Google else "https://search.naver.com/search.naver?where=image&sm=tab_jum&query="  # 이미지 검색 쿼리 기본 URL

        details = self.init_detail_data(engineType=engineType)

        #다운받을 폴더 생성
        if not os.path.exists(FORDER_PATH):
            os.makedirs(FORDER_PATH,exist_ok=True)
      

        # 각 키워드별로 쿼리 실행
        for keyword in keywords:

            print(f"Start to search {keyword} image from {engineType.name}")
            imgTags = self.get_image_tags_from_page(engineType, self.driver, keyword,
                                baseUrl, FORDER_PATH, self.limit)
            print(f"Done to search {keyword} image from {engineType.name}")
            details =  self.download_image_from_tags(imgTags,engineType,self.driver,keyword,FORDER_PATH,details)
        print(
            f"total download from {engineType.name} : {self.imgCntGoogle if engineType == EngineType.Google else self.imgCntNaver}")
        length = 0
        for i in details[ROOT_PATH]:
            details[ROOT_PATH][i]["fileCnt"] = len(details[ROOT_PATH][i]["files"])
            length += len(details[ROOT_PATH][i]["files"])
        details["totalFileCnt"] = length
        self.save_detail_data(engineType,details)
        self.driver.close()  # 웹 드라이버 종료

    @staticmethod
    def get_keyword_from_text_file() -> list:
        #검색 키워드 가져오기
        if os.path.exists("./keyword.txt"):
            with open("./keyword.txt", 'rt') as f:
                keywords = [line.rstrip() for line in f.readlines()[1:]]
                if len(keywords) == 0:
                    print("keyword.txt에 키워드를 입력하고 진행해주세요")
                    keywords = None
                f.close()
            return keywords
        else:
            with open("./keyword.txt", 'wt') as f:
                f.write("//각 줄에 하나씩 키워드를 입력해주세요.  <- 이 줄은 지우지 마세요.")
                f.close()
            print("keyword.txt에 키워드를 입력하고 진행해주세요")
            return None
        

    def startToCrawl(self):
        """
        keyword.txt에 저장되어있는 키워드들을 검색하는 과정
        """
        start = time.time()
        tasks = []

        keywords = self.get_keyword_from_text_file()
        if keywords != None:
            if self.search_on_google:
                tasks.append([keywords, EngineType.Google])
            if self.search_on_naver:
                tasks.append([keywords, EngineType.Naver])


            with Pool(processes=2) as pool:
                try:
                    pool.map(self.crawl, tasks)
                except KeyboardInterrupt:
                    pool.terminate()
                    pool.join()
                else:
                    pool.terminate()
                    pool.join()


            print('Task ended. Pool join.')
            print(f"elapse time : {time.strftime('%H:%M:%S', time.gmtime(time.time()-start))}")
