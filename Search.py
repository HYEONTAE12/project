import requests
import sys
import io
from urllib.request import urlopen, Request
import os
import ssl
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# .env 환경변수 불러오기
load_dotenv()

# Windows 콘솔에서 한글 깨짐 방지
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')


class NaverSearch:
    def __init__(self):
        self.context = ssl._create_unverified_context()
        self.api_url = ""

        self.client_id = os.getenv("NAVER_CLIENT_ID")
        self.client_secret = os.getenv("NAVER_CLIENT_SECRET")

    # API 요청 함수
    def call_url(self, keyword, start=1, display=10):
        url = f"{self.api_url}?query={keyword}&start={start}&display={display}"
        headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret
        }
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        
        if res.status_code != 200:
            raise Exception(f"API 요청 실패: {res.status_code}")
        else:
            r = res.json()
            print(res)
            return r
    # 최대 1100개까지 크롤링 
    def crowl_count(self, keyword, data_count):
        if data_count > 1100:
            raise ValueError("데이터 추출 최대값은 1100이 최대입니다.")
        elif data_count < 0:
            raise ValueError("데이터 추출 최소값은 0입니다.")
        elif data_count == 0:
            raise ValueError("데이터 추출 최소값은 1입니다.")
        elif 0 < data_count < 100:
            i = 1
            display = data_count
        elif 100 <= data_count <=1100:   
            i = data_count // 100
            rest = data_count % 100
            display = 100
        else:
            print("잘못된 값을 입력하셨습니다.")
        result = []
        for j in range(i):
            count = 100 * j + 1
            if data_count == i * 100 and j == i - 1:
                count = 1000
            elif data_count < 100:
                count = 1
            elif j == i - 1 and rest != 0:
                display = rest
            k = self.call_url(keyword, count, display)
            print(f"{j + 1}번째 반복 {count}부터 {display}개의 데이터를 불러왔습니다.")
            
            print("▶ total:", k.get("total", 0))
            
            result += k["items"]
        return result
        
    # 이미지 다운로드
    def image_get(self, path, r):
        success, fail = 0, 0
        if not os.path.exists(path):
            os.mkdir(path)
        
        for i, img in enumerate(r, 1):
            try:
                image_url = img.get("link")
                if not image_url or not image_url.lower().endswith(('jpg', "jpeg", "png")):
                    continue
                res = Request(image_url, headers={"User-Agent":"Mozilla/5.0"})
                with open(f"{path}/{i}.jpg", "wb") as file:
                    file.write(urlopen(res, context=self.context).read())
                    success += 1
            except Exception as e:
                print(f"{e} 오류가 발생했습니다.")
                fail += 1
    
        print(f"\n✅ 저장 완료: {success}개 / ❌ 실패: {fail}개")



    # 카테고리별 API 주소 지정 함수
    def blog(self, keyword, count):
        self.api_url = "https://openapi.naver.com/v1/search/blog.json"
        r = self.crowl_count(keyword, count)
        return r
    def news(self, keyword, count):
        self.api_url = "https://openapi.naver.com/v1/search/news.json"
        r = self.crowl_count(keyword, count)
        return r
    def webkr(self, keyword, count):
        self.api_url = "https://openapi.naver.com/v1/search/webkr.json"
        r = self.crowl_count(keyword, count)
        return r
    def book(self, keyword, count):
        self.api_url = "https://openapi.naver.com/v1/search/book.json"
        r = self.crowl_count(keyword, count)
        return r    
    def image(self, keyword, count):
        self.api_url = "https://openapi.naver.com/v1/search/image.json"
        r = self.crowl_count(keyword, count)
        return r
    

    # 각 카테고리별 출력 함수
    def text_get_blog(self, keyword, count):
        result = self.blog(keyword, count)
        for i, item in enumerate(result, 1):
            bs_obj = BeautifulSoup(item["title"], "html.parser").text
            bs_obj1 = BeautifulSoup(item["description"], "html.parser").text
            self.output(bs_obj, bs_obj1, i)
            
        
    def text_get_image(self, keyword, count, path):
        result = self.image(keyword, count)
        self.image_get(path, result)
        for i, item in enumerate(result, 1):
            bs_obj = BeautifulSoup(item["title"], "html.parser").text
            bs_obj1 = BeautifulSoup(item["description"], "html.parser").text
            self.output(bs_obj, bs_obj1, i)
        
            
    def text_get_book(self, keyword, count):
        result = self.book(keyword, count)
        for i, item in enumerate(result, 1):
            bs_obj = BeautifulSoup(item["title"], "html.parser").text
            bs_obj1 = BeautifulSoup(item["description"], "html.parser").text
            self.output(bs_obj, bs_obj1, i)
        
    def text_get_webkr(self, keyword, count):
        result = self.webkr(keyword, count)
        for i, item in enumerate(result, 1):
            bs_obj = BeautifulSoup(item["title"], "html.parser").text
            bs_obj1 = BeautifulSoup(item["description"], "html.parser").text
            self.output(bs_obj, bs_obj1, i)
        
    def text_get_news(self, keyword, count):
        result = self.news(keyword, count)
        for i, item in enumerate(result, 1):
            bs_obj = BeautifulSoup(item["title"], "html.parser").text
            bs_obj1 = BeautifulSoup(item["description"], "html.parser").text
            self.output(bs_obj, bs_obj1, i)
          
    
    def output(self,bs_obj, bs_obj1, i):
        print()
        print(f"{i}번째\n제목\n- {bs_obj}")
        print(f"내용\n- {bs_obj1}")
        print()
        

# 실행부: 사용자 입력 및 함수 호출
if __name__ == "__main__":
    try:
        nv = NaverSearch()
        user_keyword = input("검색: ")
        page = input("카테고리를 설정해주세요: ")
    
        if page in ["blog", "BLOG","블로그"]:
            n = int(input("가져올 데이터 갯수를 정해주세요: "))
            if n >= 0:
                result = nv.text_get_blog(user_keyword, n)
    
        elif page in ["web", "webkr", "WEb", "WEbKR", "웹","웹문서"]:
            n = int(input("가져올 데이터 갯수를 정해주세요: "))
            if n >= 0:
                result = nv.text_get_webkr(user_keyword, n)
    
        elif page in ["book", "BOOK", "책"]:
            n = int(input("가져올 데이터 갯수를 정해주세요: "))
            if n >= 0:
                result = nv.text_get_book(user_keyword, n)
    
        elif page in ["image", "IMAGE", "이미지", "사진"]:
            n = int(input("가져올 데이터 갯수를 정해주세요: "))
            path = input("이미지를 저장할 폴더명을 입력해주세요: ").strip()
            if n >= 0:
                result = nv.text_get_image(user_keyword, n, path)
    
        elif page in ["news", "NEWS", "뉴스"]:
            n = int(input("가져올 데이터 갯수를 정해주세요: "))
            if n >= 0:    
                result = nv.text_get_news(user_keyword, n)
    
        else:
            print("잘못된 값을 카테고리를 입력하셨습니다.")
    except Exception as e:
        print("잘못된 값을 입력하셨습니다")
    


    
