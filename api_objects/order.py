import json

import allure

from api_objects.user import UserAPI


class OrderAPI(UserAPI):
    def __init__(self):
        super().__init__()
        self.base_url = "http://54.201.140.239/api/1.0/order"

    def make_an_order(self, payload):
        allure.attach(
            json.dumps(payload, indent=2, ensure_ascii=False),
            "Order Detail",
            attachment_type=allure.attachment_type.TEXT,
        )
        return self.post(self.base_url, json=payload)

    def get_order_detail_by_number(self, order_number: str):
        # 雖然API Spec寫"order_id"，但checkout response跟database的名稱都是用order number
        # API Spec文件的用詞不一致
        return self.get(self.base_url + f"/{order_number}")
