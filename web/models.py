from pydantic import BaseModel

class BookRegister(BaseModel):
    title: str
    author: str

class BorrowRequest(BaseModel):
    borrower: str
    title: str