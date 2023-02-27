import allure
import pytest
from selenium.common.exceptions import TimeoutException

valid_keywords = ["洋裝"]
invalid_keywords = ["Hello"]


@allure.feature("Filter")
@allure.story("Filter product via search")
class TestSearch:
    @allure.title("Search by keyword")
    @pytest.mark.parametrize("keyword", valid_keywords)
    def test_search_by_keyword(self, home, keyword):
        """
        確認搜尋出來的商品，是否都含有用以搜尋的關鍵字。
        """
        home.search_product_by_keyword(keyword)
        results = home.get_presented_product_names()
        for i in results:
            assert keyword in i.text, f"The searched product {i.text} doesn't contain {keyword}."

    @allure.title("Search without keyword(blank keyword)")
    @pytest.mark.parametrize("keyword", [""])
    def test_search_without_keyword(self, home, product_names, keyword):
        """
        確認未輸入關鍵字而進行搜尋時，是否會顯示所有商品。
        """
        home.search_product_by_keyword(keyword)
        home.load_all_products(product_names["title"].size)
        results = home.get_presented_product_names()
        assert len(results) == product_names["title"].size, "Not all products are displayed."

    @allure.title("Search with keywords not existed in products")
    @pytest.mark.parametrize("keyword", invalid_keywords)
    def test_no_product_found(self, home, keyword):
        """
        確認當沒有商品含有關鍵字時，是否會顯示空的搜尋結果。
        """
        with pytest.raises(TimeoutException):
            home.search_product_by_keyword(keyword)
            # Collect wrong search results and raise exception if TimeoutException hasn't occured.
            results = home.get_presented_product_names()
            result_names = []
            for i in results:
                result_names.append(i.text)
            raise Exception(
                f"""
                The keyword {keyword} shouldn't get any search result.
                The wrong search result is {result_names}.
                """
            )
