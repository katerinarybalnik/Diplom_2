from faker import Faker
import allure
import requests

from urls import CREATE_USER_URL

fake = Faker()


@allure.title("Создание уникального пользователя")
def test_create_unique_user():
    payload = {
        "email": fake.email(),
        "password": "Password123",
        "name": "Test User"
    }

    response = requests.post(CREATE_USER_URL, json=payload)

    assert response.status_code == 200
    assert response.json()["success"] is True

@allure.title("Создание пользователя, который уже зарегистрирован")
def test_create_existing_user():
    payload = {
        "email": fake.email(),
        "password": "Password123",
        "name": "Test User"
    }

    requests.post(CREATE_USER_URL, json=payload)
    response = requests.post(CREATE_USER_URL, json=payload)

    assert response.status_code == 403
    assert response.json()["success"] is False
    assert response.json()["message"] == "User already exists"

@allure.title("Создание пользователя без пароля")
def test_create_user_without_password():
    payload = {
        "email": fake.email(),
        "name": "Test User"
    }

    response = requests.post(CREATE_USER_URL, json=payload)

    assert response.status_code == 403
    assert response.json()["success"] is False
    assert response.json()["message"] == "Email, password and name are required fields"