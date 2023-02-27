import allure
import pytest

from api_objects.admin import AdminAPI
from database.stylish_backend import StylishBackend
from test_data.get_data_from_excel import GetData

test_data = GetData()
valid_api_product_create_info = test_data.get_valid_api_product_create_info()
invalid_api_product_create_info = test_data.get_invalid_api_product_create_info()


@pytest.fixture
def admin(valid_user_account: dict):
    _admin = AdminAPI()
    login_info = valid_user_account.copy()
    login_info.update({"provider": "native"})
    _admin.set_login_request_body(login_info)
    assert _admin.login() == 200
    yield _admin
    _admin.close_opened_images()
    if _admin.created_product_id is not None:
        _admin.delete_product_by_id(_admin.created_product_id)


@allure.feature("Admin APIs")
@allure.story("POST /admin/product and DELETE /admin/product/{product_id}")
@allure.title("[Happy] Valid required product info")
@pytest.mark.parametrize("product_info", valid_api_product_create_info)
def test_create_and_delete_product_with_valid_input(admin: AdminAPI, product_info):
    payload = admin.generate_product_payload(product_info)
    image_files = admin.generate_product_image_files(product_info)

    with allure.step("Create product with valid product info"):
        response = admin.create_product(payload, image_files)
        admin.created_product_id = response.json().get("data", {}).get("product_id", None)
        assert response.status_code == 200

    with allure.step("Assert if product created in database is the same with form data"):
        df = StylishBackend().get_product_detail_by_id(admin.created_product_id).astype("string")
        db_product_detail = (
            df[["category", "title", "description", "price", "texture", "wash", "place", "note", "story"]]
            .drop_duplicates(subset="category")
            .to_dict("records")[0]
        )
        db_product_detail.update(
            {
                "color_ids": df["color_id"].drop_duplicates().tolist(),
                "sizes": df["size"].drop_duplicates().tolist(),
            }
        )
        db_images = df["main_image"].drop_duplicates().tolist() + df["image"].drop_duplicates().tolist()
        assert db_product_detail == payload
        assert db_images == [image[1].name.split("/")[-1] for image in image_files]

    with allure.step("Delete product by product id which just created"):
        response = admin.delete_product_by_id(admin.created_product_id)
        assert response.status_code == 200
        assert StylishBackend().get_product_detail_by_id(admin.created_product_id).empty

    with allure.step("Delete product again"):
        response = admin.delete_product_by_id(admin.created_product_id)
        assert response.status_code == 400

    with allure.step("Assert if error message is correct"):
        assert response.json()["errorMsg"] == "Product ID not found."


@allure.feature("Admin APIs")
@allure.story("POST /admin/product")
@allure.title("[Irregular] Invalid Product Info")
@pytest.mark.parametrize("product_info", invalid_api_product_create_info)
def test_create_product_with_invalid_input(admin: AdminAPI, product_info):
    payload = admin.generate_product_payload(product_info)
    image_files = admin.generate_product_image_files(product_info)

    with allure.step("Create product with invalid product info"):
        response = admin.create_product(payload, image_files)
        admin.created_product_id = response.json().get("data", {}).get("created_product_id", None)
        assert response.status_code == 400

    with allure.step(f'Assert if error message is "{product_info["Error Msg"]}"'):
        assert response.json()["errorMsg"] == product_info["Error Msg"]
