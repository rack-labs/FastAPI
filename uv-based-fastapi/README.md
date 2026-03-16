# uv based fastapi

## uv 설치
```bash
# uv 설치
irm https://astral.sh/uv/install.ps1 | iex

# 확인
uv --version

# 프로젝트 생성 (실 사용시엔 example 대신 프로젝트명)
uv init example

# 확인
dir

# 실행 (toml에 명시된 버젼으로 python이 실행된다.)
cd example
uv run main.py
    # Using CPython 3.14.3 interpreter at: C:\Python314\python.exe
    # Creating virtual environment at: .venv
    # Hello from example!                      

# 패키지 설치
    # add 명령어를 쓰면 pyproject.toml>dependencies에 자동 반영됨.
uv add requests # request 테스트용
uv add uvicorn fastapi #uvcorn과 fastapi 설치
```

배포는 curl을 이용해서 uv를 설치하고, 소스를 붙여넣어 uv run main.py 해주면 된다.

