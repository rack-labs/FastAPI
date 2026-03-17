import mysql.connector
from mysql.connector import Error
from config import config

def list_admin():
    results = []
    with mysql.connector.connect(**config.MYSQL_DB_CONFIG) as conn:
        cur = conn.cursor()
        try:
            # cur.execute("SELECT * FROM TB_ADMIN")
            # results = cur.fetchall()

            #stored procedure
            cur.callproc("SP_L_ADMIN")
            for result in cur.stored_results():
                results.append(result.fetchall())

        except Error as err:
            print(f"쿼리 에러: {err}")
            results = False
    return results
