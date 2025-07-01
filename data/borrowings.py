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

def get_available_books():
    with connect("study.db") as con:
        cur = con.cursor()
        cur.execute("SELECT title, author FROM books WHERE available = 1")
        return [{"title": t, "author": a} for t, a in cur.fetchall()]