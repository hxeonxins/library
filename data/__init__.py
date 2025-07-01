from sqlite3 import connect, Connection, Cursor
from typing import Optional

con: Optional[Connection] = None
cur: Optional[Cursor] = None


def get_db():
    global con, cur
    if con is None:
        con = connect('./study.db', check_same_thread=False)
        cur = con.cursor()
        # books 테이블 구성
        sql = ("create table if not exists books("
               "book_id integer primary key autoincrement, "
               "title text unique, "
               "author text, "
               "available INTEGER DEFAULT 1)")
        cur.execute(sql)
        con.commit()
        sql = ("insert or ignore into books(title, author) values (?, ?)")
        cur.execute(sql, ("삼국지1", "침착맨"))
        cur.execute(sql, ("삼국지2", "침착맨"))
        cur.execute(sql, ("삼국지3", "침착맨"))
        con.commit()

        # borrowings 테이블 구성
        sql = ("create table if not exists borrowings("
               "borrow_id integer primary key autoincrement, "
               "book_id integer, "
               "borrower text, "
               "borrowed_at text default current_timestamp, "
               "returned_at text, "
               "foreign key(book_id) references books(book_id), "
               "unique(book_id, borrower))")
        cur.execute(sql)
        cur.execute("PRAGMA foreign_keys = ON")
        con.commit()
        sql = ("insert or ignore into borrowings(book_id, borrower) values(?,?)")
        cur.execute(sql, ("2", "choi"))
        con.commit()

get_db()