import uvicorn
from config import config

def main():
    uvicorn.run( # 로컬 개발에서는 브라우저에서 바로 접근 가능한 주소로 바인딩한다.
        app = 'app:app', # app.py라는 파일에서 app이라는 모듈을 참고하겠다.
        host = '127.0.0.1',
        port = config.PORT,
        reload = True # 소스파일 수정,저장 시 자동으로 서버 재시작(개발모드용)
    )

if __name__ == "__main__":
    main()
    