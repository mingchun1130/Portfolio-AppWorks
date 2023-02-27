import logging
from random import choice

import allure
import pytest

from page_objects.product_page import ProductPage

TESTCASE_BASE_LINK = "https://github.com/AppWorks-School-Materials/Automation-Test-Program-Batch1/blob/main/"
TESTCASE_CATEGORY = "week_5/part-2/Project1_UIAutomation.md#scenario-"


@pytest.fixture
def random_product_id(product_detail):
    return choice(product_detail["id"].unique())


@pytest.fixture
def product_sizes(product_detail, random_product_id):
    return product_detail.query("id==@random_product_id")["size"].unique()


@pytest.fixture
def product_colors(product_detail, random_product_id):
    _product_colors = product_detail.query("id==@random_product_id")[["color_name", "color_code"]]
    return _product_colors.set_index("color_name").to_dict()["color_code"]


@pytest.fixture
def product(driver, random_product_id):
    logging.info(random_product_id)
    return ProductPage(driver, random_product_id)


@allure.feature("Product Detail")
@allure.story("Modify purchase details")
@allure.title("Modify color")
@allure.testcase(TESTCASE_BASE_LINK + TESTCASE_CATEGORY + "color-selection", "Color Selection")
def test_color_selection(product, product_colors: dict):
    """
    確認進行選擇顏色的操作後，被選擇的顏色是否有正確被highlight。
    """
    with allure.step("Open product detail page"):
        logging.info(f"Test color is {product_colors.keys()}")

    for color in product_colors.keys():
        with allure.step("Select given color"):
            product.select_color_by_color_code(product_colors[color])

        with allure.step("Check highlighted color is the same with given color"):
            # Reverse the "color_code" dictionay(name:code pair) then find color name by color code.
            color_highlighted = {v: k for k, v in product_colors.items()}[product.get_selected_color_code()]
            logging.info(f"Highlighted color is {color_highlighted}")
            allure.attach(f"Highlighted color is {color_highlighted}", attachment_type=allure.attachment_type.TEXT)
            assert color == color_highlighted, f"Input '{color}' hasn't been highlighted, {color_highlighted} instead."


@allure.feature("Product Detail")
@allure.story("Modify purchase details")
@allure.title("Modify size")
@allure.testcase(TESTCASE_BASE_LINK + TESTCASE_CATEGORY + "size-selection", "Size Selection")
def test_size_selection(product, product_sizes):
    """
    確認進行選擇尺寸的操作後，被選擇的尺寸是否有正確被highlight。
    """
    with allure.step("Open product detail page"):
        logging.info(f"Test size is {product_sizes}")

    for size in product_sizes:
        with allure.step("Select given size"):
            product.select_size_by_size_name(size)

        with allure.step("Check highlighted size is the same with given size"):
            size_highlighted = product.get_selected_size_name()
            logging.info(f"Highlighted size is {size_highlighted}")
            allure.attach(f"Highlighted size is {size_highlighted}", attachment_type=allure.attachment_type.TEXT)
            assert size == size_highlighted, f"Input '{size}' hasn't been highlighted, {size_highlighted} instead."


@allure.feature("Product Detail")
@allure.story("Modify purchase details")
@allure.title("Increase Quantity")
@allure.testcase(TESTCASE_BASE_LINK + TESTCASE_CATEGORY + "quantity-editor---increase-quantity", "Increse Quantity")
@pytest.mark.parametrize("quantity", [8])
def test_increase_quantity(product, product_sizes, quantity):
    """
    確認進行增加數量的操作時，數量是否有正確增加，並確認最大上限為9。
    """
    with allure.step("Select size"):
        product.select_size_by_size_name(choice(product_sizes))

    with allure.step("Increase by given quantity"):
        origin_quantity = product.get_current_quantity()
        product.increase_quantity(quantity)

    with allure.step("Check if current quantity is correct"):
        assert product.get_current_quantity() == origin_quantity + quantity

    with allure.step("Add 2 more quantity while quantity has reached max"):
        product.increase_quantity(2)
        assert product.get_current_quantity() == origin_quantity + quantity


@allure.feature("Product Detail")
@allure.story("Modify purchase details")
@allure.title("Decrease Quantity")
@allure.testcase(TESTCASE_BASE_LINK + TESTCASE_CATEGORY + "quantity-editor---decrease-quantity", "Decrease Quantity")
@pytest.mark.parametrize("quantity", [8])
def test_decrease_quantity(product, product_sizes, quantity):
    """
    確認進行減少數量的操作時，數量是否有正確減少。
    """
    with allure.step("Select size"):
        product.select_size_by_size_name(choice(product_sizes))

    with allure.step("Increase by given quantity"):
        origin_quantity = product.get_current_quantity()
        product.increase_quantity(quantity)

    with allure.step("decrease by given quantity"):
        product.decrease_quantity(quantity)

    with allure.step("Check if current quantity is correct"):
        assert product.get_current_quantity() == origin_quantity


@allure.feature("Product Detail")
@allure.story("Add to cart")
@allure.title("Add to cart successfully")
@allure.testcase(TESTCASE_BASE_LINK + TESTCASE_CATEGORY + "add-to-cart---success", "Add To Cart - Success")
def test_add_to_cart_success(product, product_sizes):
    """
    確認點擊加入購物車按鈕後，商品有被加入購物車。
    """
    with allure.step("Select size"):
        product.select_size_by_size_name(choice(product_sizes))

    with allure.step("Click add-to-cart button"):
        product.add_product_to_cart()

    with allure.step("Check if success message shows"):
        alert = product.wait_alert_prompt()
        logging.info(f"Alert message is {alert.text}")
        assert alert.text == "已加入購物車"
        alert.accept()

    with allure.step("Check if cart number increase by 1"):
        assert product.get_cart_number() == 1


@allure.feature("Product Detail")
@allure.story("Add to cart")
@allure.title("Add to cart failed")
@allure.testcase(TESTCASE_BASE_LINK + TESTCASE_CATEGORY + "add-to-cart---failed", "Add To Cart - Failed")
def test_add_to_cart_fail(product):
    """
    確認未選擇尺寸的狀態下點擊加入購物車按鈕後，會跳出警告視窗。
    """
    with allure.step("Click add-to-cart button"):
        product.add_product_to_cart(is_forced=True)

    with allure.step("Check if fail message shows"):
        alert = product.wait_alert_prompt()
        logging.info(f"Alert message is {alert.text}")
        assert alert.text == "請選擇尺寸"
        alert.accept()
