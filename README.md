# FastAPI MongoDB CRUD API

This is a simple CRUD (Create, Read, Update, Delete) API built with FastAPI and MongoDB. It allows you to manage a collection of books, including adding new books, retrieving all books, retrieving a single book by its ID, updating a book, and deleting a book.

## Requirements

- Python 3.7+
- MongoDB

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your_username/fastapi-mongodb-crud-api.git
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the FastAPI server:

    ```bash
    uvicorn app:app --reload
    ```

## API Endpoints

- **POST /books/** - Add a new book
- **GET /books/** - List all books
- **GET /books/{id}** - Get a single book by its ID
- **PUT /books/{id}** - Update a book by its ID
- **DELETE /books/{id}** - Delete a book by its ID

### Request and Response Examples

#### Adding a New Book

Request:

```json
POST /books/
{
    "id": "11",
    "name": "The Catcher in the Rye",
    "img": "https://bit.ly/3y2P7Cg",
    "summary": "The novel's protagonist, Holden Caulfield, a seventeen-year-old boy, relates a tale of personal dislocation and mental turmoil"
}
