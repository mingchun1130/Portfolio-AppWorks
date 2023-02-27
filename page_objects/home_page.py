from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from page_objects.base_page import BasePage


class HomePage(BasePage):
    SEARCH = (By.CSS_SELECTOR, "input.header__search-input")
    CATEGORY = {
        "women": (By.LINK_TEXT, "女裝"),
        "men": (By.LINK_TEXT, "男裝"),
        "accessories": (By.LINK_TEXT, "配件"),
    }
    PRESENTED_PRODUCTS = (By.CSS_SELECTOR, "a.product")
    PRESENTED_PRODUCT_NAMES = (By.CSS_SELECTOR, "div.product__title")

    def __init__(self, driver, home_url=None):
        super().__init__(driver)
        if home_url is not None:
            self.driver.get(home_url)

    def _get_presented_product_amount(self):
        # Wait for current products disappear before page refreshing.
        self.wait_element_disappear((By.XPATH, "//div[@class='products' and count(a)>0]/child::*"))
        self.presented_amount = len(
            self.find_presented_elements((By.XPATH, "//div[@class='products' and count(a)>0]/child::*"))
        )

    def search_product_by_keyword(self, keyword):
        search_bar = self.find_clickable_element(self.SEARCH)
        search_bar.send_keys(keyword)
        search_bar.send_keys(Keys.ENTER)
        self._get_presented_product_amount()

    def switch_category_to(self, category: str):
        if category in self.CATEGORY:
            self.find_clickable_element(self.CATEGORY[category]).click()
            self._get_presented_product_amount()
        else:
            raise ValueError(f"The input value '{category}' isn't in women/men/accessories")

    def load_all_products(self, total):
        while self.presented_amount < total:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.presented_amount = len(
                self.find_presented_elements(
                    (
                        By.XPATH,
                        f"//div[@class='products' and count(a)>{self.presented_amount}]/child::*",
                    )
                )
            )

    def get_presented_product_names(self):
        return self.find_presented_elements(self.PRESENTED_PRODUCT_NAMES)

    def get_presented_products(self):
        return self.find_presented_elements(self.PRESENTED_PRODUCTS)
