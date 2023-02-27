from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from page_objects.base_page import BasePage


class LoginPage(BasePage):
    EMAIL_LOCATOR = (By.ID, "email")
    PASSWORD_LOCATOR = (By.ID, "pw")
    LOGIN_BTN_LOCATOR = (By.CSS_SELECTOR, "button.login100-form-btn")
    LOGOUT_BTN_LOCATOR = (By.XPATH, "//button[text()='登出']")

    def __init__(self, driver, login_url=None):
        super().__init__(driver)
        if login_url is not None:
            self.driver.get(login_url)

    def enter_email(self, email):
        self.find_clickable_element(self.EMAIL_LOCATOR).send_keys(email)

    def enter_password(self, password):
        self.find_clickable_element(self.PASSWORD_LOCATOR).send_keys(password)

    def enter_email_and_password(self, email, password):
        self.enter_email(email)
        self.enter_password(password)

    def login(self):
        self.find_and_click_element(self.LOGIN_BTN_LOCATOR)

    def logout(self):
        self.find_and_click_element(self.LOGOUT_BTN_LOCATOR)

    def get_jwt_token(self) -> str:
        return self.driver.execute_script("return localStorage.getItem('jwtToken');")

    def set_jwt_token(self, token: str):
        self.driver.execute_script(f"localStorage.setItem('jwtToken', '{token}');")

    def is_redirected_to_login_page(self) -> bool:
        try:
            self.find_presented_element(self.LOGIN_BTN_LOCATOR)
        except TimeoutException:
            return False
        else:
            return True
