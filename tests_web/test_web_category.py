import allure
import pytest

valid_categories = ["women", "men", "accessories"]


@allure.feature("Filter")
@allure.story("Filter product via category")
@allure.title("Switch category")
@pytest.mark.parametrize("category", valid_categories)
def test_category(home, product_names, category):
    """
    確認在進行切換Category的操作後，顯示商品是否有按照DB資料正確地篩選。
    """
    with allure.step("Get expected result from DB"):
        filtered_products = product_names.query("category==@category")["title"]

    with allure.step(f"Switch to target category '{category}'"):
        home.switch_category_to(category)

    with allure.step("Scroll down to load all product"):
        home.load_all_products(filtered_products.size)

    with allure.step("Get product titles presented in search result and compare with DB"):
        results = home.get_presented_product_names()
        for i in results:
            assert i.text in filtered_products.values, f"Wrong product {i.text} displayed in {category} category."
