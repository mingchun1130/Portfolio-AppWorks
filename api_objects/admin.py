import json
import logging
from typing import Optional

import allure

from api_objects.user import UserAPI
from test_data.get_data_from_excel import GetData


class AdminAPI(UserAPI):
    created_product_id: Optional[str] = None

    def __init__(self) -> None:
        super().__init__()
        self.base_url = "http://54.201.140.239/api/1.0/admin/product"

    def create_product(self, payload: dict, image_files):
        allure.attach(
            json.dumps(payload, indent=2, ensure_ascii=False),
            "Payload",
            attachment_type=allure.attachment_type.TEXT,
        )
        for file in image_files:
            allure.attach(file[1].read(), file[0], attachment_type=allure.attachment_type.JPG)
        return self.post(self.base_url, data=payload, files=image_files)

    def generate_product_payload(self, product_info: dict) -> dict:
        return {
            "category": product_info["Category"],
            "title": product_info["Title"],
            "description": product_info["Description"],
            "price": product_info["Price"],
            "texture": product_info["Texture"],
            "wash": product_info["Wash"],
            "place": product_info["Place of Product"],
            "note": product_info["Note"],
            "story": product_info["Story"],
            "color_ids": product_info["ColorIDs"].split(","),
            "sizes": product_info["Sizes"].split(","),
        }

    def generate_product_image_files(self, product_info: dict) -> list:
        test_data = GetData()
        images = []
        if product_info["Main Image"] != "":
            self.main_image = open(test_data.get_file_full_path(product_info["Main Image"]), "rb")
            images.append(("main_image", self.main_image))
        if product_info["Other Image 1"] != "":
            self.other_image_1 = open(test_data.get_file_full_path(product_info["Other Image 1"]), "rb")
            images.append(("other_images", self.other_image_1))
        if product_info["Other Image 2"] != "":
            self.other_image_2 = open(test_data.get_file_full_path(product_info["Other Image 2"]), "rb")
            images.append(("other_images", self.other_image_2))
        return images

    def delete_product_by_id(self, product_id):
        return self.delete(self.base_url + f"/{product_id}")

    def close_opened_images(self) -> None:
        if hasattr(self, "main_image"):
            logging.info('Closing "mainImage.jpg"')
            self.main_image.close()
        if hasattr(self, "other_image_1"):
            logging.info('Closing "otherImage0.jpg"')
            self.other_image_1.close()
        if hasattr(self, "other_image_2"):
            logging.info('Closing "otherImage1.jpg"')
            self.other_image_2.close()
