from . import r

def test():
    return "redis connect ok"

# 주의: 레디스 cli 접속 시  docker exec -it redis redis-cli --raw 로 접속해야 한글 인코딩이 깨지지 않습니다!!
# 키를 조회했을 때 이상하게 뜬다면 위와 같이 접속해 주세요!!

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