import uvicorn

def main():
    uvicorn.run( # uvcorn 띄우기
        app = 'app:app', # app.py라는 파일에서 app이라는 모듈을 참고하겠다.
        host = '0.0.0.0',
        port = 8080,
        reload = True # 소스파일 수정,저장 시 자동으로 서버 재시작(개발모드용)
    ) 

if __name__ == "__main__":
    main()
