from data import borrowings as data
from cache import borrower as cache

# def test():
#     db_test = data.test()
#     redis_test = cache.test()
#     return {"sqlite": db_test, "redis": redis_test}

def register_book(title: str, author: str):
    return data.insert_book(title, author)
