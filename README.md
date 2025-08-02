## project
# Naver OpenAPI Search Tool 🕵️‍♂️

Naver의 OpenAPI를 활용해 블로그, 뉴스, 웹문서, 책, 이미지 데이터를 검색하고 저장할 수 있는 Python 기반의 통합 검색 도구입니다.

## 📦 프로젝트 구성

your_project_folder/
├── .env # 민감 정보 (API 키)
├── .env.example # 예시 환경 변수 파일
├── .gitignore # Git 추적 제외 파일 목록
├── Search.py # 메인 실행 파일 (클래스 포함)
├── stock_output.py # 예시 또는 추가 기능 코드
└── README.md # 프로젝트 설명 파일

yaml
복사
편집

---

## ⚙️ 사용 방법

1. `.env` 파일 생성 후 다음과 같이 API 키를 입력하세요:

```env
NAVER_CLIENT_ID=your_client_id
NAVER_CLIENT_SECRET=your_client_secret
라이브러리 설치:

bash
복사
편집
pip install -r requirements.txt
실행:

bash
복사
편집
python Search.py
실행 후 키워드와 카테고리(blog, news, book, image, webkr)를 입력하면 해당 데이터를 가져옵니다.

✅ 기능 설명
블로그/뉴스/웹문서/책/이미지 검색 가능

BeautifulSoup을 이용해 HTML 태그 제거

이미지 자동 저장 기능

최대 1100개까지 데이터 크롤링 지원

💡 예시
makefile
복사
편집
검색: 인공지능
카테고리를 설정해주세요: blog
가져올 데이터 갯수를 정해주세요: 50
📚 기술 스택
Python

requests

BeautifulSoup

dotenv

Naver OpenAPI

📌 주의사항
.env 파일은 GitHub에 올리지 마세요 (보안을 위해 .gitignore 처리됨)

Naver API는 하루 호출 제한이 있습니다.

👨‍💻 개발자
현태 안 – GitHub
