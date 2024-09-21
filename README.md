# CowryWiseLMS
A event driven microservice architecture task


Frontend API:
POST /users/ - Enroll a user user created

GET /books/ - List all available books

GET /books/{book_id}/ - Get a single book by its ID

GET /books/filter/ - Filter books by publisher or category (query parameters)

POST /books/{book_id}/borrow - Borrow a book for a specified duration (days) 


.........................................................................................

POST /admin/books/ - Add a new book to the catalogue new book added

DELETE /admin/books/{book_id} - Remove a book from the catalogue book deleted

GET /admin/users/ - List all users

GET /admin/borrowed_books/ - List users and the books they’ve borrowed

GET /admin/unavailable_books/ - List unavailable books and their available dates..
