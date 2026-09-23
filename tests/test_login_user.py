from faker import Faker
import pytest
import allure
import requests

from urls import CREATE_USER_URL, LOGIN_USER_URL

fake = Faker()

@allure.title("Авторизация с правильными данными")
def test_login_with_valid_credentials():
    payload = {
        "email": fake.email(),
        "password": "Password123",
        "name": "Test User"
    }

    registration = requests.post(CREATE_USER_URL, json=payload)
    assert registration.status_code == 200

    response = requests.post(LOGIN_USER_URL, json={
        "email": payload["email"],
        "password": payload["password"]
    })

    assert response.status_code == 200
    assert response.json()["success"] is True


@allure.title("Авторизация с неправильными данными")
@pytest.mark.parametrize("wrong_field", ["email", "password"])
def test_login_with_invalid_credentials(wrong_field):
    payload = {
        "email": fake.email(),
        "password": "Password123",
        "name": "Test User"
    }

    registration = requests.post(CREATE_USER_URL, json=payload)
    assert registration.status_code == 200

    login_data = {
        "email": payload["email"],
        "password": payload["password"]
    }
    login_data[wrong_field] = "WrongValue"

    response = requests.post(LOGIN_USER_URL, json=login_data)

    assert response.status_code == 401
    assert response.json()["success"] is False
    assert response.json()["message"] == "email or password are incorrect"