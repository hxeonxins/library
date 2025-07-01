from . import r

def test():
    return "redis connect ok"

# 도서 제목을 대출자에 맞춰 Redis에 저장
def cache_borrowed_book(borrower: str, title: str):
    key = f"borrower:{borrower}:books"
    r.rpush(key, title)

# 특정 대출자의 모든 대출 도서 조회
def get_cached_books(borrower: str):
    key = f"borrower:{borrower}:books"
    return r.lrange(key, 0, -1)

# 대출자 Redis 캐시 삭제 (반납 시 등)
def remove_cached_book(borrower: str, title: str):
    key = f"borrower:{borrower}:books"
    r.lrem(key, 0, title) #Redis 리스트에서 값이 title인 항목을 모두 삭제