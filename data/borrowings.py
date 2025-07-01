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

def delete_available_book(book_id: int) -> bool:
    with connect("study.db") as con:
        cur = con.cursor()
        cur.execute("SELECT available FROM books WHERE book_id = ?", (book_id,))
        row = cur.fetchone()

        if row is None or row[0] == 0:  # 책이 없거나 대출 중
            return False

        cur.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
        con.commit()
        return True

def borrow_book(borrower: str, title: str) -> bool:
    try:
        con = connect("study.db", check_same_thread=False)
        cur = con.cursor()

        # 대출 가능한 책인지 확인
        cur.execute("SELECT book_id FROM books WHERE title = ? AND available = 1", (title,))
        book = cur.fetchone()
        if not book:
            return False

        book_id = book[0]

        # 대출 처리
        cur.execute("INSERT INTO borrowings(book_id, borrower) VALUES (?, ?)", (book_id, borrower))
        cur.execute("UPDATE books SET available = 0 WHERE book_id = ?", (book_id,))
        con.commit()
        return True
    except Exception as e:
        print("대출 오류:", e)
        return False