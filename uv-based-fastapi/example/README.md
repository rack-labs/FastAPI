# FastAPI Example Solution Guide

이 문서는 이 `example` 프로젝트를 "완성품"이 아니라 "뼈대, 스켈레톤(skeleton)"으로 보고 설명합니다.

즉, 지금 있는 코드를 그대로 외우는 문서가 아니라, 아래처럼 이해하는 문서입니다.

- 서버를 켜는 블록은 어디인가?
- 주소(API)를 추가하는 블록은 어디인가?
- 설정값을 바꾸는 블록은 어디인가?
- DB 연결 블록은 어디인가?
- 내가 새 기능을 만들 때 어디를 고치면 되는가?

처음 보는 사람도 블록 조립하듯이 구조를 따라갈 수 있게 설명하겠습니다.

## 1. 이 프로젝트를 한 문장으로 설명하면

이 프로젝트는 `uv`로 실행하는 아주 작은 FastAPI 서버 스켈레톤입니다.

현재 들어 있는 기능은 크게 4가지입니다.

1. 서버 실행
2. 기본 라우터(`items`, `users`)
3. 루트 주소(`/`)
4. MySQL 조회 예제(`admins`)

## 2. 가장 먼저 이해해야 할 전체 구조

프로젝트 구조는 아래처럼 보면 됩니다.

```text
example/
├─ README.md
├─ app.py
├─ main.py
├─ main_request.py
├─ pyproject.toml
├─ uv.lock
├─ config/
│  └─ config.py
├─ controller/
│  ├─ admins.py
│  ├─ items.py
│  └─ users.py
└─ model/
   └─ mysql_test.py
```

이 구조를 "포트에 부품을 꽂는 방식"으로 비유하면 아래와 같습니다.

```text
[main.py]
  서버 전원 ON
      |
      v
[app.py]
  FastAPI 본체
  + 라우터 연결 포트
      |
      +--> [controller/items.py]
      +--> [controller/users.py]
      +--> [controller/admins.py]
                              |
                              v
                    [model/mysql_test.py]
                              |
                              v
                    [config/config.py]
```

이 그림에서 핵심은 아래입니다.

- `main.py`는 서버를 "실행"합니다.
- `app.py`는 각 기능 파일을 "연결"합니다.
- `controller/*.py`는 URL 기능을 "정의"합니다.
- `model/*.py`는 DB와 통신합니다.
- `config/config.py`는 설정값을 제공합니다.

## 3. 실행 흐름을 아주 쉽게 보면

서버를 켤 때 실제로는 아래 순서로 움직입니다.

1. `uv run main.py`
2. `main.py`가 `uvicorn`으로 서버를 실행
3. `app.py`의 `app` 객체를 읽음
4. `app.py`가 `items`, `users`, `admins` 라우터를 연결
5. 사용자가 URL로 요청
6. 해당 라우터 함수 실행
7. 필요하면 DB 조회 후 결과 반환

즉, 실행 시작점은 `main.py`지만, 실제 기능 연결 중심은 `app.py`입니다.

## 4. 파일별 역할 설명

### `main.py`

이 파일은 "서버 실행 버튼"입니다.

현재 코드 핵심:

```python
uvicorn.run(
    app="app:app",
    host="127.0.0.1",
    port=config.PORT,
    reload=True,
)
```

여기서 의미는 아래와 같습니다.

- `app="app:app"`
  `app.py` 파일 안의 `app` 객체를 사용하겠다는 뜻입니다.
- `host="127.0.0.1"`
  내 컴퓨터에서만 접속합니다.
- `port=config.PORT`
  포트 번호는 설정 파일에서 가져옵니다.
- `reload=True`
  코드 저장 시 서버를 자동 재시작합니다.

실무에서 자주 바꾸는 부분:

- 포트를 바꾸고 싶다 -> `config/config.py`
- 배포 환경 설정을 바꾸고 싶다 -> `main.py` 또는 실행 명령
- 개발 중 자동 재시작을 끄고 싶다 -> `reload=False`

### `app.py`

이 파일은 "앱 본체 + 라우터 연결판"입니다.

현재 코드 핵심:

```python
app = FastAPI()

app.include_router(items.router)
app.include_router(users.router)
app.include_router(admins.router)
```

이 파일에서 하는 일은 두 가지입니다.

1. FastAPI 앱을 만든다.
2. 다른 파일에 만든 API들을 여기 연결한다.

실무에서 자주 바꾸는 부분:

- 새 API 파일을 만들었다 -> 여기서 `include_router(...)` 추가
- 앱 공통 설정을 넣고 싶다 -> 여기서 `FastAPI(...)` 옵션 추가
- 공통 미들웨어나 예외 처리 넣고 싶다 -> 여기서 확장

### `controller/items.py`

이 파일은 `/items` 주소 담당 블록입니다.

현재 핵심:

```python
router = APIRouter(prefix="/items", tags=["items"])

@router.get("/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

이 파일을 보면 아래 개념을 같이 배울 수 있습니다.

- `prefix="/items"`
  이 파일의 기본 주소 시작점
- `@router.get(...)`
  GET 요청 처리
- `item_id: int`
  경로 파라미터
- `q`
  쿼리스트링

예:

- `/items/1`
- `/items/1?q=test`

### `controller/users.py`

이 파일은 `/users` 주소 담당 블록입니다.

가장 간단한 라우터 예제이므로, 처음 연습용으로 좋습니다.

원하는 API를 직접 추가해 보려면 이 파일이 가장 쉬운 출발점입니다.

### `controller/admins.py`

이 파일은 `/admins` 주소 담당 블록입니다.

다른 라우터와 다른 점은, 이 파일은 바로 결과를 만들지 않고 `model/mysql_test.py`를 호출한다는 점입니다.

즉, 이 파일은 "URL 요청"과 "DB 로직" 사이를 연결하는 중간 블록입니다.

현재 핵심:

```python
from model import mysql_test

@router.get("/{list}")
def list_admin():
    results = mysql_test.list_admin()
    return results
```

이 파일은 현재 예제 상태 그대로 유지되어 있어서, 아래 주의가 있습니다.

- 주소는 `/{list}`를 받는 형태인데
- 함수는 실제로 그 값을 사용하지 않습니다

즉, 현재는 "DB 연결 예제"에 더 가깝고, API 설계가 완전히 정리된 상태는 아닙니다.

### `model/mysql_test.py`

이 파일은 "DB 통신 블록"입니다.

현재 하는 일:

1. MySQL에 연결
2. 저장 프로시저 `SP_L_ADMIN` 호출
3. 결과를 가져와 반환

즉, 이 파일은 URL을 처리하지 않습니다.

이 파일의 역할은 오직 "데이터 가져오기"입니다.

실무에서 자주 바꾸는 부분:

- DB 종류 변경
- SQL 변경
- 저장 프로시저 대신 직접 `SELECT`
- 반환 형식 정리
- 예외 처리 강화

### `config/config.py`

이 파일은 "설정 전용 블록"입니다.

현재 설정:

```python
PORT = 8080

MYSQL_DB_CONFIG = {
    "host": "127.0.0.1",
    "database": "test_db",
    "user": "test_user",
    "password": "0000",
}
```

처음 배우는 사람은 이 원칙만 기억하면 됩니다.

- 자주 바뀌는 값은 `config.py`로 모은다
- 하드코딩을 줄인다
- 서버 코드와 설정 코드를 분리한다

## 5. 이 스켈레톤을 어떻게 써야 하나요?

이 프로젝트는 아래 방식으로 사용하면 됩니다.

### 경우 1. "정말 기본적인 API 하나만 만들고 싶다"

가장 쉬운 방법:

1. `controller/users.py`를 복사해서 새 파일 생성
2. 원하는 주소와 함수 이름으로 수정
3. `app.py`에서 `include_router(...)` 추가

예를 들어 `products.py`를 만들고 싶다면:

1. `controller/products.py` 생성
2. `prefix="/products"`로 변경
3. `@router.get(...)` 함수 작성
4. `app.py`에서 연결

즉, 새 기능 추가의 기본 공식은 아래입니다.

```text
controller 새 파일 생성
-> router 작성
-> app.py에 include_router 추가
-> 서버 실행 후 /docs 확인
```

### 경우 2. "포트를 바꾸고 싶다"

`config/config.py`의 `PORT` 값을 바꾸면 됩니다.

예:

```python
PORT = 9000
```

그러면 접속 주소도 `http://127.0.0.1:9000`으로 바뀝니다.

### 경우 3. "DB 연결 정보를 바꾸고 싶다"

`config/config.py`의 `MYSQL_DB_CONFIG`를 수정하면 됩니다.

예:

- DB 호스트 변경
- DB 이름 변경
- 사용자 계정 변경
- 비밀번호 변경

DB 접속 오류가 나면 가장 먼저 여기부터 확인하면 됩니다.

### 경우 4. "DB를 안 쓰고 순수 API만 쓰고 싶다"

그러면 `admins.py`와 `mysql_test.py`는 잠시 무시해도 됩니다.

처음에는 아래 파일만 보면 충분합니다.

- `main.py`
- `app.py`
- `controller/items.py`
- `controller/users.py`

즉, DB 부분은 나중에 붙여도 됩니다.

### 경우 5. "DB에서 다른 데이터를 조회하고 싶다"

보통 아래 순서로 수정합니다.

1. `model/mysql_test.py`에 새 함수 추가
2. SQL 또는 저장 프로시저 호출 변경
3. `controller/*.py`에서 그 함수를 호출
4. 필요하면 새 라우터 파일 생성

즉, 원칙은 아래입니다.

- `controller`는 요청과 응답 담당
- `model`은 DB 로직 담당

둘을 한 파일에 다 몰아넣지 않는 것이 구조를 이해하기 쉽습니다.

## 6. "무엇을 고치면 무엇이 바뀌는가" 빠른 표

| 내가 바꾸고 싶은 것 | 고칠 파일 |
|---|---|
| 서버 포트 | `config/config.py` |
| 앱 연결 구조 | `app.py` |
| 서버 실행 방식 | `main.py` |
| 새 API 주소 추가 | `controller/*.py` |
| DB 조회 로직 | `model/mysql_test.py` |
| DB 접속 정보 | `config/config.py` |
| 외부 HTTP 요청 테스트 | `main_request.py` |

## 7. 새 API를 추가하는 가장 쉬운 실전 예시

예를 들어 "공지사항 목록 API"를 추가하고 싶다고 가정하겠습니다.

### 1단계. 라우터 파일 생성

`controller/notices.py`

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/notices",
    tags=["notices"],
    responses={404: {"description": "Not found"}}
)

@router.get("/list")
def list_notices():
    return [
        {"id": 1, "title": "첫 번째 공지"},
        {"id": 2, "title": "두 번째 공지"},
    ]
```

### 2단계. `app.py`에 연결

```python
from controller import items, users, admins, notices

app.include_router(notices.router)
```

### 3단계. 서버 실행

```bash
uv run main.py
```

### 4단계. 브라우저 확인

```text
http://127.0.0.1:8080/notices/list
http://127.0.0.1:8080/docs
```

이 흐름이 이 프로젝트를 사용하는 가장 기본 패턴입니다.

## 8. 실행 방법

프로젝트 폴더로 이동:

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

별도 요청 테스트 실행:

```bash
uv run main_request.py
```

## 9. 브라우저에서 확인할 기본 주소

- `http://127.0.0.1:8080/`
- `http://127.0.0.1:8080/items/1`
- `http://127.0.0.1:8080/items/1?q=test`
- `http://127.0.0.1:8080/users/1`
- `http://127.0.0.1:8080/docs`

`admins`는 MySQL 준비가 되어 있어야 의미 있게 확인할 수 있습니다.

## 10. 처음 배우는 사람에게 추천하는 실습 순서

1. `uv run main.py`로 서버를 켠다
2. `/docs`를 열어 어떤 API가 있는지 본다
3. `controller/users.py`의 함수 이름이나 반환값을 바꿔 본다
4. 저장 후 자동 반영되는지 확인한다
5. `controller/notices.py` 같은 새 파일을 직접 만들어 본다
6. 마지막에 DB 연동 파일을 읽는다

이 순서가 좋은 이유는, 처음부터 DB까지 같이 보면 어려워지기 때문입니다.

먼저 "라우터를 추가하는 감각"을 익힌 뒤 DB로 넘어가는 것이 훨씬 쉽습니다.

## 11. 현재 스켈레톤의 한계와 주의점

이 문서는 현재 코드 기준으로 설명합니다. 그래서 아래 점도 같이 알고 있어야 합니다.

- `admins.py`는 경로 파라미터 선언과 함수 시그니처가 깔끔하게 맞지 않습니다.
- `mysql_test.py`는 MySQL 서버와 저장 프로시저 `SP_L_ADMIN`이 준비되어 있어야 작동합니다.
- `main_request.py`는 FastAPI 서버 기능이 아니라 `requests` 사용 예제입니다.
- 이 프로젝트는 학습용 스켈레톤이라서, 인증/권한/검증/에러 처리 같은 실무 요소는 거의 들어 있지 않습니다.

## 12. 이 프로젝트를 볼 때 꼭 기억할 규칙

처음에는 이 4줄만 기억하면 충분합니다.

1. 서버 시작은 `main.py`
2. 앱 연결은 `app.py`
3. API 추가는 `controller`
4. DB 작업은 `model`

이 규칙만 머리에 들어오면, 이후에 파일이 늘어나도 구조를 잃지 않고 따라갈 수 있습니다.
