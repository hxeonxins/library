from data import borrowings as data
from cache import borrower as cache
from data.borrowings import get_available_books, return_book_db


# def test():
#     db_test = data.test()
#     redis_test = cache.test()
#     return {"sqlite": db_test, "redis": redis_test}

def register_book(title: str, author: str):
    return data.insert_book(title, author)

def list_available_books():
    return get_available_books()

from data.borrowings import delete_available_book

def remove_book_if_available(book_id: int) -> bool:
    return delete_available_book(book_id)

from data.borrowings import borrow_book as db_borrow_book

def borrow_book_service(borrower: str, title: str) -> bool:
    return db_borrow_book(borrower, title)

from data.borrowings import get_borrowings_by_month

def retrieve_borrowings_by_month(month: str):
    try:
        return get_borrowings_by_month(month)
    except Exception as e:
        print("대출 월 조회 오류:", e)
        return []

from cache.borrower import get_cached_books, remove_cached_book


def get_borrowed_books_from_cache(borrower: str):
    books = get_cached_books(borrower)
    return {"borrower": borrower, "books": books}

def return_book_service(borrower: str, title: str) -> bool:
    success = return_book_db(borrower, title)
    if success:
        remove_cached_book(borrower, title) # 레디스에서 책 제목 삭제
    return success