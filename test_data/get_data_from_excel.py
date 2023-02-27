from pathlib import Path
from pprint import pprint

import pandas as pd


class GetData:
    def __init__(self):
        self.root_path = Path(__file__).parent
        self.xls = pd.ExcelFile("/" / self.root_path / "Stylish-Test Case.xlsx")

    def get_invalid_checkout_data(self):
        df = pd.read_excel(self.xls, "Checkout with Invalid Value", dtype=str).fillna("")
        df["Receiver"] = df["Receiver"].replace("101 chars", "陳" * 101)
        df["Email"] = df["Email"].replace("51 chars", "abc@" + "a" * 43 + ".com")
        df["Address"] = df["Address"].replace("256 chars", "台" * 256)
        return df.to_dict("records")

    def get_valid_checkout_data(self):
        return pd.read_excel(self.xls, "Checkout with Valid Value", dtype=str).fillna("").to_dict("records")

    def get_file_full_path(self, file_name: str):
        if file_name == "":
            return None
        else:
            return str("/" / self.root_path / file_name)

    def get_invalid_product_create_info(self):
        df = pd.read_excel(self.xls, "Create Product Failed", dtype=str).fillna("")
        df["Title"] = df["Title"].replace("256 chars", "裙" * 256)
        df["Description"] = df["Description"].replace("256 chars", "詳細內容" * 64)
        df["Texture"] = df["Texture"].replace("128 chars", "棉" * 128)
        df["Wash"] = df["Wash"].replace("128 chars", "手洗" * 64)
        df["Place of Product"] = df["Place of Product"].replace("128 chars", "TW" * 64)
        df["Note"] = df["Note"].replace("128 chars", "Note" * 32)
        df["Main Image"] = df["Main Image"].replace("sample image", "mainImage.jpg")
        df["Other Image 1"] = df["Other Image 1"].replace("sample image", "otherImage0.jpg")
        df["Other Image 2"] = df["Other Image 2"].replace("sample image", "otherImage1.jpg")
        return df.to_dict("records")

    def get_valid_product_create_info(self):
        df = pd.read_excel(self.xls, "Create Product Success", dtype=str).fillna("")
        df["Title"] = df["Title"].replace("連身裙", "Mingchun_連身裙")
        df["Title"] = df["Title"].replace("1 chars", "I")
        df["Title"] = df["Title"].replace("255 chars", "Mingchun_" + "裙" * 246)
        df["Description"] = df["Description"].replace("1 chars", "I")
        df["Description"] = df["Description"].replace("255 chars", "連" * 255)
        df["Texture"] = df["Texture"].replace("1 chars", "I")
        df["Texture"] = df["Texture"].replace("127 chars", "棉" * 127)
        df["Wash"] = df["Wash"].replace("1 chars", "I")
        df["Wash"] = df["Wash"].replace("127 chars", "洗" * 127)
        df["Place of Product"] = df["Place of Product"].replace("1 chars", "I")
        df["Place of Product"] = df["Place of Product"].replace("127 chars", "台" * 127)
        df["Note"] = df["Note"].replace("1 chars", "I")
        df["Note"] = df["Note"].replace("127 chars", "筆" * 127)
        df["Story"] = df["Story"].replace("1 chars", "I")
        df["Main Image"] = df["Main Image"].replace("sample image", "mainImage.jpg")
        df["Other Image 1"] = df["Other Image 1"].replace("sample image", "otherImage0.jpg")
        df["Other Image 2"] = df["Other Image 2"].replace("sample image", "otherImage1.jpg")
        return df.to_dict("records")

    def get_valid_api_product_create_info(self):
        df = pd.read_excel(self.xls, "API Create Product Success", dtype=str).fillna("")
        df["Title"].replace("連身裙", "Mingchun_連身裙", inplace=True)
        df["Main Image"].replace("sample image", "mainImage.jpg", inplace=True)
        df["Other Image 1"].replace("sample image", "otherImage0.jpg", inplace=True)
        df["Other Image 2"].replace("sample image", "otherImage1.jpg", inplace=True)
        df.replace("1 chars", "I", inplace=True)
        df.replace("255 chars", "Mingchun_" + "褲" * 246, inplace=True)
        df.replace("127 chars", "Mingchun_" + "裙" * 118, inplace=True)
        return df.to_dict("records")

    def get_invalid_api_product_create_info(self):
        df = pd.read_excel(self.xls, "API Create Product Failed", dtype=str).fillna("")
        df["Main Image"].replace("sample image", "mainImage.jpg", inplace=True)
        df["Other Image 1"].replace("sample image", "otherImage0.jpg", inplace=True)
        df["Other Image 2"].replace("sample image", "otherImage1.jpg", inplace=True)
        df.replace("256 chars", "Mingchun_" + "褲" * 247, inplace=True)
        df.replace("128 chars", "Mingchun_" + "裙" * 119, inplace=True)
        return df.to_dict("records")


if __name__ == "__main__":
    test_data = GetData()
    pprint(test_data.get_invalid_checkout_data())
    pprint(test_data.get_valid_checkout_data())
    pprint(test_data.get_invalid_product_create_info())
    pprint(test_data.get_valid_product_create_info())
    pprint(test_data.get_valid_api_product_create_info())
