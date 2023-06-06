import image_download_api as api

if __name__ == "__main__":
    #크롤링 진행 
    tasks = [["Google",300],["Naver",300]]
    api.startToCrawl(tasks)
