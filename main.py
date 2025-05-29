from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from google_books_api_wrapper.api import GoogleBooksAPI
import os

app = FastAPI()

client = GoogleBooksAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@app.post("/book",response_class=HTMLResponse)
async def get_book(request: Request, book: str = Form(...)):
    books = await search_book(book)
    return templates.TemplateResponse("result.html", {
        "request": request,
        "books": books,  # Передаем книги в шаблон
        "book_title": book  # Передаем поисковый запрос
    })


async def search_book(book):
    books = client.search_book(book)
    #
    # books_set = {}
    # for book in books:
    #     books_set = {"Название": book.title, "Aвтор(ы)": book.authors, "date publish": book.publisher}
    # return books_set
    books_data = []
    for book in books:
        book_dict = {
            "title": book.title if hasattr(book, "title") else "No title",
            "authors": book.authors if hasattr(book, "authors") else "Unknown",
            "publisher": book.publisher if hasattr(book, "publisher") else "Unknown",
            "published_date": book.published_date if hasattr(book, "published_date") else "Unknown",
            "thumbnail": book.thumbnail if hasattr(book, "thumbnail") else None,
            "large_thumbnail": book.large_thumbnail if hasattr(book, "large_thumbnail") else None,
            "preview_link": book.preview_link if hasattr(book, "preview_link") else None
        }
        books_data.append(book_dict)
    return books_data