import json
import logging

import allure
import requests


class RequestUtil:
    def __init__(self):
        self.session = requests.Session()

    def post(self, url, **kwargs):
        logging.info(f"POST {url}")
        res = self.session.post(url, **kwargs)
        self._log_response(res)
        return res

    def get(self, url, **kwargs):
        logging.info(f"GET {url}")
        res = self.session.get(url, **kwargs)
        self._log_response(res)
        return res

    def delete(self, url, **kwargs):
        logging.info(f"DELETE {url}")
        res = self.session.delete(url, **kwargs)
        self._log_response(res)
        return res

    def _log_response(self, response: requests.Response):
        logging.info(f"Status code is {response.status_code}")
        allure.attach(
            json.dumps(dict(response.headers), indent=2),
            "Response Headers",
            attachment_type=allure.attachment_type.TEXT,
        )
        allure.attach(response.text, "Response Body", attachment_type=allure.attachment_type.TEXT)
