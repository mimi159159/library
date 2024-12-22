# Library Management System

This is a simple Library Management System built with Python and Flask. It allows users to manage books, customers, and loans in a library.

## Features

- User registration and login
- Add and manage customers
- Add and manage books
- Loan and return books
- Track late book returns
- Profile information for logged-in users
- Authentication and authorization using JWT (JSON Web Tokens)

## Prerequisites

Before running the application, make sure you have the following dependencies installed:

- alembic==1.13.1
- aniso8601==9.0.1
- bcrypt==4.1.2
- blinker==1.7.0
- cffi==1.16.0
- click==8.1.7
- colorama==0.4.6
- cryptography==41.0.7
- Flask==3.0.0
- Flask-Bcrypt==1.0.1
- Flask-Cors==4.0.0
- Flask-JWT-Extended==4.6.0
- Flask-Migrate==4.0.5
- Flask-RESTful==0.3.10
- Flask-SQLAlchemy==3.1.1
- greenlet==3.0.3
- itsdangerous==2.1.2
- Jinja2==3.1.2
- jwt==1.3.1
- Mako==1.3.0
- MarkupSafe==2.1.3
- pycparser==2.21
- PyJWT==2.0.1
- pytz==2023.3.post1
- six==1.16.0
- SQLAlchemy==2.0.25
- typing_extensions==4.9.0
- Werkzeug==3.0.1
- urllib3==2.1.0
- requests==2.31.0
- idna==3.6
- charset-normalizer==3.3.2
- certifi==2023.11.17


You can install these dependencies using pip:
- see "getting started" section 3

## Getting Started

1. Clone this repository:
git clone https://github.com/mimi159159/library.git
cd library-management-system


2. Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate # On Windows, use venv\Scripts\activate


3. Install the project dependencies:
pip install -r requirements.txt


4. Run the application:
   cd backhand
   python app.py


The application should now be running locally at http://localhost:5000.

## API Endpoints

- `POST /register`: Register a new user.
- `POST /login`: Authenticate and log in a user.
- `GET /allBooks`: Retrieve a list of all books.
- `GET /allCust`: Retrieve a list of all customers.
- `GET /allLoans`: Retrieve a list of all loans.
- `GET /allLateLoan`: Retrieve a list of all late loan records.
- `POST /addCust`: Add a new customer (requires authentication).
- `POST /addBook`: Add a new book (requires authentication).
- `POST /loanBook`: Loan a book to a customer (requires authentication).
- `POST /returnBook`: Return a book (requires authentication).
- `POST /searchCust`: Search for a customer by name.
- `POST /searchBook`: Search for a book by name.
- `GET /profile`: Retrieve user profile information (requires authentication).

Please refer to the `app.py` file for detailed information on each endpoint's functionality and request/response format.

## unit test
- file name= test2.py
- to run test : py test2.py + py app.py 
- run together with app.py 




## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

