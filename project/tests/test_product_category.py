import json
import unittest
from project.tests.base import BaseTestCase
from project.api.models import Category
from project.api.models import db
from project.tests.utils import add_category

PRODUCT_CATEGORY_BASE_URL = "/product_category"


class TestProductCategory(BaseTestCase):
    def test_add_categories(self):
        with self.client:
            response = self.client.post(
                PRODUCT_CATEGORY_BASE_URL,
                data=json.dumps({"name": "Jogos"}),
                content_type="application/json",
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)
            self.assertIn("Category Jogos was created!", data["data"]["message"])
            self.assertIn("success", data["status"])

    def test_add_categories_invalid_json(self):
        with self.client:
            response = self.client.post(
                PRODUCT_CATEGORY_BASE_URL,
                data=json.dumps({}),
                content_type="application/json",
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid payload.", data["message"])
            self.assertIn("fail", data["status"])

    def test_get_all_category(self):
        add_category("Eletrodomésticos")
        add_category("Livros e revistas")
        add_category("Eletrônicos")

        with self.client:
            response = self.client.get(PRODUCT_CATEGORY_BASE_URL)
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn("success", data["status"])

            self.assertIn("Eletrodomésticos", data["data"]["categories"][0]["name"])
            self.assertIn("Livros e revistas", data["data"]["categories"][1]["name"])
            self.assertIn("Eletrônicos", data["data"]["categories"][2]["name"])
