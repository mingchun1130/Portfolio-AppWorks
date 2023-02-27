import json

import allure

from api_objects.user import UserAPI
from database.stylish_backend import StylishBackend


@allure.feature("User APIs")
@allure.story("/user/login")
@allure.title("Login with valid account info")
def test_login_with_valid_request_doby(valid_user_account: dict, db_user_data: dict):
    with allure.step("Call user login api"):
        user = UserAPI()
        payload = valid_user_account.copy()
        payload.update({"provider": "native"})
        user.set_login_request_body(payload)
        assert user.login() == 200
    with allure.step("Assert if response is the same with database"):
        allure.attach(
            json.dumps(db_user_data, indent=2, default=str),
            "user data in database",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert user.get_access_token() == StylishBackend().get_access_token_by_email(valid_user_account["email"])
        assert user.get_loggedin_user_data() == db_user_data


@allure.feature("User APIs")
@allure.story("/user/login")
@allure.title("Login with invalid account info")
def test_login_with_invalid_request_body(valid_user_account: dict):
    with allure.step("Call user login api and assert response code is 400"):
        user = UserAPI()
        payload = valid_user_account.copy()
        user.set_login_request_body(payload)
        assert user.login() == 400


@allure.feature("User APIs")
@allure.story("/user/logout")
@allure.title("Logout with valid token")
def test_logout_with_valid_token(valid_user_account: dict):
    with allure.step("Call user login api"):
        user = UserAPI()
        payload = valid_user_account.copy()
        payload.update({"provider": "native"})
        user.set_login_request_body(payload)
        assert user.login() == 200
        assert user.get_access_token() == StylishBackend().get_access_token_by_email(valid_user_account["email"])
    with allure.step("Call logout api"):
        assert user.logout() == 200
    with allure.step("Assert if access token is deleted in database"):
        assert StylishBackend().get_access_token_by_email(valid_user_account["email"]) == ""


@allure.feature("User APIs")
@allure.story("/user/logout")
@allure.title("Logout without token")
def test_logout_without_token():
    with allure.step("Call logout api and ssert if response code is 401"):
        user = UserAPI()
        assert user.logout() == 401


@allure.feature("User APIs")
@allure.story("/user/logout")
@allure.title("Logout with expired token")
def test_logout_with_expired_token(valid_user_account: dict):
    with allure.step("Call user login api"):
        user = UserAPI()
        payload = valid_user_account.copy()
        payload.update({"provider": "native"})
        user.set_login_request_body(payload)
        assert user.login() == 200
    with allure.step("Call logout api"):
        token = user.get_access_token()
        assert user.logout() == 200
    with allure.step("Call logout api with expired token"):
        assert user.logout(token) == 403


@allure.feature("User APIs")
@allure.story("/user/profile")
@allure.title("Get logged-in user profile")
def test_get_loggedin_user_profile(valid_user_account: dict, db_user_data: dict):
    with allure.step("Call user login api"):
        user = UserAPI()
        payload = valid_user_account.copy()
        payload.update({"provider": "native"})
        user.set_login_request_body(payload)
        assert user.login() == 200
    with allure.step("Call profile api"):
        status_code, user_data = user.get_profile()
        assert status_code == 200
    with allure.step("Assert if response is the same with database"):
        db_user_data.pop("id")
        assert user_data == db_user_data


@allure.feature("User APIs")
@allure.story("/user/profile")
@allure.title("Get user profile without logged-in")
def test_get_user_profile_without_loggedin():
    with allure.step("Call profile api"):
        user = UserAPI()
        assert user.get_profile() == 401


@allure.feature("User APIs")
@allure.story("/user/profile")
@allure.title("Get user profile with invalid token")
def test_get_user_profile_with_invalid_token():
    with allure.step("Call profile api"):
        user = UserAPI()
        assert user.get_profile(token="Invalid token") == 403
