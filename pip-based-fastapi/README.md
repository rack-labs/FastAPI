# FastAPI
fastapi-team-starter
## basic FastAPI starter app

### git ignore 대상
```gitignore
.venv/
__pycache__/
*.pyc

```

### 가상환경 실행
```bash
# 가상환경 설치
python -m venv .venv

# 가상환경 실행
.\.venv\Scripts\activate

# 가상환경 종료
deactivate
```


### fastapi, uvicorn 설치
```bash
# 패키지 설치
pip install fastapi
pip install uvicorn

# 확인
pip list

# 현재 프로젝트의 의존성 목록을 파일로 고정 저장
pip freeze > requirements.txt
```

### fastapi 활용 간단한 코드 작성(main.py)
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
### uvicorn을 이용해 실행
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

## controller expansion
컨트롤러(main.py)가 방대해지는 것을 방지한다.

### main.py의 read_item을 별도 컨트롤러(라우터)로 변경
```python
# ===== main.py =====
    from fastapi import FastAPI
    from controller import items #추가
    # from typing import Union

    app = FastAPI()
    app.include_router(items.router) #추가

    @app.get("/")
    def read_root():
        return{"Hello":"world"}

    # -> /controller/items.py로 이관
    # @app.get("/items/{item_id}") 
    # def read_item(item_id: int, q: Union[str, None] = None):
    #     return {"item_id": item_id, "q": q}

# ===== /controller/__init__.py ===== (최근 버전에서는 안만들어줘도 됨)

# ===== /controller/items.py ===== 
from typing import Union
from fastapi import APIRouter

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description":"Not found"}},
)

@router.get("/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

### controller에 users 라우트 엔드포인트 추가

```python
# main.py (users 추가)
    from fastapi import FastAPI
    from controller import items, users #

    app = FastAPI()
    app.include_router(items.router)
    app.include_router(users.router) #

    @app.get("/")
    def read_root():
        return{"Hello":"world"}


# users.py (Uvicorn 없이 간단히 작성)
    from fastapi import APIRouter

    router = APIRouter(
        prefix="/users",
        tags=["users"],
        responses={404: {"description":"Not found"}},
    )

    @router.get("/{user_id}")
    def read_user(user_id: int):
        return {"user_id": user_id}

```
fastapi는 db가 필요하다.

## PostgreSQL 

### DB세팅

```bash
# powershell 띄워 scoop 설치해준다. scoop으로 PostgreSQL을 설치하게 될 것이다.
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression

# powershell 재시작 후 PostgreSQL 설치
scoop install postgresql

# PostgreSQL server 시작
pg_ctl start

# 로그인 절차
psql -U postgres

# user 생성
create user test_user with password 'test123';

# DB 생성
create database test_db with encoding='utf-8' owner test_user;

# 빠져나오기
ctl \q

# 생성된 사용자와 db로 로그인
psql -U test_user -d test_db
```

```SQL
-- 아래 sql 작성, 완료시 'CREATE TABLE' 결과 표시됨.
CREATE TABLE TB_ADMIN
(
	ADMIN_NO Serial NOT NULL,
    LOGIN_ID Varchar(20) NOT NULL UNIQUE,
    PASSWD Varchar(20) NOT NULL,
    NICK Varchar(20) NOT NULL,
    EMAIL Varchar(40),
    PRIMARY KEY (ADMIN_NO)
) Without Oids;

-- 아래 두개 데이터 작성
INSERT INTO TB_ADMIN(LOGIN_ID, PASSWD, NICK, EMAIL)
VALUES('hongildong', 'ajtwlddl', 'HONG', 'hgd@gmail.com');

INSERT INTO TB_ADMIN(LOGIN_ID, PASSWD, NICK, EMAIL)
VALUES('jangnara', 'dlQmsdl', 'JANG', 'jnr@gmail.com');

-- 작성한 데이터 확인
select * from tb_admin;

-- procedure
CREATE OR REPLACE PROCEDURE public.SP_L_ADMIN(out1 refcursor)
    LANGUAGE plpgsql
AS $procedure$
    BEGIN
        OPEN out1 FOR
        SELECT ADMIN_NO, LOGIN_ID, PASSWD, NICK, EMAIL FROM TB_ADMIN;
    END;
$procedure$
;

-- function 
CREATE OR REPLACE FUNCTION public.FN_L_ADMIN(out1 refcursor)
    RETURNS SETOF refcursor
    LANGUAGE plpgsql
AS $function$
    BEGIN 
        OPEN out1 FOR 
        SELECT ADMIN_NO, LOGIN_ID, PASSWD, NICK, EMAIL FROM TB_ADMIN;
        RETURN NEXT out1;
    END;
$function$
;

-- 작성한 PROCEDURE와 FUNCTION이 잘 작동하는지 확인
    --function 호출
    begin; -- 이후 오타났을 시 'rollback;' 후 다시 'begin;'
    select fn_l_admin('out1');
    fetch all from out1;
    commit;

    --procedure 호출
    call sp_l_admin('out1');
    fetch all from out1;
    commit;
```

### DB연동

python에서 postgres sql을 이용하는 패키지 설치

```bash
# psycopg 패키지 설치
pip install "psycopg[binary,pool]"
```

```python
# config/__init__.py
# config/contig.py
    # pgsql 연결을 위한 DBstring
    PGSQL_TEST_DATABASE_STRING = "host=127.0.0.1 dbname=test_db user=test_user password=test123 port=5432"
    # connection pool에 관한 설정
    PGSQL_TEST_POOL_MIN_SIZE = 10
    PGSQL_TEST_POOL_MAX_SIZE = 10
    PGSQL_TEST_POOL_MIN_IDLE = 60

# model/__init__.py
# model/pgsql_test.py
    import psycopg
    import psycopg_pool
    from config import config

    pool_default = psycopg_pool.ConnectionPool(
        config.PGSQL_TEST_DATABASE_STRING,
        min_size=config.PGSQL_TEST_POOL_MIN_IDLE,
        max_size=config.PGSQL_TEST_POOL_MAX_SIZE,
        max_idle=config.PGSQL_TEST_POOL_MIN_IDLE
    )

    def list_admin():
        with pool_default.connection() as conn:
            cur = conn.cursor(row_factory=psycopg.rows.dict_row)
            try:
                results = cur.execute('SELECT * FROM TB_ADMIN').fetchall()
            except psycopg.ProgrammingError as err:
                print(f'Error querying: {err}')
            except psycopg.ProgrammingError as err:
                print('Database error via psycopg.  %s',err)
                results = False
            except psycopg.IntegrityError as err:
                print('PostgreSQL integrity error via psycopg. %s', err)
                results = False
        return results

# controller/admins.py
    from fastapi import APIRouter
    from model import pgsql_test

    router = APIRouter(
        prefix="/admins",
        tags=["admins"],
        responses={404: {"description":"Not found"}},
    )

    @router.get("list") #
    def list_admin():
        results = pgsql_test.list_admin()
        return results

# main.py 
    from fastapi import FastAPI
    from controller import items, users, admins #

    app = FastAPI()
    app.include_router(items.router)
    app.include_router(users.router)
    app.include_router(admins.router) #

    @app.get("/")
    def read_root():
        return{"Hello":"world"}
```


