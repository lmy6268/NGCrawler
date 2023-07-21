# <b>ng-crawler</b>
```zsh
NG-Crawler is the crawler for crawling images by keywords from Naver, Google at the same time.
```

## <b>Environment</b>
```zsh
Macbook Air M1 2020, MacOS Ventura 13.4, Python 3.9.6, Visual Studio Code 1.79.1 (Universal)
```

## <b>How to use</b>
1. <b>Go to the source path using Terminal.</b> <br/>
    ``` zsh
    cd  <source path>
    ```
2. <b>Install python libraries by requirements.txt.</b> <br/>
    ```zsh
    pip install -r ./requirements.txt
    ``` 
3. In <b>keyword.txt</b>, you can type your keywords to find in naver,google to get wanted images.<br/>
    
    <i>Here is the example. </i>

    ```
    // Add keyword what you want to search in each line. <- Do not delete this Line!!
    put your keywords.
    ...
    ```
4. <b>run main.py to get images.</b>
    
    > <b>\< parameters \></b> 
    <br>-g, --Google : Not Execute Search On Google
    <br>-n, --Naver : Not Execute Search On Google 
    <br>-f, --Full_Resolution : Download Full Resolution Image
    <br>-l {counts}, --Limit {counts} : Set Image Download Limit Counts.
    <br>-S, --Show : Not Use Headless Mode.

    ```zsh
    python3 ./main.py {parmeters}
    ```
    or
     ```zsh
    python ./main.py {parmeters}
    ```

## <b>How do I find the downloaded images?</b>
---
You can find images in "./crawledData". <br/>
The crawled result is recorded by Json each Search Engine. 
