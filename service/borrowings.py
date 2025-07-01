from data import borrowings as data
from cache import borrower as cache
from data.borrowings import get_available_books


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
