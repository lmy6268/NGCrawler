
"""
네이버 크롤러 v1.0
"""
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import urllib
from tqdm import tqdm #진행바 표시 
import os
import time  # 딜레이를 주기 위해서

# 이미지 비교를 위해 -> imageHash를 고려가능


def initDriver(): 
    """ 셀레니움 드라이버 초기화 """
    userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('no-sandbox')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('window-size=1920x1080')
    options.add_argument(f"user-agent={userAgent}")
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install() #만약 드라이버가 없다면 자동으로 설치해줌
        ), options=options)
    return driver

def scrollDown(driver, wait=.5):
    """ 화면 끝까지 스크롤 함 """
    body = driver.find_element(By.TAG_NAME, 'body')
    while True:
        body.send_keys(Keys.END)
        if driver.find_elements(By.XPATH, '//div[contains(@class,"photo_loading")]')[0].get_attribute('style') == '':
            time.sleep(wait)
        else:
            break

def get_files_count(folder_path):
    """ 특정 폴더가 가지고 있는 파일의 갯수"""
    dirListing = os.listdir(folder_path)
    return len(dirListing)


def saveImage(imgUrl:str, keyword:str, idx:int,savePath:str):
    """ URL에 있는 사진을 저장함"""
    imgName = f"{keyword}_{idx+1}.jpg"  # 파일명 지정
    urllib.request.urlretrieve(imgUrl, f"{savePath}/{imgName}")  # 사진을 저장


def loadImgList(driver:webdriver, keyword:str, query:str):
    """ 검색결과에서 이미지 목록만 가져옴 """
    driver.get(f"{query}{keyword}")
    time.sleep(1)
    scrollDown(driver)  # 스크롤을 끝까지 내린다.
    imgs = driver.find_elements(By.CLASS_NAME, "_listImage")  # 이미지가 있는 태그로 이동
    return imgs

def doCrawl(driver:webdriver,keywords:str,baseUrl:str,forderPath:str):
    """ 실제로 크롤링을 수행하는 부분 \n 
    -> 입력된 폴더경로에 사진들이 저장된다. 
    \t('keyword_순번.jpg' 형식으로 저장됨.)
    """
    for keyword in tqdm(keywords, desc="네이버 사진 수집 완료", position=0):
        idx = 0
        imgs = loadImgList(driver, keyword, query=baseUrl)
        for img in tqdm(imgs, desc=f"{keyword} 데이터 수집중", position=1):
            #     # imgUrl = img.get_property('src').replace('&type=a340','') #원본화질로 받기 위함
            imgUrl = img.get_property('src') #가로길이가 340픽셀 고정으로 저장됨.
            saveImage(imgUrl, keyword, idx,forderPath)
            idx += 1