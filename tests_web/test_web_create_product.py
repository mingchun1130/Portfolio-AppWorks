import json
import logging

import allure
import pytest

from page_objects.admin_page import AdminPage
from page_objects.login_page import LoginPage
from test_data.get_data_from_excel import GetData

TESTCASE_BASE_LINK = "https://github.com/AppWorks-School-Materials/Automation-Test-Program-Batch1/blob/main/"
TESTCASE_CATEGORY = "week_7/part-1/Project1_UIAutomation.md#scenario-"


test_data = GetData()
invalid_product_create_info = test_data.get_invalid_product_create_info()
valid_product_create_info = test_data.get_valid_product_create_info()


@pytest.fixture
def admin_init(driver, user, request):
    login = LoginPage(driver, "http://54.201.140.239/login.html")
    login.enter_email_and_password(user["email"], user["password"])
    login.login()
    alert = login.wait_alert_prompt()
    alert.accept()
    _admin = AdminPage(driver, "http://54.201.140.239/admin/products.html")
    yield _admin, request.param
    _admin.switch_back_to_main_window()
    _admin.driver.refresh()
    _admin.delete_product_by_name(request.param["Title"])


@pytest.fixture
def no_login(driver, request):
    login = LoginPage(driver)
    _admin = AdminPage(driver, "http://54.201.140.239/admin/products.html")
    alert = _admin.wait_alert_prompt()
    logging.info(f"Alert message is {alert.text}")
    assert alert.text == "Unauthorized"
    alert.accept()
    yield _admin, request.param, login


@allure.feature("Create Product")
@allure.story("Create Product")
@allure.title("Create Product Success")
@allure.testcase(
    TESTCASE_BASE_LINK + TESTCASE_CATEGORY + "create-product-success-3-test-cases", "Create Product Success"
)
@pytest.mark.parametrize("admin_init", valid_product_create_info, indirect=True)
def test_create_product_success(admin_init, all_color_code):
    """
    確認使用有效的資料建立新商品時，可成功建立商品。
    """
    admin, product_info = admin_init

    with allure.step("Transfer to create product page"):
        admin.open_create_product_page()

    with allure.step("Fill in product info with valid values"):
        allure.attach(
            json.dumps(product_info, indent=2, ensure_ascii=False),
            "product_info",
            attachment_type=allure.attachment_type.TEXT,
        )
        admin.select_category(product_info["Category"])
        admin.fill_in_product_info(product_info)
        admin.select_color(product_info, all_color_code)
        admin.select_size(product_info)

    with allure.step("Set product images"):
        admin.set_main_image_to_upload(test_data.get_file_full_path(product_info["Main Image"]))
        admin.set_other_images_to_upload(0, test_data.get_file_full_path(product_info["Other Image 1"]))
        admin.set_other_images_to_upload(1, test_data.get_file_full_path(product_info["Other Image 2"]))

    with allure.step("Create product and check if success message shows"):
        admin.click_create_button()
        alert = admin.wait_alert_prompt(timeout=10)
        logging.info(f"Alert message is {alert.text}")
        assert alert.text == "Create Product Success"
        alert.accept()
        admin.switch_back_to_main_window()

    with allure.step("Check if new product is displayed on product list"):
        admin.driver.refresh()
        assert admin.is_product_displayed(product_info["Title"])


@allure.feature("Create Product")
@allure.story("Create Product")
@allure.title("Create Product with Invalid Value")
@allure.testcase(
    TESTCASE_BASE_LINK + TESTCASE_CATEGORY + "create-product-with-invalid-value-20-test-cases",
    "Create Product with Invalid Value",
)
@pytest.mark.parametrize("admin_init", invalid_product_create_info, indirect=True)
def test_create_product_fail(admin_init, all_color_code):
    """
    確認使用無效的資料建立新商品時，不可成功建立商品並顯示預期的訊息。
    """
    admin, product_info = admin_init

    with allure.step("Transfer to create product page"):
        admin.open_create_product_page()

    with allure.step("Fill in product info with invalid values"):
        allure.attach(
            json.dumps(product_info, indent=2, ensure_ascii=False),
            "product_info",
            attachment_type=allure.attachment_type.TEXT,
        )
        admin.select_category(product_info["Category"])
        admin.fill_in_product_info(product_info)
        admin.select_color(product_info, all_color_code)
        admin.select_size(product_info)

    with allure.step("Set product images"):
        admin.set_main_image_to_upload(test_data.get_file_full_path(product_info["Main Image"]))
        admin.set_other_images_to_upload(0, test_data.get_file_full_path(product_info["Other Image 1"]))
        admin.set_other_images_to_upload(1, test_data.get_file_full_path(product_info["Other Image 2"]))

    with allure.step("Create product and check if error message shows"):
        admin.click_create_button()
        alert = admin.wait_alert_prompt(timeout=10)
        logging.info(f"Alert message is {alert.text}")
        assert alert.text == product_info["Alert Msg"]
        alert.accept()
        admin.switch_back_to_main_window()

    with allure.step("Check if new product is not displayed on product list"):
        admin.driver.refresh()
        assert not admin.is_product_displayed(product_info["Title"])


@allure.feature("Create Product")
@allure.story("Create Product")
@allure.title("Create Product without login")
@allure.testcase(
    TESTCASE_BASE_LINK + TESTCASE_CATEGORY + "create-product-without-login",
    "Create Product without login",
)
@pytest.mark.parametrize("no_login", valid_product_create_info, indirect=True)
def test_create_product_without_login(no_login, all_color_code):
    """
    確認在未登入的狀態下進行建立商品的操作時，不能建立商品且會被重新導到登入畫面。
    """
    admin, product_info, login = no_login

    with allure.step("Transfer to create product page"):
        admin.open_create_product_page()

    with allure.step("Fill in product info with valid values"):
        allure.attach(
            json.dumps(product_info, indent=2, ensure_ascii=False),
            "product_info",
            attachment_type=allure.attachment_type.TEXT,
        )
        admin.select_category(product_info["Category"])
        admin.fill_in_product_info(product_info)
        admin.select_color(product_info, all_color_code)
        admin.select_size(product_info)

    with allure.step("Set product images"):
        admin.set_main_image_to_upload(test_data.get_file_full_path(product_info["Main Image"]))
        admin.set_other_images_to_upload(0, test_data.get_file_full_path(product_info["Other Image 1"]))
        admin.set_other_images_to_upload(1, test_data.get_file_full_path(product_info["Other Image 2"]))

    with allure.step("Create product and check if error message shows"):
        admin.click_create_button()
        alert = admin.wait_alert_prompt(timeout=10)
        logging.info(f"Alert message is {alert.text}")
        assert alert.text == "Please Login First"
        alert.accept()

    with allure.step("Check if is redirected to login page"):
        assert login.is_redirected_to_login_page()
