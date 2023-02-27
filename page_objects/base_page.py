from selenium.webdriver.common.by import By

from page_objects.browser import Browser


class BasePage(Browser):
    def __init__(self, driver) -> None:
        super().__init__(driver)

    def get_cart_number(self) -> int:
        cart_number_locator = (By.CLASS_NAME, "header__link-icon-cart-number")
        return int(self.find_presented_element(cart_number_locator).text)

    def enter_shopping_cart(self) -> None:
        shopping_cart_locator = (By.CSS_SELECTOR, "a[href='./cart.html']")
        self.find_and_click_element(shopping_cart_locator)

    def move_to_member_profile(self) -> None:
        member_profile_locator = (By.CSS_SELECTOR, "a[href='./profile.html']")
        self.find_and_click_element(member_profile_locator)
