import json
import unittest

from project.tests.base import BaseTestCase
from database_singleton import Singleton

from project.api.models import Category

db = Singleton().database_connection()


def add_category(name):
    category = Category(name)
    db.session.add(category)
    db.session.commit()
    return category


class TestProductCategory(BaseTestCase):
    def test_get_all_category(self):
        add_category("Eletrodomésticos")
        add_category("Livros e revistas")
        add_category("Eletrônicos")

        with self.client:
            response = self.client.get("/product_category")
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn("success", data["status"])

            self.assertIn("Eletrodomésticos", data["data"]["categories"][0]["name"])
            self.assertIn("Livros e revistas", data["data"]["categories"][1]["name"])
            self.assertIn("Eletrônicos", data["data"]["categories"][2]["name"])
