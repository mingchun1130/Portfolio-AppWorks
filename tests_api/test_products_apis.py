import math

import allure
import pytest

from api_objects.products import ProductsAPI


def shape_db_product_data(db_products, id_list):
    products = []
    for id in id_list:
        df = db_products.query("id==@id")
        detail = (
            df[
                [
                    "id",
                    "category",
                    "title",
                    "description",
                    "price",
                    "texture",
                    "wash",
                    "place",
                    "note",
                    "story",
                    "main_image",
                ]
            ]
            .drop_duplicates(subset="id")
            .to_dict("records")[0]
        )
        detail["images"] = df[["image_id", "image"]].drop_duplicates(subset="image_id")["image"].tolist()
        detail["variants"] = (
            df[["variant_id", "color_code", "size", "stock"]]
            .drop_duplicates(subset="variant_id")
            .set_index("variant_id")
            .to_dict("records")
        )
        detail["colors"] = (
            df[["color_code", "color_name"]]
            .drop_duplicates(subset="color_code")
            .rename(columns={"color_code": "code", "color_name": "name"})
            .to_dict("records")
        )
        detail["sizes"] = df["size"].drop_duplicates().tolist()
        products.append(detail)
    return products


@pytest.fixture
def category_result(db_products, request):
    if request.param == "all":
        id_list = db_products["id"].drop_duplicates().tolist()
    else:
        id_list = (
            db_products[["id", "category"]]
            .drop_duplicates(subset="id")
            .query("category==@request.param")["id"]
            .tolist()
        )
    last_page = math.ceil(len(id_list) / 6) - 1
    if last_page < 0:
        last_page = 0
    return request.param, shape_db_product_data(db_products, id_list), last_page


@pytest.fixture
def keyword_result(db_products, request):
    db_unique = db_products[["id", "title"]].drop_duplicates(subset="id")
    id_list = db_unique[db_unique["title"].str.contains(request.param)]["id"].tolist()
    last_page = math.ceil(len(id_list) / 6) - 1
    if last_page < 0:
        last_page = 0
    return request.param, shape_db_product_data(db_products, id_list), last_page


@pytest.fixture
def detail_result(db_products, request):
    id_list = [request.param]
    return request.param, shape_db_product_data(db_products, id_list)


@allure.feature("Products APIs")
@allure.story("/products/{category}?paging={paging}")
@allure.title("Search products with valid category and page")
@pytest.mark.parametrize("category_result", ["all", "women", "men", "accessories"], indirect=True)
def test_category_with_valid_input(category_result):
    category, db_filter_result, last_page = category_result
    product = ProductsAPI()

    with allure.step("Get category products of first page"):
        res = product.get_products_by_category(category, 0)
        assert res.status_code == 200
    with allure.step("Assert if product in first page is the same with database"):
        assert res.json()["data"] == db_filter_result[0:6]

    with allure.step("Get category products of last page"):
        res = product.get_products_by_category(category, last_page)
        assert res.status_code == 200
    with allure.step("Assert if product in last page is the same with database"):
        last_page_index = last_page * 6
        assert res.json()["data"] == db_filter_result[last_page_index:]


@allure.feature("Products APIs")
@allure.story("/products/{category}?paging={paging}")
@allure.title("Search products without the page parameter")
@pytest.mark.parametrize("category_result", ["all", "women", "men", "accessories"], indirect=True)
def test_category_without_page(category_result):
    category, db_filter_result, _ = category_result
    product = ProductsAPI()

    with allure.step("Get category products withou page"):
        res = product.get_products_by_category(category)
        assert res.status_code == 200
    with allure.step("Assert if product in first page is the same with database"):
        assert res.json()["data"] == db_filter_result[0:6]


@allure.feature("Products APIs")
@allure.story("/products/{category}?paging={paging}")
@allure.title("Search products with an out of range page number")
@pytest.mark.parametrize("category_result", ["all", "women", "men", "accessories"], indirect=True)
def test_category_with_out_of_range_page(category_result):
    category, _, last_page = category_result
    product = ProductsAPI()

    with allure.step("Get category products of last+1 page"):
        res = product.get_products_by_category(category, last_page + 1)
        assert res.status_code == 200
    with allure.step("Assert if no products"):
        assert res.json()["data"] == []


@allure.feature("Products APIs")
@allure.story("/products/{category}?paging={paging}")
@allure.title("Search products with minus page number")
@pytest.mark.parametrize("category", ["women"])
def test_category_with_minus_page(category):
    product = ProductsAPI()

    with allure.step("Get category products of -1 page"):
        res = product.get_products_by_category(category, -1)
    with allure.step("Assert if status code is 400"):
        # 雖然實際上是報500，但因為理想應該是要報400所以期待結果維持理想值
        assert res.status_code == 400


@allure.feature("Products APIs")
@allure.story("/products/{category}?paging={paging}")
@allure.title("Search products with invalid category name")
@pytest.mark.parametrize("category", ["invalid"])
def test_category_with_invalid_category_name(category):
    product = ProductsAPI()

    with allure.step("Get products of invalid category"):
        res = product.get_products_by_category(category, 0)
    with allure.step("Assert if status code is 400"):
        assert res.status_code == 400


@allure.feature("Products APIs")
@allure.story("/products/search?keyword={keyword}&paging={paging}")
@allure.title("Search products with valid keyword and page")
@pytest.mark.parametrize("keyword_result", ["洋裝", "Hello"], indirect=True)
def test_keyword_with_valid_input(keyword_result):
    keyword, db_filter_result, last_page = keyword_result
    product = ProductsAPI()

    with allure.step("Get keyword products of first page"):
        res = product.get_products_by_keyword(keyword, 0)
        assert res.status_code == 200

    with allure.step("Assert if product in first page is the same with database"):
        assert res.json()["data"] == db_filter_result[0:6]

    with allure.step("Get keyword products of last page"):
        res = product.get_products_by_keyword(keyword, last_page)
        assert res.status_code == 200

    with allure.step("Assert if product in last page is the same with database"):
        last_page_index = last_page * 6
        assert res.json()["data"] == db_filter_result[last_page_index:]


@allure.feature("Products APIs")
@allure.story("/products/search?keyword={keyword}&paging={paging}")
@allure.title("Search products with valid keyword and an out of range page number")
@pytest.mark.parametrize("keyword_result", ["洋裝"], indirect=True)
def test_keyword_with_out_of_range_page(keyword_result):
    keyword, _, last_page = keyword_result
    product = ProductsAPI()

    with allure.step("Get keyword products of last+1 page"):
        res = product.get_products_by_keyword(keyword, last_page + 1)
        assert res.status_code == 200

    with allure.step("Assert if no products"):
        assert res.json()["data"] == []


@allure.feature("Products APIs")
@allure.story("/products/search?keyword={keyword}&paging={paging}")
@allure.title("Search products with valid keyword and minus page number")
@pytest.mark.parametrize("keyword", ["洋裝"])
def test_keyword_with_minus_page(keyword):
    product = ProductsAPI()

    with allure.step("Get keyword products of -1 page"):
        res = product.get_products_by_keyword(keyword, -1)
    with allure.step("Assert if status code is 400"):
        # 雖然實際上是報500，但因為理想應該是要報400所以期待結果維持理想值
        assert res.status_code == 400


@allure.feature("Products APIs")
@allure.story("/products/search?keyword={keyword}&paging={paging}")
@allure.title("Search products without the keyword parameter")
def test_keyword_without_keywords():
    product = ProductsAPI()

    with allure.step("Get products without keywords"):
        res = product.get_products_by_keyword(page=0)
    with allure.step("Assert if status code is 400"):
        assert res.status_code == 400


@allure.feature("Products APIs")
@allure.story("/products/details/?id={product_id}")
@allure.title("Get product details with valid product id")
@pytest.mark.parametrize("detail_result", [201902191210], indirect=True)
def test_details_with_valid_product_id(detail_result):
    product_id, db_filter_result = detail_result
    product = ProductsAPI()

    with allure.step("Get product detail with valid product id"):
        res = product.get_products_by_id(product_id)
        assert res.status_code == 200
    with allure.step("Assert if product detail is the same with database"):
        assert res.json()["data"] == db_filter_result[0]


@allure.feature("Products APIs")
@allure.story("/products/details/?id={product_id}")
@allure.title("Get product details with invalid product id")
@pytest.mark.parametrize("product_id", [123, "abc"])
def test_details_with_invalid_product_id(product_id):
    product = ProductsAPI()

    with allure.step("Get product detail with invalid product id"):
        res = product.get_products_by_id(product_id)
    with allure.step("Assert if status code is 400"):
        assert res.status_code == 400


@allure.feature("Products APIs")
@allure.story("/products/details/?id={product_id}")
@allure.title("Get product details without the product id parameter")
def test_details_without_product_id():
    with allure.step("Get product detail without product id"):
        product = ProductsAPI()
        res = product.get_products_by_id()
    with allure.step("Assert if status code is 400"):
        assert res.status_code == 400
