import random
import requests

from flask_bcrypt import Bcrypt
from flask_jwt_extended import decode_token

from app import app, db, customers, users


bcrypt = Bcrypt(app)

random_user_name = lambda: f'UserName{random.randint(0, 999999999999999)}'
random_customer_name = lambda: f'CustomerName{random.randint(0, 999999999999999)}'

random_book_name = f'BookName{random.randint(0, 999999999999999)}'
random_author_name = f'AuthorName{random.randint(0, 999999999999999)}'

base_url = 'http://127.0.0.1:5000'




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



    # url = /addBook'
    # headers = {
    #     'Content-Type': 'application/json',
    #     'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNTc2NzIxMywianRpIjoiYzJmYmI3ZDYtMWIwYS00ZDAyLWJiZDItODQxYWZiZjNlYjJkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzA1NzY3MjEzLCJjc3JmIjoiNTgwNDJiZDMtZmY5YS00YjI1LWEwM2ItOGJlNmRhMzBjYWJiIiwiZXhwIjoxNzA1Nzc0NDEzLCJyb2xlIjoiQWRtaW4ifQ.8IO10YtQJtc4UzrkJvZNNC0bOBqsJBjUMwZgjP56RSI'
    # }
    # data = {
    #     'name': random_book_name,
    #     'author' : 'AuthorName',
    #     "year_published" : 2022,
    # }

    # 

    # print (response.json())

    # response.status == 201

    # response = requests.get('/getallbooks')
    # response.data


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
    assert 'access_token' in response.json()


def main():
    test_funcs = [test_add_customer, test_register, test_login]

    for func in test_funcs:
        func()

        print(func.__name__, 'succeeded')
    

if __name__ == '__main__':
    main()
