
#  library-management-system-fastapi

Create a library management system that allows users to borrow and return books. The system should support the following functionality

### User Management:
-	User registration with name, email, password, and role (user/librarian)
-	Secure login/logout using JWT authentication
-	Role-based authorization for specific actions (e.g., only librarians can add/remove books)

### Book Management:

-	Book data model with title, author, genre, availability status, etc.
-	Fast API endpoints for CRUD operations on books (Create, Read, Update, Delete) with authorization checks
-	Prevent duplicate book entries during creation
-	Define data models for books using Pydantic, including attributes like title, author, genre etc
-	Implement validation of user input using Pydantic validators.
-	Write unit tests for your API endpoints.
-	Implement pagination for book listings

###	Borrowing/Returning:
-	Book search by title, author, or genre with availability information
-	Users can borrow available books and see due dates
-	Implement system checks to prevent invalid borrowing attempts
-	Allow for returning borrowed books, updating availability
