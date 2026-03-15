import psycopg
import psycopg_pool
from config import config

pool_default = psycopg_pool.ConnectionPool(
    config.PGSQL_TEST_DATABASE_STRING,
    min_size=config.PGSQL_TEST_POOL_MIN_SIZE,
    max_size=config.PGSQL_TEST_POOL_MAX_SIZE,
    max_idle=config.PGSQL_TEST_POOL_MIN_IDLE,
    timeout=5,
)

def list_admin():
    try:
        with pool_default.connection() as conn:
            cur = conn.cursor(row_factory=psycopg.rows.dict_row)
            cur.execute("CALL SP_L_ADMIN('out1')")
            results = cur.execute("FETCH ALL FROM out1").fetchall()
            conn.commit()
            return results
    except psycopg_pool.PoolTimeout as err:
        raise RuntimeError(
            "PostgreSQL connection timeout. Check that the DB server is running on 127.0.0.1:5432 and the credentials are correct."
        ) from err
    except psycopg.Error as err:
        raise RuntimeError(f"PostgreSQL query failed: {err}") from err
