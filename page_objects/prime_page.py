from typing import Optional

from selenium.webdriver.common.by import By

from page_objects.cart_page import CartPage


class PrimePage(CartPage):
    TEST_CARD_INFO = {
        "Credit Card No": "4242424242424242",
        "Expiry Date": "01/23",
        "Security Code": "123",
    }
    # "id=cc-ccv" in cart page but "id=cc-cvc" in prime page.
    SECURITY_CODE_LOCATOR = (By.ID, "cc-cvc")
    GET_PRIME_BTN_LOCATOR = (By.ID, "checkoutBtn")

    def __init__(self, driver, prime_url=None) -> None:
        super().__init__(driver)
        self.prime_url = "http://54.201.140.239/get_prime.html"
        if prime_url is not None:
            self.prime_url = prime_url
        self.driver.get(self.prime_url)

    def get_prime(self, card_info: Optional[dict] = None) -> str:
        if card_info is None:
            self.fill_in_payment_info(self.TEST_CARD_INFO)
        else:
            self.fill_in_payment_info(card_info)
        self.find_and_click_element(self.GET_PRIME_BTN_LOCATOR)
        alert = self.wait_alert_prompt()
        return alert.text
