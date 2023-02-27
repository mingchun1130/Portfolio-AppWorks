import json
import logging
from random import choice, randint, sample

import allure
import pytest

from page_objects.cart_page import CartPage
from page_objects.product_page import ProductPage

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


@allure.feature("Shopping Cart")
@allure.story("Shopping Cart")
@allure.title("Shopping Cart Info Correct")
@allure.testcase(TESTCASE_BASE_LINK + TESTCASE_CATEGORY + "shopping-cart-info-correct", "Shopping Cart Info Correct")
def test_shopping_cart_info(driver, random_product_ids, all_color_code):
    """
    檢查商品加入購物車後，其在購物車內顯示的資訊與選擇的相同。
    """
    product = ProductPage(driver)
    shop_list = []

    with allure.step("Add products to shopping cart"):
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
            "shop_list",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Enter shopping cart"):
        product.enter_shopping_cart()
        cart = CartPage(driver)

    with allure.step("Check if product info is displayed correctly"):
        cart_item_list = []
        for item in cart.get_cart_items():
            cart_item_list.append(cart.get_item_info(item))
        assert cart_item_list == shop_list


@allure.feature("Shopping Cart")
@allure.story("Shopping Cart")
@allure.title("Remove product from cart")
@allure.testcase(TESTCASE_BASE_LINK + TESTCASE_CATEGORY + "remove-product-from-cart", "Remove product from cart")
def test_remove_item_from_cart(driver, random_product_ids, all_color_code):
    """
    檢查商品能否從購物車中正確移除。
    """
    product = ProductPage(driver)
    shop_list = []

    with allure.step("Add products to shopping cart"):
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
            "shop_list",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Enter shopping cart"):
        product.enter_shopping_cart()
        cart = CartPage(driver)

    with allure.step("Delete product from shopping cart"):
        cart_items = cart.get_cart_items()
        delete_item = choice(cart_items)
        cart.delete_item(delete_item)
        cart_items.remove(delete_item)

    with allure.step("Check if delete message shows"):
        alert = cart.wait_alert_prompt()
        logging.info(f"Alert message is {alert.text}")
        assert alert.text == "已刪除商品"
        alert.accept()
        cart.wait_element_disappear(elem=delete_item)

    with allure.step("Check if new cart info is updated correctly"):
        new_cart_items = cart.get_cart_items()
        assert new_cart_items == cart_items

    with allure.step("Check if cart icon number is updated correctly"):
        assert cart.get_cart_number() == len(new_cart_items)


@allure.feature("Shopping Cart")
@allure.story("Shopping Cart")
@allure.title("Edit quantity in cart")
@allure.testcase(TESTCASE_BASE_LINK + TESTCASE_CATEGORY + "edit-quantity-in-cart", "Edit quantity in cart")
def test_edit_quantity_in_cart(driver, random_product_ids, all_color_code):
    """
    檢查加入購物車的商品能否正確變更數量。
    """
    product = ProductPage(driver)
    shop_list = []

    with allure.step("Add products to shopping cart"):
        for id in random_product_ids:
            product.open_product_page(id)
            shop_list.append(
                {
                    "id": str(id),
                    "name": product.get_product_name(),
                    "color": {v: k for k, v in all_color_code.items()}[product.select_random_color()],
                    "size": product.select_random_size(),
                    "quantity": product.get_current_quantity(),
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
            "shop_list",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Enter shopping cart"):
        product.enter_shopping_cart()
        cart = CartPage(driver)

    with allure.step("Edit the quantity of the product"):
        cart_item = choice(cart.get_cart_items())
        unit_price = cart.get_item_price(cart_item)
        logging.info(f"Unit price is {unit_price}")
        new_quantity = randint(2, 9)
        logging.info(f"Modify to quantity {new_quantity}")
        cart.modify_item_quantity(cart_item, new_quantity)

    with allure.step("Check if modified message shows"):
        alert = cart.wait_alert_prompt()
        logging.info(f"Alert message is {alert.text}")
        assert alert.text == "已修改數量"
        alert.accept()

    with allure.step("Check if subtotal is updated correctly"):
        assert cart.get_item_quantity(cart_item) == new_quantity
        assert cart.get_item_subtotal(cart_item) == unit_price * new_quantity
