import json
import logging
from random import sample

import allure
import pytest

from page_objects.cart_page import CartPage
from page_objects.login_page import LoginPage
from page_objects.product_page import ProductPage
from test_data.get_data_from_excel import GetData

TESTCASE_BASE_LINK = "https://github.com/AppWorks-School-Materials/Automation-Test-Program-Batch1/blob/main/"
TESTCASE_CATEGORY = "week_6/part-2/Project1_UIAutomation.md#scenario-"


@pytest.fixture
def random_product_ids(product_detail, amount=2):
    allure.attach(
        json.dumps(
            product_detail[["id", "title"]].drop_duplicates(subset="id").to_dict("records"),
            indent=2,
            ensure_ascii=False,
        ),
        "all_product_id_name",
        attachment_type=allure.attachment_type.TEXT,
    )
    return sample(product_detail["id"].unique().tolist(), amount)


test_data = GetData()
invalid_checkout_values = test_data.get_invalid_checkout_data()
valid_checkout_values = test_data.get_valid_checkout_data()


@allure.feature("Checkout")
@allure.story("Checkout")
@allure.title("Checkout with empty cart")
@allure.testcase(TESTCASE_BASE_LINK + TESTCASE_CATEGORY + "checkout-with-empty-cart", "Shopping Cart Info Correct")
def test_checkout_with_empty_cart(driver, user):
    """
    檢查空購物車進行結帳時，會顯示預期的警告訊息。
    """
    with allure.step("Login success"):
        login = LoginPage(driver, "http://54.201.140.239/login.html")
        login.enter_email_and_password(user["email"], user["password"])
        login.login()
        alert = login.wait_alert_prompt()
        alert.accept()

    with allure.step("Enter shopping cart and checkout without products"):
        login.enter_shopping_cart()
        cart = CartPage(driver)
        cart.checkout()

    with allure.step("Check if notice message shows"):
        alert = cart.wait_alert_prompt()
        logging.info(f"Alert message is {alert.text}")
        assert alert.text == "尚未選購商品"
        alert.accept()


@allure.feature("Checkout")
@allure.story("Checkout")
@allure.title("Checkout with invalid values")
@allure.testcase(
    TESTCASE_BASE_LINK + TESTCASE_CATEGORY + "checkout-with-invalid-values-17-test-cases",
    "Checkout with invalid values",
)
@pytest.mark.parametrize("checkout_info", invalid_checkout_values)
def test_checkout_with_invalid_values(driver, random_product_ids, all_color_code, user, checkout_info):
    """
    檢查輸入各種無效的訂單資訊時，會顯示預期的警告訊息。
    """
    with allure.step("Login success"):
        login = LoginPage(driver, "http://54.201.140.239/login.html")
        login.enter_email_and_password(user["email"], user["password"])
        login.login()
        alert = login.wait_alert_prompt()
        alert.accept()

    with allure.step("Add products to shopping cart"):
        product = ProductPage(driver)
        shop_list = []
        for id in random_product_ids:
            product.open_product_page(id)
            shop_list.append(
                {
                    "id": str(id),
                    "name": product.get_product_name(),
                    "color": {v: k for k, v in all_color_code.items()}[product.select_random_color()],
                    "size": product.select_random_size(),
                    "quantity": product.select_random_quantity(),
                    "price": product.get_product_price(),
                    "subtotal": product.get_current_quantity() * product.get_product_price(),
                }
            )
            product.add_product_to_cart()
            alert = product.wait_alert_prompt()
            alert.accept()
            logging.info(shop_list[-1])
        allure.attach(
            json.dumps(shop_list, indent=2, ensure_ascii=False),
            "cart_item_list",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Enter shopping cart"):
        cart = CartPage(driver)
        cart.enter_shopping_cart()

    with allure.step("Check if product info is displayed correctly in cart"):
        cart_item_list = []
        for item in cart.get_cart_items():
            cart_item_list.append(cart.get_item_info(item))
        allure.attach(
            json.dumps(cart_item_list, indent=2, ensure_ascii=False),
            "cart_item_list",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert cart_item_list == shop_list

    with allure.step("Fill in with invalid values"):
        cart.fill_in_order_info(checkout_info)
        cart.fill_in_payment_info(checkout_info)
        allure.attach(
            json.dumps(checkout_info, indent=2, ensure_ascii=False),
            "checkout_info",
            attachment_type=allure.attachment_type.TEXT,
        )
        cart.checkout()

    with allure.step("Check if notice message shows"):
        alert = cart.wait_alert_prompt()
        logging.info(f"Alert message is {alert.text}")
        assert alert.text == checkout_info["Alert Msg"]
        alert.accept()


@allure.feature("Checkout")
@allure.story("Checkout")
@allure.title("Checkout with valid values")
@allure.testcase(
    TESTCASE_BASE_LINK + TESTCASE_CATEGORY + "checkout-with-valid-values-3-test-cases",
    "Checkout with valid values",
)
@pytest.mark.parametrize("checkout_info", valid_checkout_values)
def test_checkout_with_valid_values(driver, random_product_ids, all_color_code, user, checkout_info):
    """
    檢查輸入有效的訂單資訊時，可成功結帳且結帳商品的資訊正確。
    """
    with allure.step("Login success"):
        login = LoginPage(driver, "http://54.201.140.239/login.html")
        login.enter_email_and_password(user["email"], user["password"])
        login.login()
        alert = login.wait_alert_prompt()
        alert.accept()

    with allure.step("Add products to shopping cart"):
        product = ProductPage(driver)
        shop_list = []
        for id in random_product_ids:
            product.open_product_page(id)
            shop_list.append(
                {
                    "id": str(id),
                    "name": product.get_product_name(),
                    "color": {v: k for k, v in all_color_code.items()}[product.select_random_color()],
                    "size": product.select_random_size(),
                    "quantity": product.select_random_quantity(),
                    "price": product.get_product_price(),
                    "subtotal": product.get_current_quantity() * product.get_product_price(),
                }
            )
            product.add_product_to_cart()
            alert = product.wait_alert_prompt()
            alert.accept()
            logging.info(shop_list[-1])
        allure.attach(
            json.dumps(shop_list, indent=2, ensure_ascii=False),
            "cart_item_list",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Enter shopping cart"):
        cart = CartPage(driver)
        cart.enter_shopping_cart()

    with allure.step("Check if product info is displayed correctly in cart"):
        cart_item_list = []
        for item in cart.get_cart_items():
            cart_item_list.append(cart.get_item_info(item))
        allure.attach(
            json.dumps(cart_item_list, indent=2, ensure_ascii=False),
            "cart_item_list",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert cart_item_list == shop_list

    with allure.step("Fill in with valid values"):
        cart.fill_in_order_info(checkout_info)
        cart.fill_in_payment_info(checkout_info)
        allure.attach(
            json.dumps(checkout_info, indent=2, ensure_ascii=False),
            "checkout_info",
            attachment_type=allure.attachment_type.TEXT,
        )
        cart.checkout()

    with allure.step("Check if notice message shows"):
        alert = cart.wait_alert_prompt()
        logging.info(f"Alert message is {alert.text}")
        assert alert.text == "付款成功"
        alert.accept()

    with allure.step("Check if product info is displayed correctly in thank you page"):
        cart.wait_for_thankyou_page()
        checkout_item_list = []
        for item in cart.get_cart_items():
            checkout_item_list.append(cart.get_item_info(item))
        allure.attach(
            json.dumps(checkout_item_list, indent=2, ensure_ascii=False),
            "checkout_item_list",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert checkout_item_list == cart_item_list
