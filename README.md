# <b>ng-crawler</b>
```zsh
NG-Crawler is a crawler for crawling images using keywords from Naver, Google at the same time.
```

## <b>Environment</b>
---
```zsh
Macbook Air M1, MacOS Ventura 13.4, Python 3.9.6, Visual Studio Code 1.79.1 (Universal)
```

## <b>How to use</b>
---
1. <b>Go to the source path using Terminal.</b> <br/>
    ``` zsh
    cd  <source path>
    ```
2. <b>Install python libraries by requirements.txt.</b> <br/>
    ```zsh
    pip install -r ./requirements.txt
    ``` 
3. Edit main.py and keyword.txt using editor tools. (VS Code etc...)<br/>
    <b>( If you can't find keyword.txt, create the file by running the 'main.py' once.)</b>
    <br/>
    ``` python
    # 'main.py'

    from image_download_api import NGCrawler
    import separate

    if __name__ == "__main__":
        crawler = NGCrawler()   #edit here!
        crawler.startToCrawl()
        separate.do_seperate()

    ```

    In NGCrawler, it has parameters. You can pass value to each parameter using this crawler. 
    ```python
    # 'image_download_api.py'
    class NGCrawler:
        def __init__(
            #You can download images using google. 
            search_on_google: bool = True, 
            #You can download images using naver. 
            search_on_naver: bool = True, 
            #If you make True value both search_on_google and search_on_google_full, 
            #you can download image with full resolution.
            search_on_google_full = False, 
            #If you make True value both search_on_naver and search_on_naver_full, 
            #you can download image with full resolution.
            search_on_naver_full = False,
            #Limit the image amount 
            #(BUT you need to know that query image result of Naver has limitation 
            # of image amount about 450-500, so limit parameter has the limit 500.)
            limit=500 
        ) 
    ```

    And in keyword.txt, you can type your keywords to find in naver,google to get wanted images.<br/>
    Below text is in 'keyword.txt'. Here is the example. 

    ```
    //각 줄에 하나씩 키워드를 입력해주세요.  <- 이 줄은 지우지 마세요.
    감성사진
    여행사진 
    ... put your keywords.
    ```
4. <b>run main.py to get image.</b>

    ```zsh
    python3 ./main.py
    ```
    or
     ```zsh
    python ./main.py
    ```

## <b>Downloaded Image Path</b>
---
You can find images in "./crawledData". <br/>
And Naver crawled result is recored in Json and Google's too. 
