# uv-based-fastapi

`uv` 기반 FastAPI 예제를 현재 코드 상태 그대로 다시 따라갈 수 있게 정리한 루트 작업 메모다.

## 비교 결과 요약

- 문서 누락: `mysql-connector-python` 의존성, `admins` 라우터, `model/mysql_test.py`, `config.py`의 MySQL 접속 설정이 README에 충분히 반영되어 있지 않았다.
- 문서 오기: 현재 라우트 목록이 `/admins/{list}`를 빠뜨리고 있었고, 폴더 구조도 `admins.py`, `model/mysql_test.py` 추가 전 상태로 남아 있었다.
- 현재 상태상 주의: DB 연동은 로컬 MySQL과 `test_db.TB_ADMIN` 테이블, 그리고 저장 프로시저 `SP_L_ADMIN`이 준비되어야만 동작하고, `example/README.md`는 비어 있다. 또한 `admins.py`의 경로 파라미터 선언과 함수 시그니처가 맞지 않아 실제 동작 시 검증이 필요하다.

## 현재 기준

- 기준 문서는 이 파일이다.
- 실제 예제 프로젝트는 `example` 폴더에 있다.
- 실행 진입점은 `example/main.py`다.
- FastAPI 앱 정의는 `example/app.py`다.
- 라우터 파일은 `example/controller/items.py`, `example/controller/users.py`, `example/controller/admins.py`다.
- DB 조회 로직은 `example/model/mysql_test.py`에 있다.
- 실행 설정은 `example/config/config.py`에서 관리한다.
- 요청 테스트 스크립트는 `example/main_request.py`다.
- 현재 의존성은 `fastapi`, `uvicorn`, `requests`, `mysql-connector-python`이다.

## 작업 순서

### 1. uv 설치

```bash
irm https://astral.sh/uv/install.ps1 | iex
uv --version
```

### 2. 프로젝트 생성

```bash
uv init example
cd example
```

생성 직후 기준 파일:

- `pyproject.toml`
- `main.py`
- `README.md`
- `.python-version`

### 3. 패키지 추가

`uv add`를 사용하면 `pyproject.toml`과 `uv.lock`이 같이 갱신된다.

```bash
uv add requests
uv add uvicorn fastapi
uv add mysql-connector-python
```

현재 `example/pyproject.toml`:

```toml
[project]
name = "example"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.14"
dependencies = [
    "fastapi>=0.135.1",
    "mysql-connector-python>=9.6.0",
    "requests>=2.32.5",
    "uvicorn>=0.42.0",
]
```

### 4. FastAPI 앱 구성

현재 구조는 `main.py`가 실행만 담당하고, 실제 앱은 `app.py`에 있으며 라우터와 DB 접근 코드는 분리되어 있다.

`example/config/config.py`

```python
PORT = 8080

MYSQL_DB_CONFIG = {
    "host": "127.0.0.1",
    "database": "test_db",
    "user": "test_user",
    "password": "0000",
}
```

`example/main.py`

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

if __name__ == "__main__":
    main()
```

`example/app.py`

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

`example/controller/items.py`

```python
from typing import Union
from fastapi import APIRouter

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}}
)

@router.get("/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

`example/controller/users.py`

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

@router.get("/{user_id}")
def read_user(user_id: int):
    return {"user_id": user_id}
```

`example/controller/admins.py`

```python
from fastapi import APIRouter
from model import mysql_test

router = APIRouter(
    prefix="/admins",
    tags=["admins"],
    responses={404: {"description": "Not found"}}
)

@router.get("/{list}")
def list_admin():
    results = mysql_test.list_admin()
    return results
```

`example/model/mysql_test.py`

```python
import mysql.connector
from mysql.connector import Error
from config import config

def list_admin():
    results = []
    with mysql.connector.connect(**config.MYSQL_DB_CONFIG) as conn:
        cur = conn.cursor()
        try:
            cur.callproc("SP_L_ADMIN")
            for result in cur.stored_results():
                results.append(result.fetchall())
        except Error as err:
            print(f"쿼리 에러: {err}")
            results = False
    return results
```

### 5. 서버 실행

```bash
cd example
uv run main.py
```

현재 실행 조건:

- 호스트: `127.0.0.1`
- 포트: `8080`
- `reload=True`

현재 코드 기준 확인 주소:

- `http://127.0.0.1:8080/`
- `http://127.0.0.1:8080/items/1`
- `http://127.0.0.1:8080/items/1?q=test`
- `http://127.0.0.1:8080/users/1`
- `http://127.0.0.1:8080/admins/test`
- `http://127.0.0.1:8080/docs`

`/admins/test`는 라우터 경로 정의상 예시로 적은 주소다. 현재 함수는 경로 파라미터를 실제로 사용하지 않으므로, 이 엔드포인트는 코드 수정 없이 그대로 신뢰하기보다 실행 검증이 필요하다.

### 6. 요청 테스트 스크립트 실행

외부 HTTP 요청 테스트용 `requests` 예제:

`example/main_request.py`

```python
import requests

def main():
    resp = requests.get("https://peps.python.org/api/peps.json")
    data = resp.json()
    print(data)

if __name__ == "__main__":
    main()
```

실행:

```bash
cd example
uv run main_request.py
```

### 7. MySQL 준비

DB 연동 예제를 재현하려면 로컬 MySQL과 저장 프로시저가 먼저 준비되어 있어야 한다.

Windows용 MySQL Community Server:
https://dev.mysql.com/downloads/mysql/

- LTS 버전 선택
- `Windows (x86, 64-bit), MSI Installer` 다운로드

```sql
-- 시작
mysql -u root -p

-- 비밀번호 입력
0000

-- 존재하는 데이터베이스 목록 확인
show databases;

-- 사용자 추가
create user 'test_user'@'%' identified by '0000';

-- 확인
use mysql;
select user, host from user;

-- 데이터베이스 생성
create database test_db default character set utf8 collate utf8_general_ci;

-- 권한 설정
grant all privileges on test_db.* to test_user@'%';

-- 종료
quit

-- 사용자로, db를 지정하여 로그인
mysql -u test_user -p test_db

-- 비밀번호 입력
0000

-- 테이블 생성
CREATE TABLE TB_ADMIN
(
    ADMIN_NO INT AUTO_INCREMENT NOT NULL,
    LOGIN_ID VARCHAR(20) NOT NULL UNIQUE,
    PASSWD VARCHAR(20) NOT NULL,
    NICK VARCHAR(20) NOT NULL,
    EMAIL VARCHAR(40),
    PRIMARY KEY (ADMIN_NO)
);

-- 데이터 입력
INSERT INTO TB_ADMIN(LOGIN_ID, PASSWD, NICK, EMAIL)
VALUES('hongildong', 'ajtwoddl', '홍길동', 'hgd@gamil.com');

INSERT INTO TB_ADMIN(LOGIN_ID, PASSWD, NICK, EMAIL)
VALUES('jangnara', 'dlQmsdl', '장나라', 'jnr@gamil.com');

-- 정보 수정
UPDATE TB_ADMIN SET NICK = '홍길똥' WHERE LOGIN_ID = 'hongildong';
UPDATE TB_ADMIN SET NICK = '짱나라' WHERE LOGIN_ID = 'jangnara';

-- 정보 삭제
DELETE FROM TB_ADMIN WHERE LOGIN_ID = 'hongildong';

-- 빠져나오기
exit
```

### 8. DB 백업

```sql
-- mysqldump 확인
mysqldump --version

-- 백업 (PowerShell 말고 cmd 창 기준)
mysqldump -u root -p test_db > test_db.bak

-- 비밀번호 입력
0000

-- 백업 파일 확인
code test_db.bak

-- 테이블 삭제
DROP TABLE TB_ADMIN;

-- 확인
SHOW TABLES;

-- 종료
exit

-- mysql로 복구
mysql -u test_user -p test_db < test_db.bak
mysql -u test_user -p test_db -e "source test_db.bak"
```

주의:

- 현재 저장소 루트에 `test_db.bak` 파일이 있다.
- 문서 메모상 PowerShell보다 `cmd`에서 복구가 안정적이라고 적혀 있다.
- 기본 연결 프로그램이 한글 오피스로 바인딩되면 백업 파일이 변형될 수 있다는 메모가 있다.

### 9. FastAPI DB 연동 확인

현재 코드의 `admins` 라우터는 `TB_ADMIN`을 직접 `SELECT`하지 않고 저장 프로시저 `SP_L_ADMIN`을 호출한다.

MySQL 저장 프로시저 예시:

```sql
DELIMITER $$
CREATE PROCEDURE SP_L_ADMIN ()
BEGIN
    SELECT ADMIN_NO, LOGIN_ID, PASSWD, NICK, EMAIL FROM TB_ADMIN;
END $$
DELIMITER ;

CALL SP_L_ADMIN();
```

현재 코드 기준 DB 연동 흐름:

1. `config.py`에서 접속 정보 정의
2. `model/mysql_test.py`에서 `mysql.connector.connect()` 후 `SP_L_ADMIN` 호출
3. `stored_results()`로 결과셋을 읽어 리스트에 담음
4. `controller/admins.py`에서 `list_admin()` 결과 반환
5. `app.py`에서 `admins.router` 등록

## 현재 폴더 구조

```text
uv-based-fastapi/
├─ README.md
├─ prompts/
│  └─ update-root-readme-from-project-status.md
└─ example/
   ├─ .python-version
   ├─ app.py
   ├─ config/
   │  └─ config.py
   ├─ controller/
   │  ├─ admins.py
   │  ├─ items.py
   │  └─ users.py
   ├─ model/
   │  └─ mysql_test.py
   ├─ main.py
   ├─ main_request.py
   ├─ pyproject.toml
   ├─ README.md
   └─ uv.lock
```

## 현재 상태상 주의

- `example/README.md` 파일은 존재하지만 비어 있다.
- `pyproject.toml`의 `readme = "README.md"`는 비어 있는 `example/README.md`를 가리킨다.
- `/admins/{list}` 라우트는 경로 파라미터를 선언하지만 함수 `list_admin()`은 인자를 받지 않는다.
- `model/mysql_test.py`는 `TB_ADMIN` 테이블, `SP_L_ADMIN` 저장 프로시저, MySQL 접속 정보 중 하나라도 맞지 않으면 실패한다.
- `model/mysql_test.py`는 결과를 단일 행 목록이 아니라 저장 프로시저 결과셋 목록 형태로 반환한다.
- `.venv`, `__pycache__` 같은 생성물은 작업 기준에서 제외한다.

## 문서 갱신 기준

아래 항목이 바뀌면 이 문서를 먼저 함께 수정한다.

- 실행 진입점
- 앱 정의 파일
- 라우터 구성
- 의존성
- 포트, 호스트, `reload` 설정
- 테스트 스크립트
- DB 접속 방식과 선행 준비물
- 실행 절차
