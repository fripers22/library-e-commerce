from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.book_service import BookService
from app.domain.book_model import BookCreate, BookUpdate, BookResponse

router = APIRouter(prefix="/libros", tags=["Libros"])


def get_db():
	"""Yield a database session and ensure it's closed."""
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
	"""Create a new book."""
	service = BookService(db)
	return service.create_book(book)


@router.get("/", response_model=list[BookResponse])
def get_all_books(db: Session = Depends(get_db)):
	"""Get all books."""
	service = BookService(db)
	return service.get_all_books()


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
	"""Get a book by ID."""
	service = BookService(db)
	return service.get_book(book_id)


@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
	"""Update a book."""
	service = BookService(db)
	return service.update_book(book_id, book)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
	"""Delete a book."""
	service = BookService(db)
	service.delete_book(book_id)
	return None
