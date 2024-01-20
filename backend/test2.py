from datetime import timedelta
import random
import requests

from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

from app import app, db, customers, users, books,loans,late_loan


bcrypt = Bcrypt(app)

random_user_name = lambda: f'UserName{random.randint(0, 999999999999999)}'
random_customer_name = lambda: f'CustomerName{random.randint(0, 999999999999999)}'

random_book_name = f'BookName{random.randint(0, 999999999999999)}'
random_author_name = f'AuthorName{random.randint(0, 999999999999999)}'
random_year = random.randint (0,9999)

base_url = 'http://127.0.0.1:5000'


def get_access_token():
    customer_name = random_customer_name()
    user_name = random_user_name()

    with app.app_context():
        user = users(username=user_name, password=bcrypt.generate_password_hash('pw').decode('utf-8'), role='Admin', customer_name='customer')

        db.session.add(customers(name=customer_name, age=123, city='city123'))
        db.session.add(user)
        db.session.commit()

        expires = timedelta(hours=2)
        access_token = create_access_token(identity=user.id, expires_delta=expires, additional_claims={'role': user.role})

    return access_token


access_token_for_tests = get_access_token()


def test_add_customer():
    customer_name = random_customer_name()

    response = requests.post(
        url=f'{base_url}/addCust',
        data={
            'name': customer_name,
            'city': 'the city',
            'age': 88,
        })
    
    with app.app_context():
        customer = customers.query.filter(customers.name == customer_name).first()

    assert response.status_code == 200
    assert customer.name == customer_name
    assert customer.age == 88
    assert customer.city == 'the city'


def test_register():
    customer_name = random_customer_name()
    user_name = random_user_name()

    with app.app_context():
        db.session.add(customers(name=customer_name, age=123, city='city123'))
        db.session.commit()

    response = requests.post(
        url=f'{base_url}/register',
        data={
            'username': user_name,
            'password': 'pw',
            'role': 'Admin',
            'customer_name': customer_name
        })
    
    with app.app_context():
        user = users.query.filter(users.customer_name == customer_name).first()
    
    assert response.status_code == 201
    assert user.username == user_name
    assert bcrypt.check_password_hash(user.password, 'pw') == True
    assert user.role == 'Admin'
    assert user.customer_name == customer_name


def test_login():
    customer_name = random_customer_name()
    user_name = random_user_name()

    with app.app_context():
        db.session.add(customers(name=customer_name, age=123, city='city123'))
        db.session.add(users(username=user_name, password=bcrypt.generate_password_hash('pw').decode('utf-8'), role='Admin', customer_name='customer'))
        db.session.commit()

    response = requests.post(
        url=f'{base_url}/login',
        json={
            'username': user_name,
            'password': 'pw'
        })
    
    assert response.status_code == 200
    # assert 'access_token' in response.json()


def test_all_books():
    response = requests.get(url=f'{base_url}/allBooks')
    all_books = response.json()

    assert response.status_code == 200
    assert len(all_books) > 0
    assert 'author' in all_books[0]
    assert 'id' in all_books[0]
    assert 'image_path' in all_books[0]
    assert 'name' in all_books[0]
    assert 'type' in all_books[0]
    assert 'year_published' in all_books[0]
    

def test_all_cust():
    response = requests.get(url=f'{base_url}/allCust')
    assert response.status_code == 200
    

def test_all_loans():
    response = requests.get(url=f'{base_url}/allLoans')
    assert response.status_code == 200


def test_all_lateLoan():
    response = requests.get(url=f'{base_url}/allLateLoan')
    assert response.status_code == 200

# access_token_for_tests

def test_add_book():
    book_name = random_book_name
    author_name = random_author_name
    year =  random_year
    print(access_token_for_tests)
    response = requests.post(
        url=f'{base_url}/addBook',
        headers={
            'Authorization': 'Bearer ' + access_token_for_tests
        },
        data={
         'name' : book_name,
         'author' : author_name,
         'year_published' : year
          } )
    with app.app_context():
       book = books.query.filter((books.name == book_name), (books.author == author_name)).first()
    assert response.status_code == 200
    assert book.name == book_name
    assert book.author == author_name
    assert book.year_published == year


def test_search_book():
    book_name = random_book_name
    author_name = random_author_name
    year =  random_year
    with app.app_context():
        db.session.add(books(name=book_name,author =author_name , year_published =year ))
        db.session.commit()

    response = requests.post(
        url=f'{base_url}/searchBook',
        data={
            'book_name': book_name
        })
    assert response.status_code == 200
    # print(response.json())


def test_search_customer():
    customer_name = random_customer_name()

    with app.app_context():
        db.session.add(customers(name=customer_name, age=123, city='city123'))
        db.session.commit()


    response = requests.post(
        url=f'{base_url}/searchCust',
        data={
            'cust_name': customer_name
        })
    assert response.status_code == 200
    # print(response.json())   


def test_loan_book():
    pass

def main():
    test_funcs = [test_add_customer, test_register, test_login,test_all_books,test_all_cust,test_all_lateLoan,test_all_loans,
                  test_add_book,test_search_book, test_search_customer]

    for func in test_funcs:
        func()

        print(func.__name__, 'succeeded')
    

if __name__ == '__main__':
    main()

# TODO
# make sure addCustomer is still working from the frontend because we deleted the token code
# create more tests