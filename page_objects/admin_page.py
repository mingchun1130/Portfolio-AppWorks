from typing import Literal

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from page_objects.base_page import BasePage


class AdminPage(BasePage):
    CREATE_PRODUCT_BTN_LOCATOR = (By.XPATH, "//button[text()='Create New Product']")
    PRODUCTS_LOCATOR = (By.XPATH, "//tbody[@id='product_list']/child::tr")
    CATEGORY_SELECTOR = (By.NAME, "category")
    TITLE_LOCATOR = (By.CSS_SELECTOR, "input[name='title']")
    DESCRIPTION_LOCATOR = (By.CSS_SELECTOR, "textarea[name='description']")
    PRICE_LOCATOR = (By.CSS_SELECTOR, "input[name='price']")
    TEXTURE_LOCATOR = (By.CSS_SELECTOR, "input[name='texture']")
    WASH_LOCATOR = (By.CSS_SELECTOR, "input[name='wash']")
    PLACE_LOCATOR = (By.CSS_SELECTOR, "input[name='place']")
    NOTE_LOCATOR = (By.CSS_SELECTOR, "input[name='note']")
    STORY_LOCATOR = (By.CSS_SELECTOR, "input[name='story']")
    MAIN_IMAGE_LOCATOR = (By.CSS_SELECTOR, "input[name='main_image']")
    OTHER_IMAGES_LOCATOR = (By.CSS_SELECTOR, "input[name='other_images']")
    CREATE_BTN_LOCATOR = (By.CSS_SELECTOR, "input[value='Create']")
    DELETE_BTN_LOCATOR = (By.XPATH, "//button[text()='刪除']")

    def __init__(self, driver, admin_url=None) -> None:
        super().__init__(driver)
        if admin_url is not None:
            self.driver.get(admin_url)

    def open_create_product_page(self) -> None:
        self.find_and_click_element(self.CREATE_PRODUCT_BTN_LOCATOR, is_using_js=True)
        self.driver.switch_to.window(self.driver.window_handles[1])

    def get_all_product_elements(self) -> list:
        return self.find_presented_elements((By.XPATH, "//tbody[@id='product_list']/child::tr"))

    def select_category(self, category: Literal["Women", "Men", "Accessories"]) -> None:
        select = Select(self.find_presented_element(self.CATEGORY_SELECTOR))
        select.select_by_visible_text(category)

    def fill_in_product_info(self, info: dict) -> None:
        self.find_clickable_element(self.TITLE_LOCATOR).send_keys(info["Title"])
        self.find_clickable_element(self.DESCRIPTION_LOCATOR).send_keys(info["Description"])
        self.find_clickable_element(self.PRICE_LOCATOR).send_keys(info["Price"])
        self.find_clickable_element(self.TEXTURE_LOCATOR).send_keys(info["Texture"])
        self.find_clickable_element(self.WASH_LOCATOR).send_keys(info["Wash"])
        self.find_clickable_element(self.PLACE_LOCATOR).send_keys(info["Place of Product"])
        self.find_clickable_element(self.NOTE_LOCATOR).send_keys(info["Note"])
        self.find_clickable_element(self.STORY_LOCATOR).send_keys(info["Story"])

    def select_checkbox(self, text: str) -> None:
        self.find_and_click_element(
            (By.XPATH, f"//label[contains(text(),'{text}')]/preceding-sibling::input"), is_using_js=True
        )

    def select_color(self, info: dict, all_color_code: dict) -> None:
        colors = info["Colors"]
        if colors == "全選":
            colors = all_color_code.keys()
        elif colors == "":
            return
        else:
            colors = colors.split(", ")
        for color in colors:
            self.select_checkbox(color)

    def select_size(self, info: dict) -> None:
        sizes = info["Sizes"]
        if sizes == "全選":
            sizes = ["S", "M", "L", "XL", "F"]
        elif sizes == "":
            return
        else:
            sizes = sizes.split(", ")
        for size in sizes:
            self.select_checkbox(size)

    def set_main_image_to_upload(self, file_path) -> None:
        if file_path is not None:
            self.find_presented_element(self.MAIN_IMAGE_LOCATOR).send_keys(file_path)

    def set_other_images_to_upload(self, index: Literal[0, 1], file_path) -> None:
        if file_path is not None:
            self.find_presented_elements(self.OTHER_IMAGES_LOCATOR)[index].send_keys(file_path)

    def click_create_button(self) -> None:
        self.find_and_click_element(self.CREATE_BTN_LOCATOR, is_using_js=True)

    def delete_product_by_name(self, product_name: str):
        delete_btn_locator = (
            By.XPATH,
            f"//td[@id='product_title' and text()='{product_name}']/following-sibling::td/button",
        )
        try:
            self.find_and_click_element(delete_btn_locator, is_using_js=True)
        except TimeoutException:
            pass
        else:
            self.wait_alert_prompt().accept()
            self.wait_element_disappear(locator=delete_btn_locator)

    def is_product_displayed(self, product_name: str) -> bool:
        try:
            self.find_presented_element((By.XPATH, f"//td[@id='product_title' and text()='{product_name}']"))
        except TimeoutException:
            return False
        else:
            return True

    def delete_all_test_data(self) -> None:
        try:
            delete_btns = self.find_presented_elements(self.DELETE_BTN_LOCATOR)
        except TimeoutException:
            pass
        else:
            for btn in delete_btns:
                self.click_element(btn, is_using_js=True)
                self.wait_element_disappear(elem=btn)
                self.wait_alert_prompt().accept()
