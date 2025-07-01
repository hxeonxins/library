from . import con, cur

# def test():
#     return "sqlite connect ok"

from sqlite3 import connect

con = connect('./study.db', check_same_thread=False)
cur = con.cursor()

def insert_book(title: str, author: str) -> bool:
    try:
        sql = "INSERT INTO books(title, author) VALUES (?, ?)"
        cur.execute(sql, (title, author))
        con.commit()
        return True
    except Exception as e:
        print("도서 등록 에러:", e)
        return False

