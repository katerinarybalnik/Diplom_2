import uuid

import allure
import requests

from urls import CREATE_USER_URL, LOGIN_USER_URL


@allure.title("Авторизация с правильными данными")
def test_login_with_valid_credentials():
    payload = {
        "email": f"test_{uuid.uuid4().hex}@example.com",
        "password": "Password123",
        "name": "Test User"
    }

    requests.post(CREATE_USER_URL, json=payload)

    response = requests.post(LOGIN_USER_URL, json={
        "email": payload["email"],
        "password": payload["password"]
    })

    assert response.status_code == 200
    assert response.json()["success"] is True


@allure.title("Авторизация с неправильным паролем")
def test_login_with_invalid_password():
    payload = {
        "email": f"test_{uuid.uuid4().hex}@example.com",
        "password": "Password123",
        "name": "Test User"
    }

    requests.post(CREATE_USER_URL, json=payload)

    response = requests.post(LOGIN_USER_URL, json={
        "email": payload["email"],
        "password": "WrongPassword"
    })

    assert response.status_code == 401
    assert response.json()["success"] is False
    assert response.json()["message"] == "email or password are incorrect"