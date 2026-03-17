# FastAPI Study Repository

프로젝트가 처음인 팀원을 기준으로, 이 저장소를 어떻게 읽고 실행하면 되는지 차근차근 설명하는 안내서입니다.

이 문서는 `uv` 방식만 다룹니다. 이 저장소 안에는 다른 실험 폴더도 있지만, 지금부터는 `uv-based-fastapi`만 본다고 생각하면 됩니다.

## 1. 이 저장소는 무엇을 배우기 위한 것인가요?

이 저장소는 FastAPI의 가장 기본적인 흐름을 직접 만져 보기 위한 예제입니다.

이 예제를 통해 아래 순서를 익힐 수 있습니다.

1. Python 프로젝트를 만든다.
2. `uv`로 필요한 패키지를 설치한다.
3. FastAPI 서버를 실행한다.
4. URL로 API를 호출해 본다.
5. 라우터를 파일별로 나눠 본다.
6. MySQL과 연결해 데이터를 조회해 본다.

즉, "웹 서버가 어떻게 켜지고", "API 파일이 어떻게 나뉘고", "DB에서 데이터를 어떻게 읽어 오는지"를 한 번에 경험하는 저장소입니다.

## 2. 어디부터 보면 되나요?

가장 먼저 볼 폴더는 아래입니다.

`uv-based-fastapi/example`

이 폴더가 실제로 실행하는 FastAPI 예제 프로젝트입니다.

루트에서 중요한 경로는 아래 정도만 먼저 기억하면 충분합니다.

- `uv-based-fastapi/README.md`
  현재 `uv` 버전 예제의 작업 메모입니다.
- `uv-based-fastapi/example/main.py`
  서버를 실행하는 시작 파일입니다.
- `uv-based-fastapi/example/app.py`
  FastAPI 앱과 라우터를 등록하는 파일입니다.
- `uv-based-fastapi/example/controller/`
  API 주소별로 기능을 나눈 폴더입니다.
- `uv-based-fastapi/example/model/mysql_test.py`
  MySQL 조회 코드가 들어 있는 파일입니다.
- `uv-based-fastapi/example/config/config.py`
  포트와 DB 접속 설정이 들어 있는 파일입니다.
- `uv-based-fastapi/example/main_request.py`
  `requests` 패키지 테스트용 예제 파일입니다.

## 3. 폴더 구조를 먼저 이해해 봅시다

현재 기준 주요 구조는 아래와 같습니다.

```text
FastAPI/
├─ README.md
├─ test_db.bak
├─ uv-based-fastapi/
│  ├─ README.md
│  ├─ prompts/
│  │  └─ update-root-readme-from-project-status.md
│  └─ example/
│     ├─ README.md
│     ├─ app.py
│     ├─ main.py
│     ├─ main_request.py
│     ├─ pyproject.toml
│     ├─ uv.lock
│     ├─ config/
│     │  └─ config.py
│     ├─ controller/
│     │  ├─ admins.py
│     │  ├─ items.py
│     │  └─ users.py
│     └─ model/
│        └─ mysql_test.py
└─ pip-based-fastapi/
```

여기서 초보자가 꼭 알아야 할 핵심은 아래입니다.

- `main.py`는 "서버를 실행하는 파일"입니다.
- `app.py`는 "FastAPI 앱을 만드는 파일"입니다.
- `controller` 폴더는 "URL별 기능을 나누는 곳"입니다.
- `model` 폴더는 "DB 접근 코드를 두는 곳"입니다.
- `config.py`는 "설정값을 모아 두는 곳"입니다.

## 4. 실행 전에 알아둘 것

이 예제는 현재 코드 기준으로 아래 패키지를 사용합니다.

- `fastapi`
- `uvicorn`
- `requests`
- `mysql-connector-python`

`uv-based-fastapi/example/pyproject.toml`에 실제 의존성이 적혀 있습니다.

현재 설정은 아래와 같습니다.

- Python 버전 조건: `>=3.14`
- 서버 호스트: `127.0.0.1`
- 서버 포트: `8080`
- 자동 재시작: `reload=True`

## 5. uv는 무엇인가요?

`uv`는 Python 패키지 설치, 가상환경 관리, 실행을 빠르게 도와주는 도구입니다.

예전에는 아래처럼 따로따로 많이 했습니다.

- 가상환경 만들기
- 가상환경 활성화하기
- `pip install` 하기
- `python main.py` 실행하기

`uv`를 쓰면 이 과정을 더 단순하게 가져갈 수 있습니다.

이 저장소는 그 `uv` 방식으로 정리되어 있습니다.

## 6. 처음 실행하는 순서

### 6-1. `uv` 설치 확인

터미널에서 아래 명령으로 `uv`가 설치되어 있는지 확인합니다.

```bash
uv --version
```

버전이 보이면 다음 단계로 가면 됩니다.

만약 설치가 안 되어 있다면, 팀에서 사용하는 표준 설치 방법으로 먼저 `uv`를 설치해야 합니다.

### 6-2. 예제 프로젝트 폴더로 이동

```bash
cd uv-based-fastapi\example
```

이제부터 대부분의 명령은 이 폴더에서 실행합니다.

### 6-3. 의존성 설치

`pyproject.toml`에 적혀 있는 패키지를 기준으로 환경을 맞춥니다.

```bash
uv sync
```

이 명령은 현재 프로젝트에 필요한 패키지를 설치하고, 잠금 파일인 `uv.lock` 기준으로 환경을 맞추는 데 사용합니다.

## 7. 서버는 어떻게 실행하나요?

`main.py`가 서버 실행 진입점입니다.

```bash
uv run main.py
```

이 명령이 하는 일은 아래와 같습니다.

1. `main.py`를 실행합니다.
2. `main.py` 안에서 `uvicorn.run(...)`을 호출합니다.
3. `app="app:app"` 설정을 보고 `app.py`의 `app` 객체를 찾습니다.
4. FastAPI 서버가 `127.0.0.1:8080`에서 실행됩니다.

실제 코드 흐름은 대략 이렇게 읽으면 됩니다.

### `main.py`

```python
import uvicorn
from config import config

def main():
    uvicorn.run(
        app="app:app",
        host="127.0.0.1",
        port=config.PORT,
        reload=True,
    )
```

여기서 중요한 포인트는 아래입니다.

- `app="app:app"`
  `app.py` 파일 안의 `app` 객체를 사용한다는 뜻입니다.
- `host="127.0.0.1"`
  내 컴퓨터에서만 접속 가능한 로컬 주소입니다.
- `port=config.PORT`
  포트 번호는 설정 파일에서 가져옵니다.
- `reload=True`
  코드를 저장하면 서버가 자동으로 다시 시작됩니다.

## 8. 브라우저에서 무엇을 확인하면 되나요?

서버가 켜지면 아래 주소들을 열어 볼 수 있습니다.

- `http://127.0.0.1:8080/`
- `http://127.0.0.1:8080/items/1`
- `http://127.0.0.1:8080/items/1?q=test`
- `http://127.0.0.1:8080/users/1`
- `http://127.0.0.1:8080/docs`

각 주소의 의미는 아래와 같습니다.

- `/`
  가장 기본적인 루트 주소입니다.
- `/items/1`
  경로 파라미터를 받는 예제입니다.
- `/items/1?q=test`
  경로 파라미터와 쿼리스트링을 함께 받는 예제입니다.
- `/users/1`
  다른 라우터 파일로 분리된 API 예제입니다.
- `/docs`
  FastAPI가 자동으로 만들어 주는 Swagger UI 문서입니다.

초보자라면 특히 `/docs`를 꼭 열어 보세요.

코드를 다 읽지 않아도 어떤 API가 있는지 버튼으로 확인할 수 있어서 이해가 훨씬 쉬워집니다.

## 9. `app.py`는 무슨 역할을 하나요?

`app.py`는 FastAPI 앱을 만들고, 각 라우터를 등록하는 파일입니다.

현재 코드는 아래 구조입니다.

```python
from fastapi import FastAPI
from controller import items, users, admins

app = FastAPI()

app.include_router(items.router)
app.include_router(users.router)
app.include_router(admins.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

이 파일을 읽을 때는 아래 순서로 이해하면 됩니다.

1. `app = FastAPI()`로 앱을 만듭니다.
2. `include_router(...)`로 기능별 라우터를 붙입니다.
3. `/` 주소용 간단한 API도 직접 하나 만듭니다.

## 10. `controller` 폴더는 왜 나누나요?

프로젝트가 커지면 `main.py`나 `app.py` 한 파일에 모든 API를 몰아넣기 어렵습니다.

그래서 주소별로 파일을 나눕니다.

현재는 아래처럼 나뉘어 있습니다.

- `controller/items.py`
- `controller/users.py`
- `controller/admins.py`

### `items.py`

`/items/{item_id}` 주소를 담당합니다.

```python
@router.get("/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

여기서 배우면 좋은 개념은 아래입니다.

- `item_id: int`
  주소에 들어오는 값을 정수로 받겠다는 뜻입니다.
- `q`
  선택적으로 받는 쿼리스트링입니다.

예를 들어 아래처럼 호출할 수 있습니다.

```text
/items/1
/items/1?q=test
```

### `users.py`

`/users/{user_id}` 주소를 담당합니다.

```python
@router.get("/{user_id}")
def read_user(user_id: int):
    return {"user_id": user_id}
```

이 파일은 가장 단순한 라우터 예제라고 보면 됩니다.

## 11. `requests` 테스트 파일은 무엇인가요?

`main_request.py`는 FastAPI 서버를 띄우는 파일이 아닙니다.

이 파일은 Python 코드에서 외부 HTTP 요청을 보내는 아주 간단한 예제입니다.

실행은 아래처럼 합니다.

```bash
uv run main_request.py
```

현재 코드는 Python 공식 문서 쪽 API에 요청을 보내고, JSON 응답을 출력합니다.

```python
import requests

def main():
    resp = requests.get("https://peps.python.org/api/peps.json")
    data = resp.json()
    print(data)
```

즉, 이 파일은 "HTTP 요청을 보내는 코드가 이런 느낌이구나"를 보기 위한 별도 예제입니다.

## 12. MySQL 연동은 어떻게 되어 있나요?

이 저장소에는 DB 연결 예제도 들어 있습니다.

현재는 MySQL 기준입니다.

먼저 설정 파일을 보면 아래와 같습니다.

### `config/config.py`

```python
PORT = 8080

MYSQL_DB_CONFIG = {
    "host": "127.0.0.1",
    "database": "test_db",
    "user": "test_user",
    "password": "0000",
}
```

이 파일은 크게 두 가지를 관리합니다.

- FastAPI 서버 포트
- MySQL 접속 정보

### `model/mysql_test.py`

이 파일은 실제 DB에 접속해 저장 프로시저를 호출합니다.

현재 로직은 아래 흐름입니다.

1. `config.py`에서 DB 접속 정보를 가져옵니다.
2. MySQL에 연결합니다.
3. `SP_L_ADMIN` 저장 프로시저를 호출합니다.
4. 결과를 리스트로 모아서 반환합니다.

즉, 지금 코드는 단순 `SELECT`가 아니라 저장 프로시저 기반 예제입니다.

## 13. DB 연동이 되려면 무엇이 먼저 준비되어야 하나요?

아래 조건이 맞아야 `/admins/...` 쪽이 동작합니다.

1. 로컬 MySQL 서버가 실행 중이어야 합니다.
2. `test_db` 데이터베이스가 있어야 합니다.
3. `test_user / 0000` 계정이 있어야 합니다.
4. `TB_ADMIN` 테이블이 있어야 합니다.
5. `SP_L_ADMIN` 저장 프로시저가 있어야 합니다.

저장소 루트에는 `test_db.bak` 파일도 있습니다.

이 파일은 DB 백업 관련 실습 흔적으로 보며, 필요할 때 참고할 수 있습니다.

## 14. `/admins` API는 현재 어떤 상태인가요?

현재 `controller/admins.py`는 아래처럼 되어 있습니다.

```python
@router.get("/{list}")
def list_admin():
    results = mysql_test.list_admin()
    return results
```

여기서 초보자도 꼭 알아야 할 점이 있습니다.

- URL 경로에는 `/{list}`가 선언되어 있습니다.
- 그런데 함수 `list_admin()`은 `list` 값을 인자로 받지 않습니다.

즉, 현재 코드는 "주소 형식"과 "함수 매개변수"가 깔끔하게 맞아 떨어지는 상태는 아닙니다.

그래서 `/admins/test` 같은 주소는 문서상 예시로는 볼 수 있지만, 실제 프로젝트에서는 이 부분을 나중에 정리하는 것이 좋습니다.

이 README는 현재 코드를 숨기지 않고 그대로 설명하기 위해 이 상태를 그대로 적었습니다.

## 15. 초보자에게 추천하는 읽는 순서

처음 보는 팀원이라면 아래 순서가 가장 이해하기 쉽습니다.

1. `uv-based-fastapi/example/main.py`
   서버를 어떻게 켜는지 먼저 봅니다.
2. `uv-based-fastapi/example/app.py`
   FastAPI 앱과 라우터 연결 구조를 봅니다.
3. `uv-based-fastapi/example/controller/items.py`
   가장 쉬운 API 예제를 봅니다.
4. `uv-based-fastapi/example/controller/users.py`
   라우터를 하나 더 추가한 예제를 봅니다.
5. 브라우저에서 `/docs`
   코드와 실제 API 화면을 연결해서 이해합니다.
6. `uv-based-fastapi/example/config/config.py`
   설정 파일의 역할을 봅니다.
7. `uv-based-fastapi/example/model/mysql_test.py`
   DB 연결은 마지막에 봅니다.

처음부터 DB 코드까지 한 번에 이해하려고 하면 부담이 큽니다.

먼저 "서버 실행 -> 라우터 이해 -> API 호출 확인"까지 익힌 뒤에 DB 쪽으로 넘어가는 것이 좋습니다.

## 16. 가장 자주 쓰는 명령만 다시 정리

프로젝트 폴더 이동:

```bash
cd uv-based-fastapi\example
```

의존성 설치:

```bash
uv sync
```

서버 실행:

```bash
uv run main.py
```

요청 테스트 파일 실행:

```bash
uv run main_request.py
```

## 17. 현재 코드 기준으로 기억할 주의사항

- 이 저장소는 `uv` 기준으로 보는 것이 가장 자연스럽습니다.
- 실제 실행 프로젝트는 `uv-based-fastapi/example`입니다.
- `example/README.md`는 현재 비어 있습니다.
- `pyproject.toml`의 `readme = "README.md"`는 비어 있는 `example/README.md`를 가리키고 있습니다.
- `/admins/{list}` 라우터는 경로 선언과 함수 시그니처가 완전히 맞지 않습니다.
- DB 예제는 MySQL과 저장 프로시저 준비가 끝나야 정상 동작합니다.
- Python 버전 조건이 `>=3.14`로 잡혀 있으므로, 실행 환경 버전을 먼저 확인하는 것이 좋습니다.

## 18. 막히면 어디를 먼저 확인하면 되나요?

서버가 안 켜지면 아래 순서로 보면 됩니다.

1. `uv-based-fastapi/example` 폴더 안에서 명령을 실행했는지 확인
2. `uv sync`를 했는지 확인
3. `uv --version`이 되는지 확인
4. `config/config.py`의 포트가 `8080`인지 확인
5. 실행 명령을 `uv run main.py`로 쳤는지 확인

`/admins`가 안 되면 아래를 확인하면 됩니다.

1. MySQL 서버가 켜져 있는지
2. 접속 정보가 `config.py`와 맞는지
3. `test_db`와 `TB_ADMIN`이 있는지
4. `SP_L_ADMIN` 저장 프로시저가 있는지

## 19. 한 줄 요약

이 저장소는 `uv-based-fastapi/example` 폴더를 중심으로 FastAPI의 기본 실행, 라우터 분리, 그리고 MySQL 연동까지 연습하는 입문용 예제입니다.
