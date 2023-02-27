from pprint import pprint

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from database.config import STYLISH_DB_URL


class StylishBackend:
    def __init__(self):
        self.engine = create_engine(
            STYLISH_DB_URL,
            poolclass=NullPool,
        )

    def get_all_product_names(self) -> pd.DataFrame:
        """Get all product names.

        Returns:
            DataFrame: Return all product names in dataframe.
        """
        sql = """
        SELECT id, category, title
          FROM product;
        """
        return pd.read_sql_query(sql, self.engine).set_index("id")

    def get_color_code_dict(self) -> dict:
        """Get all color code of each color name.

        Returns:
            Dict: Return all color code in dictionary.
        """
        sql = """
        SELECT name, code
          FROM color;
        """
        return pd.read_sql_query(sql, self.engine).set_index("name").to_dict()["code"]

    def get_all_product_detail(self) -> pd.DataFrame:
        """Get all product detail info.

        Returns:
            DataFrame: Return all product detail info in dataframe.
        """
        sql = """
        SELECT product.id, product.category, product.title, description, price, texture,
               wash, place, note, story, main_image, product_images.id AS image_id, image,
               variant.id AS variant_id, color.code AS color_code, variant.size, stock, color.name AS color_name
          FROM product
               INNER JOIN product_images
               ON product_images.product_id = product.id
               INNER JOIN variant
               ON variant.product_id = product.id
               INNER JOIN color
               ON color.id = variant.color_id;
        """
        return pd.read_sql_query(sql, self.engine)

    def get_access_token_by_email(self, email: str) -> str:
        """Get jwt Token.

        Returns:
            str: Return specific jwt Token registered in database.
        """
        sql = f"""
        SELECT access_token
          FROM user
         WHERE email = '{email}';
        """
        return pd.read_sql_query(sql, self.engine).iloc[0]["access_token"]

    def get_user_data_by_email(self, email: str) -> dict:
        sql = f"""
        SELECT id,
               provider,
               email,
               name,
               picture
          FROM user
         WHERE email = '{email}';
        """
        return pd.read_sql_query(sql, self.engine).to_dict("records")[0]

    def get_product_detail_by_id(self, product_id) -> pd.DataFrame:
        sql = f"""
        SELECT product.id, category, title, description, price, texture, wash, place, note, story, main_image,
               product_images.id AS image_id, image,
               variant.id AS variant_id, size, stock,
               color.id AS color_id, code, color.name
          FROM product
               INNER JOIN product_images
               ON product_images.product_id = product.id
               INNER JOIN variant
               ON variant.product_id = product.id
               INNER JOIN color
               ON color.id = variant.color_id
         WHERE product.id = {product_id};
        """
        return pd.read_sql_query(sql, self.engine)

    def get_order_detail_by_number(self, number: str):
        sql = f"""
        SELECT id, number, time, status, details, user_id, total
          FROM order_table
         WHERE number = '{number}';
        """
        return pd.read_sql_query(sql, self.engine).to_dict("records")[0]


def _main():
    df = StylishBackend().get_product_detail_by_id(1671269183625)
    pprint(df.empty)


if __name__ == "__main__":
    _main()
