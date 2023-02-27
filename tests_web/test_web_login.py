import allure
import pytest

from page_objects.login_page import LoginPage

TESTCASE_BASE_LINK = "https://github.com/AppWorks-School-Materials/Automation-Test-Program-Batch1/blob/main/"
TESTCASE_CATEGORY = "week_6/part-1/Project1_UIAutomation.md"

invalid_user = {
    "user1": {"email": "user1@foo.bar", "password": "abcdefg"},
    "user2": {"email": "user2@foo.bar", "password": "1234567"},
}


@pytest.fixture
def login(driver):
    _login_url = "http://54.201.140.239/login.html"
    return LoginPage(driver, _login_url)


@allure.feature("Login and Logout")
@allure.story("Login and Logout")
@allure.title("Login and Logout Success")
@allure.testcase(
    TESTCASE_BASE_LINK + TESTCASE_CATEGORY + "#scenario-login-and-logout-success", "Login and Logout Success"
)
@allure.link("http://54.201.140.239/login.html", "待測網頁")
def test_login_logout_success(login, user, database):
    """
    確認使用正確的email與password時，能成功登入並取得jwt token。
    """
    with allure.step("Enter correct email and password then login"):
        login.enter_email_and_password(user["email"], user["password"])
        login.login()

    with allure.step("Check if login success"):
        alert = login.wait_alert_prompt()
        assert alert.text == "Login Success"
        alert.accept()

    with allure.step("Check there is jwt token in local storage"):
        jwt = login.get_jwt_token()
        allure.attach(jwt, "jwt_token", attachment_type=allure.attachment_type.TEXT)
        assert jwt == database.get_access_token_by_email(user["email"])

    with allure.step("Logout"):
        login.logout()

    with allure.step("Check if logout success"):
        alert = login.wait_alert_prompt()
        assert alert.text == "Logout Success"
        alert.accept()

    with allure.step("Check if jwt token has been deleted"):
        assert login.get_jwt_token() is None and database.get_access_token_by_email(user["email"]) == ""


@allure.feature("Login and Logout")
@allure.story("Login and Logout")
@allure.title("Login Failed with incorrect email or password")
@allure.testcase(
    TESTCASE_BASE_LINK + TESTCASE_CATEGORY + "#scenario-login-failed-with-incorrect-email-or-password",
    "Login Failed with incorrect email or password",
)
@allure.link("http://54.201.140.239/login.html", "待測網頁")
@pytest.mark.parametrize("user", [invalid_user["user1"]])
def test_login_failed(login, user):
    """
    確認使用錯誤的email與password時，會登入錯誤。
    """
    with allure.step("Enter incorrect email and password then login"):
        login.enter_email_and_password(user["email"], user["password"])
        login.login()

    with allure.step("Check if login failed"):
        alert = login.wait_alert_prompt()
        assert alert.text == "Login Failed"
        alert.accept()


@allure.feature("Login and Logout")
@allure.story("Login and Logout")
@allure.title("Login with invalid access token")
@allure.testcase(
    TESTCASE_BASE_LINK + TESTCASE_CATEGORY + "#scenario-login-with-invalid-access-token",
    "Login with invalid access token",
)
@allure.link("http://54.201.140.239/login.html", "待測網頁")
def test_login_with_invalid_token(login, user):
    """
    確認使用無效的jwt token時，不會允許登入。
    """
    with allure.step("Enter correct email and password then login"):
        login.enter_email_and_password(user["email"], user["password"])
        login.login()
        alert = login.wait_alert_prompt()
        alert.accept()

    with allure.step("Get jwt token in local storage"):
        jwt = login.get_jwt_token()
        allure.attach(jwt, "jwt_token", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Logout"):
        login.logout()
        alert = login.wait_alert_prompt()
        alert.accept()

    with allure.step("Set jwt token to local storage"):
        login.set_jwt_token(jwt)

    with allure.step("Check if error message 'Invalid Access Token' shows"):
        login.driver.get("http://54.201.140.239/profile.html")
        alert = login.wait_alert_prompt()
        assert alert.text == "Invalid Access Token"
        alert.accept()
