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

@router.delete("/books/{book_id}")
def delete_book(book_id: int):
    success = service.remove_book_if_available(book_id)
    return success

from service.borrowings import borrow_book_service
from fastapi.responses import Response

class BorrowRequest(BaseModel):
    borrower: str
    title: str

@router.post("/borrows")
def borrow_book(req: BorrowRequest):
    success = borrow_book_service(req.borrower, req.title)
    return Response(content="true" if success else "false", media_type="text/plain")

@router.get("/borrows/month/{borrow_month}")
def get_borrowed_books_by_month(borrow_month: str):
    data = service.retrieve_borrowings_by_month(borrow_month)
    return data