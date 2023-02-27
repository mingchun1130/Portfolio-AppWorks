import json
from random import choices, randint

import allure
import pytest

from api_objects.order import OrderAPI
from database.stylish_backend import StylishBackend
from page_objects.prime_page import PrimePage


@pytest.fixture
def prime(driver) -> str:
    return PrimePage(driver).get_prime()


@pytest.fixture
def shopping_cart(db_products) -> list:
    buy_amount = randint(1, 5)
    df = db_products.drop(["image_id", "image"], axis=1).drop_duplicates(subset="variant_id").sample(buy_amount)
    product_info = (
        df[["id", "main_image", "title", "price", "size"]]
        .rename(columns={"main_image": "image", "title": "name"})
        .to_dict("records")
    )
    color = (
        df[["color_code", "color_name"]].rename(columns={"color_code": "code", "color_name": "name"}).to_dict("records")
    )
    quantity = choices(range(1, 10), k=buy_amount)
    return [x[0] | {"color": x[1], "qty": x[2]} for x in list(zip(product_info, color, quantity))]


@pytest.fixture
def order_info(prime: str, shopping_cart: list):
    freight = 30
    subtotal = sum(product["price"] * product["qty"] for product in shopping_cart)
    return {
        "prime": prime,
        "order": {
            "shipping": "delivery",
            "payment": "credit_card",
            "subtotal": subtotal,
            "freight": freight,
            "total": subtotal + freight,
            "recipient": {
                "name": "陳大文",
                "phone": "0912345678",
                "email": "abc@abc.com",
                "address": "台北市",
                "time": "anytime",
            },
            "list": shopping_cart,
        },
    }


@pytest.fixture
def order(valid_user_account: dict):
    _order = OrderAPI()
    login_info = valid_user_account.copy()
    login_info.update({"provider": "native"})
    _order.set_login_request_body(login_info)
    assert _order.login() == 200
    return _order


order_attr = {
    "shipping": "Shipping Method is required.",
    "payment": "Payment Method is required.",
    "subtotal": "Subtotal is incorrect",
    "freight": "Freight is required.",
    "total": "Total is incorrect",
    "recipient": "Recipient is required.",
    "list": "Order List is required.",
}
recipient_attr = {
    "name": "Receiver Name is required.",
    "phone": "Mobile is required.",
    "email": "Email is required.",
    "address": "Address is required.",
    "time": "Deliver Time is required.",
}


@allure.feature("Order APIs")
@allure.story("/order")
@allure.title("[Happy] Valid required info")
def test_order_with_valid_info(order: OrderAPI, order_info: dict):
    with allure.step("Make an order with valid order info"):
        response = order.make_an_order(order_info)
        assert response.status_code == 200

    with allure.step("Assert if order detail in database is the same with payload"):
        order_number = response.json()["data"]["number"]
        order_detail = StylishBackend().get_order_detail_by_number(order_number)
        assert json.loads(order_detail["details"]) == order_info["order"]


@allure.feature("Order APIs")
@allure.story("/order")
@allure.title("[Irregular] No prime")
def test_order_without_prime(order: OrderAPI, order_info: dict):
    with allure.step("Make an order without prime"):
        order_info.pop("prime")
        response = order.make_an_order(order_info)
        assert response.status_code == 400
        error_msg = response.json()["errorMsg"]

    with allure.step(f'Assert if error message is "{error_msg}"'):
        assert error_msg == "Prime value is required."


@allure.feature("Order APIs")
@allure.story("/order")
@allure.title("[Irregular] No logging in")
def test_order_without_login(order_info: dict):
    with allure.step("Make an order with valid order info"):
        order = OrderAPI()
        response = order.make_an_order(order_info)
        assert response.status_code == 401
        error_msg = response.json()["errorMsg"]

    with allure.step(f'Assert if error message is "{error_msg}"'):
        assert error_msg == "Unauthorized"


@allure.feature("Order APIs")
@allure.story("/order")
@allure.title("[Irregular] Broken order attribute")
@pytest.mark.parametrize("attr", [*order_attr])
def test_order_with_broken_order_info(order: OrderAPI, order_info: dict, attr: str):
    with allure.step(f'Make an order without order attr "{attr}"'):
        order_info["order"].pop(attr)
        response = order.make_an_order(order_info)
        assert response.status_code == 400
        error_msg = response.json()["errorMsg"]

    with allure.step(f'Assert if error message is "{error_msg}"'):
        assert error_msg == order_attr[attr]
        # TODO: payload中不存在"list" attribute時會回應Internal Error，需回報修正


@allure.feature("Order APIs")
@allure.story("/order")
@allure.title("[Irregular] Broken recipient attribute")
@pytest.mark.parametrize("attr", [*recipient_attr])
def test_order_with_broken_recipient_info(order: OrderAPI, order_info: dict, attr: str):
    with allure.step(f'Make an order without recipient attr "{attr}"'):
        order_info["order"]["recipient"].pop(attr)
        response = order.make_an_order(order_info)
        assert response.status_code == 400
        error_msg = response.json()["errorMsg"]

    with allure.step(f'Assert if error message is "{error_msg}"'):
        assert error_msg == recipient_attr[attr]


@allure.feature("Order APIs")
@allure.story("/order")
@allure.title("[Irregular] Order attribute is NULL")
@pytest.mark.parametrize("attr", [*order_attr])
def test_order_with_null_order_info(order: OrderAPI, order_info: dict, attr: str):
    with allure.step(f'Make an order with NULL of "{attr}"'):
        order_info["order"][attr] = [] if attr == "list" else None
        response = order.make_an_order(order_info)
        assert response.status_code == 400
        error_msg = response.json()["errorMsg"]

    with allure.step(f'Assert if error message is "{error_msg}"'):
        assert error_msg == error_msg


@allure.feature("Order APIs")
@allure.story("/order")
@allure.title("[Irregular] Recipient attribute is NULL")
@pytest.mark.parametrize("attr", [*recipient_attr])
def test_order_with_null_recipient_info(order: OrderAPI, order_info: dict, attr: str):
    with allure.step(f"Make an order with NULL of '{attr}'"):
        order_info["order"]["recipient"][attr] = None
        response = order.make_an_order(order_info)
        assert response.status_code == 400
        error_msg = response.json()["errorMsg"]

    with allure.step(f'Assert if error message is "{error_msg}"'):
        assert error_msg == recipient_attr[attr]


@allure.feature("Order APIs")
@allure.story("/order/{order_id}")
@allure.title("[Happy] Valid order number")
@pytest.mark.parametrize("order_number", ["71223749413"])
def test_get_order_detai_with_valid_number(order: OrderAPI, order_number: str):
    with allure.step("Get order detail by order number"):
        response = order.get_order_detail_by_number(order_number)
        assert response.status_code == 200

    with allure.step("Assert if response is the same with order detail in database"):
        db_order = StylishBackend().get_order_detail_by_number(order_number)
        db_order["details"] = json.loads(db_order["details"])
        assert response.json()["data"] == db_order


@allure.feature("Order APIs")
@allure.story("/order/{order_id}")
@allure.title("[Irregular] Invalid order number")
@pytest.mark.parametrize("order_number", ["abc", "123"])
def test_get_order_detai_with_invalid_number(order: OrderAPI, order_number: str):
    with allure.step("Get order detail by order number"):
        response = order.get_order_detail_by_number(order_number)
        assert response.status_code == 400
        error_msg = response.json()["errorMsg"]

    with allure.step(f'Assert if error message is "{error_msg}"'):
        assert error_msg == "Order Not Found."
        # TODO: 實測用"abc"會回應Internal Error，需回報修正


@allure.feature("Order APIs")
@allure.story("/order/{order_id}")
@allure.title("[Irregular] No logging in")
@pytest.mark.parametrize("order_number", ["71223749413"])
def test_get_order_detai_without_login(order_number: str):
    with allure.step("Get order detail by order number"):
        order = OrderAPI()
        response = order.get_order_detail_by_number(order_number)
        assert response.status_code == 401
        error_msg = response.json()["errorMsg"]

    with allure.step(f'Assert if error message is "{error_msg}"'):
        assert error_msg == "Unauthorized"
