from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Browser:
    def __init__(self, driver):
        self.driver = driver

    def find_clickable_element(self, locator: tuple, timeout: int = 5):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def find_and_click_element(self, locator: tuple, is_using_js: bool = False, timeout: int = 5):
        elem = self.find_clickable_element(locator, timeout)
        self.click_element(elem, is_using_js)

    def click_element(self, elem, is_using_js=False):
        if is_using_js:
            # For unknow reason, ElementClickInterceptedException shows even using "element_to_be_clickable".
            # A workaround found on Stack Overflow but the author also doesn't know what the root cause is.
            self.driver.execute_script("arguments[0].click();", elem)
        else:
            elem.click()

    def find_presented_element(self, locator: tuple, timeout: int = 5):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def find_presented_elements(self, locator: tuple, timeout: int = 5):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))

    def wait_element_disappear(self, locator=None, elem=None, timeout: int = 5):
        if locator is not None:
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
        elif elem is not None:
            WebDriverWait(self.driver, timeout).until(EC.staleness_of(elem))

    def wait_alert_prompt(self, timeout: int = 5):
        WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        return self.driver.switch_to.alert

    def switch_to_frame_element(self, elem) -> None:
        self.driver.switch_to.frame(elem)

    def switch_to_default_content(self) -> None:
        self.driver.switch_to.default_content()

    def switch_back_to_main_window(self) -> None:
        self.driver.switch_to.window(self.driver.window_handles[0])
