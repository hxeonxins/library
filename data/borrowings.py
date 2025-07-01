from cache.borrower import cache_borrowed_book
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

        #캐싱
        cache_borrowed_book(borrower, title)

        return True
    except Exception as e:
        print("대출 오류:", e)
        return False


def get_borrowings_by_month(borrow_month: str):
    con = connect("study.db", check_same_thread=False)
    cur = con.cursor()

    like_pattern = borrow_month + "%"  # 예: 2025-06%

    sql = """
          SELECT b.borrower, bk.title, bk.author
          FROM borrowings b
                   JOIN books bk ON b.book_id = bk.book_id
          WHERE b.borrowed_at LIKE ? \
          """
    cur.execute(sql, (like_pattern,))
    rows = cur.fetchall()

    return [{"borrower": r[0], "title": r[1], "author": r[2]} for r in rows]

def return_book_db(borrower: str, title: str) -> bool:
    try:
        with connect("study.db") as con:
            cur = con.cursor()

            # 책 ID 찾기
            cur.execute("SELECT book_id FROM books WHERE title = ?", (title,))
            row = cur.fetchone()
            if not row:
                return False
            book_id = row[0]

            # borrowings에 존재하는지 확인
            cur.execute("SELECT * FROM borrowings WHERE book_id = ? AND borrower = ? AND returned_at IS NULL",
                        (book_id, borrower))
            if not cur.fetchone():
                return False

            # 반환 처리
            cur.execute("UPDATE books SET available = 1 WHERE book_id = ?", (book_id,))
            cur.execute("UPDATE borrowings SET returned_at = CURRENT_TIMESTAMP WHERE book_id = ? AND borrower = ?",
                        (book_id, borrower))
            con.commit()
        return True
    except Exception as e:
        print("반납 오류:", e)
        return False