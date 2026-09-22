from faker import Faker
import allure
import requests

from urls import CREATE_USER_URL, CREATE_ORDER_URL, INGREDIENTS_URL

fake = Faker()

@allure.title("Создание заказа с авторизацией")
def test_create_order_with_authorization():
    user = {"email": fake.email(),
        "password": "Password123","name": "Test User"}

    registration = requests.post(CREATE_USER_URL, json=user)
    token = registration.json()["accessToken"]

    ingredients_response = requests.get(INGREDIENTS_URL)
    ingredient_id = ingredients_response.json()["data"][0]["_id"]

    response = requests.post(CREATE_ORDER_URL,json={"ingredients": [ingredient_id]},headers={"Authorization": token})

    assert response.status_code == 200
    assert response.json()["success"] is True


@allure.title("Создание заказа без авторизации")
def test_create_order_without_authorization():
    ingredients_response = requests.get(INGREDIENTS_URL)
    ingredient_id = ingredients_response.json()["data"][0]["_id"]

    response = requests.post(CREATE_ORDER_URL,json={"ingredients": [ingredient_id]})

    assert response.status_code == 200
    assert response.json()["success"] is True


@allure.title("Создание заказа без ингредиентов")
def test_create_order_without_ingredients():
    response = requests.post(CREATE_ORDER_URL,json={"ingredients": []})

    assert response.status_code == 400
    assert response.json()["success"] is False
    assert response.json()["message"] == "Ingredient ids must be provided"


@allure.title("Создание заказа с неверным хешем ингредиента")
def test_create_order_with_invalid_ingredient():
    response = requests.post(CREATE_ORDER_URL,json={"ingredients": ["invalid_ingredient_hash"]})

    assert response.status_code == 500