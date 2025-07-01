from fastapi import APIRouter
from pydantic import BaseModel

from service import borrowings as service

router = APIRouter()

#도서 제목(title), 도서 저자(author)를 받아 해당 도서를 등록한다.

class bookRegister(BaseModel):
    title: str
    author: str
@router.post("/books")
def register_book(req: bookRegister):
    return service.register_book(req.title, req.author)

@router.get("/books")
def get_books():
    return service.list_available_books()