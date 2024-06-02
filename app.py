from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

# Define the FastAPI app
app = FastAPI()

# MongoDB connection settings
MONGO_DETAILS = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.bookstore
book_collection = database.get_collection("books")

# Define the Book model
class Book(BaseModel):
    id: str
    name: str
    img: str
    summary: str

class BookUpdate(BaseModel):
    name: str = None
    img: str = None
    summary: str = None

# Utility function to convert MongoDB document to dictionary
def book_helper(book) -> dict:
    return {
        "id": str(book["_id"]),
        "name": book["name"],
        "img": book["img"],
        "summary": book["summary"],
    }

# Create a new book
@app.post("/books/", response_description="Add new book", response_model=Book)
async def create_book(book: Book):
    book = await book_collection.insert_one(book.dict())
    new_book = await book_collection.find_one({"_id": book.inserted_id})
    return book_helper(new_book)

# Read all books
@app.get("/books/", response_description="List all books", response_model=List[Book])
async def list_books():
    books = []
    async for book in book_collection.find():
        books.append(book_helper(book))
    return books

# Read a book by ID
@app.get("/books/{id}", response_description="Get a single book", response_model=Book)
async def read_book(id: str):
    book = await book_collection.find_one({"_id": ObjectId(id)})
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book_helper(book)

# Update a book by ID
@app.put("/books/{id}", response_description="Update a book", response_model=Book)
async def update_book(id: str, book: BookUpdate):
    book = {k: v for k, v in book.dict().items() if v is not None}
    if len(book) >= 1:
        update_result = await book_collection.update_one({"_id": ObjectId(id)}, {"$set": book})
        if update_result.modified_count == 1:
            updated_book = await book_collection.find_one({"_id": ObjectId(id)})
            return book_helper(updated_book)
    existing_book = await book_collection.find_one({"_id": ObjectId(id)})
    if existing_book:
        return book_helper(existing_book)
    raise HTTPException(status_code=404, detail="Book not found")

# Delete a book by ID
@app.delete("/books/{id}", response_description="Delete a book")
async def delete_book(id: str):
    delete_result = await book_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
