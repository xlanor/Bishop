import pymysql
from contextlib import closing
from pymysql import IntegrityError
from cfg import SQL
def insert_into_post(post_text:str,hash_value:str):
    with closing(pymysql.connect(**SQL)) as conn:
        conn.autocommit(True)
        with closing(conn.cursor()) as cur:
            try:
                cur.execute("""
                            INSERT INTO posts VALUES(%s,%s,%s)
                            """,(post_text,0,hash_value,)
                            
                            )
            except IntegrityError:
                print("Duplicate pass")
                pass

def get_unposted():
    with closing(pymysql.connect(**SQL)) as conn:
        conn.autocommit(True)
        with closing(conn.cursor()) as cur:
            try:
                cur.execute("""
                            SELECT * FROM posts WHERE is_posted = 0
                            """)
                if cur.rowcount == 0:
                    return None
                else:
                    return cur.fetchall()
            except Exception as e:
                print(str(e))


def update_posted(hash_value:str):
    with closing(pymysql.connect(**SQL)) as conn:
        conn.autocommit(True)
        with closing(conn.cursor()) as cur:
            try:
                cur.execute("""
                            UPDATE posts SET is_posted = 1 WHERE hash_value = %s
                            """,(hash_value,))
            except Exception as e:
                print(str(e))
