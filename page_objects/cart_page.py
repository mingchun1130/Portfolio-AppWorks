from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from page_objects.base_page import BasePage


class CartPage(BasePage):
    CART_ITEMS_LOCATOR = (By.CSS_SELECTOR, "div.cart__item")
    RECEIVER_NAME_LOCATOR = (By.XPATH, "//div[text()='收件人姓名']/following-sibling::input")
    EMAIL_LOCATOR = (By.XPATH, "//div[text()='Email']/following-sibling::input")
    MOBILE_LOCATOR = (By.XPATH, "//div[text()='手機']/following-sibling::input")
    ADDRESS_LOCATOR = (By.XPATH, "//div[text()='地址']/following-sibling::input")
    DELIVER_TIME_LOCATOR = {
        "Morning": (By.XPATH, "//label[text()='08:00-12:00']/child::input"),
        "Afternoon": (By.XPATH, "//label[text()='14:00-18:00']/child::input"),
        "Anytime": (By.XPATH, "//label[text()='不指定']/child::input"),
    }
    CARD_NUMBER_IFRAME_LOCATOR = (By.XPATH, "//div[@id='card-number']/iframe")
    CARD_NUMBER_LOCATOR = (By.ID, "cc-number")
    EXPIRE_DATE_IFRAME_LOCATOR = (By.XPATH, "//div[@id='card-expiration-date']/iframe")
    EXPIRE_DATE_LOCATOR = (By.ID, "cc-exp")
    SECURITY_CODE_IFRAME_LOCATOR = (By.XPATH, "//div[@id='card-ccv']/iframe")
    SECURITY_CODE_LOCATOR = (By.ID, "cc-ccv")
    CHECKOUT_BTN_LOCATOR = (By.CSS_SELECTOR, "button.checkout-button")

    def __init__(self, driver, cart_url=None):
        super().__init__(driver)
        if cart_url is not None:
            self.driver.get(cart_url)

    def get_cart_items(self) -> list:
        return self.find_presented_elements(self.CART_ITEMS_LOCATOR)

    def get_item_info(self, elem) -> dict:
        return {
            "id": self.get_item_id(elem),
            "name": self.get_item_name(elem),
            "color": self.get_item_color(elem),
            "size": self.get_item_size(elem),
            "quantity": self.get_item_quantity(elem),
            "price": self.get_item_price(elem),
            "subtotal": self.get_item_subtotal(elem),
        }

    def modify_item_quantity(self, elem, quantity: int):
        select = Select(elem.find_element(By.CSS_SELECTOR, "select.cart__item-quantity-selector"))
        select.select_by_visible_text(f"{quantity}")

    def get_item_id(self, elem) -> str:
        return elem.find_element(By.CLASS_NAME, "cart__item-id").text

    def get_item_name(self, elem) -> str:
        return elem.find_element(By.CLASS_NAME, "cart__item-name").text

    def get_item_color(self, elem) -> str:
        return elem.find_element(By.CLASS_NAME, "cart__item-color").text.split("｜")[-1]

    def get_item_size(self, elem) -> str:
        return elem.find_element(By.CLASS_NAME, "cart__item-size").text.split("｜")[-1]

    def get_item_quantity(self, elem) -> int:
        try:
            select = Select(elem.find_element(By.CSS_SELECTOR, "select.cart__item-quantity-selector"))
            return int(select.first_selected_option.text)
        except NoSuchElementException:
            return int(elem.find_element(By.XPATH, ".//div[@class='cart__item-quantity']/div[last()]").text)

    def get_item_price(self, elem) -> int:
        return int(elem.find_element(By.CLASS_NAME, "cart__item-price-content").text.split(".")[-1])

    def get_item_subtotal(self, elem) -> int:
        return int(elem.find_element(By.CLASS_NAME, "cart__item-subtotal-content").text.split(".")[-1])

    def delete_item(self, elem):
        elem.find_element(By.CLASS_NAME, "cart__delete-button").click()

    def checkout(self):
        self.find_and_click_element(self.CHECKOUT_BTN_LOCATOR, is_using_js=True)

    def fill_in_order_info(self, info: dict):
        self.find_clickable_element(self.RECEIVER_NAME_LOCATOR).send_keys(info["Receiver"])
        self.find_clickable_element(self.EMAIL_LOCATOR).send_keys(info["Email"])
        self.find_clickable_element(self.MOBILE_LOCATOR).send_keys(info["Mobile"])
        self.find_clickable_element(self.ADDRESS_LOCATOR).send_keys(info["Address"])
        if self.DELIVER_TIME_LOCATOR.get(info["Deliver Time"], None) is not None:
            self.find_and_click_element(self.DELIVER_TIME_LOCATOR[info["Deliver Time"]], is_using_js=True)

    def fill_in_payment_info(self, info: dict):
        self.switch_to_frame_element(self.find_presented_element(self.CARD_NUMBER_IFRAME_LOCATOR))
        self.find_clickable_element(self.CARD_NUMBER_LOCATOR).send_keys(info["Credit Card No"])
        self.switch_to_default_content()
        self.switch_to_frame_element(self.find_presented_element(self.EXPIRE_DATE_IFRAME_LOCATOR))
        self.find_clickable_element(self.EXPIRE_DATE_LOCATOR).send_keys(info["Expiry Date"])
        self.switch_to_default_content()
        self.switch_to_frame_element(self.find_presented_element(self.SECURITY_CODE_IFRAME_LOCATOR))
        self.find_clickable_element(self.SECURITY_CODE_LOCATOR).send_keys(info["Security Code"])
        self.switch_to_default_content()

    def wait_for_thankyou_page(self):
        self.find_presented_element((By.CLASS_NAME, "thankyou__content"))
