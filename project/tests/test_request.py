import json
import unittest
from project.tests.base import BaseTestCase
from project.api.models import Request
from project.api.models import db
from project.tests.utils import add_request, add_category


class TestRequest(BaseTestCase):
    def test_get_all_requests(self):
        add_category("Eletrodomésticos")
        add_request(
            "Banco Imobiliario",
            "2020-09-12 00:00:00.000",
            "2020-09-30 00:00:00.000",
            "Queria um banco imobiliário emprestado para jogar com meus amigos neste fim de semana!",
            "matheus@email.com",
            1,
        )
        add_request(
            "Jogo da vida",
            "2020-09-12 00:00:00.000",
            "2020-09-30 00:00:00.000",
            "Queria um jogo da vida emprestado para jogar com meus amigos neste fim de semana!",
            "matheus@email.com",
            1,
        )
        add_request(
            "War",
            "2020-09-12 00:00:00.000",
            "2020-09-30 00:00:00.000",
            "Queria um war emprestado para jogar com meus amigos neste fim de semana!",
            "matheus@email.com",
            1,
        )

        with self.client:
            response = self.client.get("/requests")
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn("success", data["status"])

            self.assertEqual(len(data["data"]["requests"]), 3)

    def test_get_filtered_requests(self):
        add_category("Eletrodomésticos")
        add_request(
            "Jogo da vida",
            "2020-09-12 00:00:00.000",
            "2020-09-30 00:00:00.000",
            "Queria um jogo da vida emprestado para jogar com meus amigos neste fim de semana!",
            "matheus@email.com",
            1,
        )
        add_request(
            "War",
            "2020-09-12 00:00:00.000",
            "2020-09-30 00:00:00.000",
            "Queria um war emprestado para jogar com meus amigos neste fim de semana!",
            "matheus@email.com",
            1,
        )

        with self.client:
            response = self.client.get("/requests/1")
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn("success", data["status"])

            self.assertIn("Jogo da vida", data["data"]["requests"][0]["productname"])
            self.assertIn("War", data["data"]["requests"][1]["productname"])

    def test_update_lender_request(self):
        add_category("Eletrodomésticos")
        product = add_request(
            "Banco Imobiliario",
            "2020-09-12 00:00:00.000",
            "2020-09-30 00:00:00.000",
            "Queria um banco imobiliário emprestado para jogar com meus amigos neste fim de semana!",
            "matheus@email.com",
            1,
        )

        with self.client:
            response = self.client.patch(
                f"/requests/{product.requestid}",
                data=json.dumps({"lender": "maia@email.com"}),
                content_type="application/json",
            )

            data = json.loads(response.data.decode())
            self.assertIn("maia@email.com", data["request"]["lender"])

    def test_cannot_update_non_existing_request_lender(self):
        with self.client:
            response = self.client.patch(
                "/requests/8d27b6c1-ac8a-4f29-97b0-96cef6938267",
                data=json.dumps({"lender": "maia@email.com"}),
                content_type="application/json",
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)

    def test_finalize_request(self):
        add_category("Eletrodomésticos")
        product = add_request(
            "Banco Imobiliario",
            "2020-09-12 00:00:00.000",
            "2020-09-30 00:00:00.000",
            "Queria um banco imobiliário emprestado para jogar com meus amigos neste fim de semana!",
            "matheus@email.com",
            1,
        )

        with self.client:
            response = self.client.patch(
                f"/requests/{product.requestid}/finalize",
                content_type="application/json",
            )

            data = json.loads(response.data.decode())
            self.assertEqual(data["request"]["finalized"], True)

    def test_cannot_finalize_non_existing_request(self):
        with self.client:
            response = self.client.patch(
                "/requests/8d27b6c1-ac8a-4f29-97b0-96cef6938267/finalize",
                content_type="application/json",
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
