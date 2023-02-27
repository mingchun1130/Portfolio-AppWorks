from api_objects.request_util import RequestUtil


class ProductsAPI(RequestUtil):
    def __init__(self):
        super().__init__()
        self.base_url = "http://54.201.140.239/api/1.0/products/"

    def get_products_by_category(self, category=None, page=None):
        if category is None and page is None:
            url = f"{self.base_url}"
        elif category is None:
            url = f"{self.base_url}?paging={page}"
        elif page is None:
            url = f"{self.base_url}{category}"
        else:
            url = f"{self.base_url}{category}?paging={page}"
        return self.get(url)

    def get_products_by_keyword(self, keyword=None, page=None):
        if keyword is None and page is None:
            url = f"{self.base_url}search"
        elif keyword is None:
            url = f"{self.base_url}search?paging={page}"
        elif page is None:
            url = f"{self.base_url}search?keyword={keyword}"
        else:
            url = f"{self.base_url}search?keyword={keyword}&paging={page}"
        return self.get(url)

    def get_products_by_id(self, product_id=None):
        if product_id is None:
            url = f"{self.base_url}details/"
        else:
            url = f"{self.base_url}details/?id={product_id}"
        return self.get(url)
