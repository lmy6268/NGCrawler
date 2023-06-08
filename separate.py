import json
import shutil,os
import datetime
def do_seperate():
    now = datetime.datetime.now()
    with open("./crawledData/imageGoogleDetails.json") as file:
            d_google= json.load(file)
            file.close()
    with open("./crawledData/imageNaverDetails.json") as file:
            d_naver= json.load(file)
            file.close()      
    e_n = 0
    e_g =0
    F_G =f"./crawledData/google_eiffel_{now.strftime('%Y%m%d')}/"
    F_N = f"./crawledData/naver_eiffel_{now.strftime('%Y%m%d')}/"
    os.makedirs(F_G,exist_ok=True)
    os.makedirs(F_N,exist_ok=True)

    for data in d_google["data"]:
        if ("Eiffel Tower" in data["keyword"]) or ("에펠탑" in data["keyword"]):
            print(data)
            e_g+=1
            src  = data["name"]
            #파일 이동
            try:
                shutil.move("./crawledData/eiffelImg/"+src,F_G+src)
            except FileNotFoundError:
                pass

    for data in d_naver["data"]:
        if ("Eiffel Tower" in data["keyword"]) or ("에펠탑"  in data["keyword"]):
            src  = data["name"]
            e_n+=1
            try:
                shutil.move("./crawledData/eiffelImg/"+src,F_N+src)
            except FileNotFoundError:
                pass
    print(f"naver: {e_n} / google: {e_g}")
    d_google["eiffel_cnt"] = e_g
    d_naver["eiffel_cnt"] = e_n
    with open("./crawledData/imageNaverDetails.json","w") as file:
            json.dump(d_naver,file,indent=2, ensure_ascii=False)
            file.close()      
    with open("./crawledData/imageGoogleDetails.json","w") as file:
            json.dump(d_google,file,
                        indent=2, ensure_ascii=False)
            file.close()      
if __name__ == "__main__":
   do_seperate()