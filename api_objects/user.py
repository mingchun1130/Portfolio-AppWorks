import json
import logging
from typing import Optional

import allure

from api_objects.request_util import RequestUtil


class UserAPI(RequestUtil):
    def __init__(self):
        super().__init__()
        self.base_url = "http://54.201.140.239/api/1.0/user/"
        self.login_api = self.base_url + "login"
        self.logout_api = self.base_url + "logout"
        self.profile_api = self.base_url + "profile"

    def set_login_request_body(self, payload: dict) -> None:
        self.payload = payload
        allure.attach(
            json.dumps(self.payload, indent=2), "Login Request Body", attachment_type=allure.attachment_type.TEXT
        )

    def login(self) -> int:
        if hasattr(self, "payload"):
            response = self.post(self.login_api, json=self.payload)
        else:
            Exception("Please set login info first.")
        if response.status_code == 200:
            response_body = response.json()["data"]
            self.session.headers.update({"authorization": f'Bearer {response_body["access_token"]}'})
            self.access_token = response_body["access_token"]
            self.loggedin_user = response_body["user"]
        return response.status_code

    def get_access_token(self) -> str:
        return self.access_token if hasattr(self, "access_token") else ""

    def get_loggedin_user_data(self) -> dict:
        if hasattr(self, "access_token"):
            return self.loggedin_user
        else:
            raise Exception("You have not logged in successfully yet.")

    def logout(self, token: Optional[str] = None) -> int:
        if token is not None:
            self.access_token = token
            self.session.headers.update({"authorization": f"Bearer {token}"})
        if self.session.headers.get("authorization", None) is not None:
            logging.info(f"Logout with access token: {self.session.headers['authorization']}")
            response = self.post(self.logout_api)
            delattr(self, "access_token")
            self.session.headers.pop("authorization")
        else:
            logging.info("Logout without access token")
            response = self.post(self.logout_api)
        if response.status_code == 200:
            delattr(self, "loggedin_user")
        return response.status_code

    def get_profile(self, token: Optional[str] = None):
        if token is not None:
            self.session.headers.update({"authorization": f"Bearer {token}"})
        if self.session.headers.get("authorization", None) is not None:
            logging.info(f"Get profile with access token: {self.session.headers['authorization']}")
            response = self.get(self.profile_api)
        else:
            logging.info("Get profile without access token")
            response = self.get(self.profile_api)
        if response.status_code == 200:
            return response.status_code, response.json()["data"]
        else:
            return response.status_code
