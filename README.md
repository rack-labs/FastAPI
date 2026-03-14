# FastAPI
fastapi-team-starter

## git ignore 대상
```gitignore
.venv/
__pycache__/
*.pyc

```

## 가상환경 실행
```bash
# 가상환경 설치
python -m venv .venv

# 가상환경 실행
.\.venv\Scripts\activate

# 가상환경 종료
deactivate
```


## fastapi, uvicorn 설치
```bash
# 패키지 설치
pip install fastapi
pip install uvicorn

# 확인
pip list

# 현재 프로젝트의 의존성 목록을 파일로 고정 저장
pip freeze > requirements.txt
```

## fastapi 활용 간단한 코드 작성(main.py)
```python
from fastapi import FastAPI
from typing import Union

app = FastAPI()

@app.get("/")
def read_root():
    return{"Hello":"world"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```
## uvicorn을 이용해 실행
```bash
uvicorn main:app --reload
    # main: main.py를 지칭
    # app: main.py에서 선언했던 app 객체
    # --reload: 소스가 수정되었을 때 리로딩해줌.
    # 매번 수동으로 실행하기 힘드니, 별도 파일로 관리(run.bat) 이후 터미널에서 './run.bat' 만 치면 됨.

# 실행
http://127.0.0.1:8000/
http://127.0.0.1:8000/items/1
http://127.0.0.1:8000/items/1?q=hi

# swagger (API를 설명하고 문서화하는 생태계. 표준 이름은 OpenAPI)
http://127.0.0.1:8000/docs
```