from random import choice, randint

from selenium.webdriver.common.by import By

from page_objects.base_page import BasePage


class ProductPage(BasePage):
    SELECTED_COLOR_LOCATOR = (By.CLASS_NAME, "product__color--selected")
    SELECTED_SIZE_LOCATOR = (By.CLASS_NAME, "product__size--selected")
    ADD_TO_CART_LOCATOR = (By.CLASS_NAME, "product__add-to-cart-button")
    ADD_QUANTITY_LOCATOR = (By.CLASS_NAME, "product__quantity-add")
    MINUS_QUANTITY_LOCATOR = (By.CLASS_NAME, "product__quantity-minus")
    CURRENT_QUANTITY_LOCATOR = (By.CLASS_NAME, "product__quantity-value")
    COLORS_LOCATOR = (By.CLASS_NAME, "product__color")
    SIZES_LOCATOR = (By.CLASS_NAME, "product__size")
    PRICE_LOCATOR = (By.CLASS_NAME, "product__price")
    TITLE_LOCATOR = (By.CLASS_NAME, "product__title")

    def __init__(self, driver, product_id=None):
        super().__init__(driver)
        self.use_js = True
        if product_id is not None:
            self.open_product_page(product_id)

    def open_product_page(self, product_id):
        self.driver.get(f"http://54.201.140.239/product.html?id={product_id}")

    def select_color_by_color_code(self, color_code: str):
        color_locator = (By.CSS_SELECTOR, f"div[data_id='color_code_{color_code}']")
        self.find_and_click_element(color_locator, is_using_js=self.use_js)

    def is_selected_color_highlighted(self, color_code: str) -> bool:
        color_locator = (By.CSS_SELECTOR, f"div[data_id='color_code_{color_code}']")
        return "product__color--selected" in self.find_clickable_element(color_locator).get_attribute("class")

    def select_size_by_size_name(self, size: str):
        size_locator = (By.XPATH, f"//div[@class='product__size' and text()='{size}']")
        self.find_and_click_element(size_locator, is_using_js=self.use_js)

    def increase_quantity(self, quantiy: int):
        if not self.is_add_to_cart_available():
            raise Exception("A size havsn't been selected")
        btn_add_quantity = self.find_clickable_element(self.ADD_QUANTITY_LOCATOR)
        for i in range(quantiy):
            self.click_element(btn_add_quantity, is_using_js=self.use_js)

    def decrease_quantity(self, quantiy: int):
        if not self.is_add_to_cart_available():
            raise Exception("A size havsn't been selected")
        btn_minus_quantity = self.find_clickable_element(self.MINUS_QUANTITY_LOCATOR)
        for i in range(quantiy):
            self.click_element(btn_minus_quantity, is_using_js=self.use_js)

    def get_product_name(self) -> str:
        return self.find_presented_element(self.TITLE_LOCATOR).text

    def get_product_price(self) -> int:
        return int(self.find_presented_element(self.PRICE_LOCATOR).text.split(".")[-1])

    def get_selected_color_code(self) -> str:
        return self.find_clickable_element(self.SELECTED_COLOR_LOCATOR).get_attribute("data_id").split("_")[-1]

    def get_selected_size_name(self) -> str:
        return self.find_clickable_element(self.SELECTED_SIZE_LOCATOR).text

    def get_current_quantity(self) -> int:
        return int(self.find_presented_element(self.CURRENT_QUANTITY_LOCATOR).text)

    def is_add_to_cart_available(self) -> bool:
        return self.find_clickable_element(self.ADD_TO_CART_LOCATOR).text == "加入購物車"

    def add_product_to_cart(self, is_forced=False):
        if self.is_add_to_cart_available() or is_forced:
            self.find_and_click_element(self.ADD_TO_CART_LOCATOR, is_using_js=self.use_js)
        else:
            raise Exception("A size havsn't been selected")

    def select_random_color(self):
        color_btn = choice(self.find_presented_elements(self.COLORS_LOCATOR))
        self.click_element(color_btn, is_using_js=True)
        return self.get_selected_color_code()

    def select_random_size(self):
        size_btn = choice(self.find_presented_elements(self.SIZES_LOCATOR))
        self.click_element(size_btn, is_using_js=True)
        return self.get_selected_size_name()

    def select_random_quantity(self):
        random_quantity = randint(1, 9) - self.get_current_quantity()
        if random_quantity > 0:
            self.increase_quantity(random_quantity)
        elif random_quantity < 0:
            self.decrease_quantity(abs(random_quantity))
        return self.get_current_quantity()
