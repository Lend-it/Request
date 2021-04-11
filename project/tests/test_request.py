import json
import unittest
from project.tests.base import BaseTestCase
from project.api.models import Request
from project.api.models import db
from project.tests.utils import add_request, add_category


FAKE_EMAIL = "tah_tu@email.com"
FAKE_DESCRIPTION = (
    "Queria um Uno emprestado para jogar com meus amigos neste fim de semana!"
)
FAKE_ENDDATE = "2020-09-30 00:00:00.000"
FAKE_STARTDATE = "2020-09-12 00:00:00.000"
FAKE_REQUESTER = "matheus@email.com"
REQUEST_BASE_URL = "/requests"


class TestRequest(BaseTestCase):
    def test_create_request(self):
        add_category("Eletrodomésticos")
        with self.client:
            response = self.client.post(
                REQUEST_BASE_URL,
                data=json.dumps(
                    {
                        "productname": "Batedeira",
                        "startdate": FAKE_STARTDATE,
                        "enddate": FAKE_ENDDATE,
                        "description": "Preciso de uma batedeira para fazer meu bolo de aniversario.",
                        "requester": "tah_tu@gmail.com",
                        "productcategoryid": 1,
                        "lender": None,
                    }
                ),
                content_type="application/json",
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)
            self.assertIn("success", data["status"])

    def test_create_request_invalid_json(self):
        with self.client:
            response = self.client.post(
                REQUEST_BASE_URL,
                data=json.dumps({}),
                content_type="application/json",
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid payload.", data["message"])
            self.assertIn("fail", data["status"])

    def test_get_all_requests(self):
        add_category("Eletrodomésticos")
        add_request(
            "Banco Imobiliario",
            FAKE_STARTDATE,
            FAKE_ENDDATE,
            "Queria um banco imobiliário emprestado para jogar com meus amigos neste fim de semana!",
            FAKE_REQUESTER,
            1,
        )
        add_request(
            "Jogo da vida",
            FAKE_STARTDATE,
            FAKE_ENDDATE,
            "Queria um jogo da vida emprestado para jogar com meus amigos neste fim de semana!",
            FAKE_REQUESTER,
            1,
        )
        add_request(
            "War",
            FAKE_STARTDATE,
            FAKE_ENDDATE,
            "Queria um war emprestado para jogar com meus amigos neste fim de semana!",
            FAKE_REQUESTER,
            1,
        )

        with self.client:
            response = self.client.get(REQUEST_BASE_URL)
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn("success", data["status"])

            self.assertEqual(len(data["data"]["requests"]), 3)

    def test_get_all_requests_requester(self):
        add_category("Eletrodomésticos")
        add_request(
            "Jogo da vida",
            FAKE_STARTDATE,
            FAKE_ENDDATE,
            "Queria um jogo da vida emprestado para jogar com meus amigos neste fim de semana!",
            FAKE_REQUESTER,
            1,
        )
        add_request(
            "War",
            FAKE_STARTDATE,
            FAKE_ENDDATE,
            "Queria um war emprestado para jogar com meus amigos neste fim de semana!",
            "jose@email.com",
            1,
        )

        with self.client:
            response = self.client.get(
                f"{REQUEST_BASE_URL}?requester=matheus@email.com"
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn("success", data["status"])

            self.assertEqual(len(data["data"]["requests"]), 1)

    def test_get_all_requests_lender(self):
        add_category("Eletrodomésticos")
        add_request(
            "Jogo da vida",
            FAKE_STARTDATE,
            FAKE_ENDDATE,
            "Queria um jogo da vida emprestado para jogar com meus amigos neste fim de semana!",
            FAKE_REQUESTER,
            1,
            lender="jose@email.com",
        )
        add_request(
            "War",
            FAKE_STARTDATE,
            FAKE_ENDDATE,
            "Queria um war emprestado para jogar com meus amigos neste fim de semana!",
            "jose@email.com",
            1,
            lender="juca@email.com",
        )

        with self.client:
            response = self.client.get(f"{REQUEST_BASE_URL}?lender=juca@email.com")
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn("success", data["status"])

            self.assertEqual(len(data["data"]["requests"]), 1)

    def test_get_filtered_requests(self):
        add_category("Eletrodomésticos")
        add_request(
            "Jogo da vida",
            FAKE_STARTDATE,
            FAKE_ENDDATE,
            "Queria um jogo da vida emprestado para jogar com meus amigos neste fim de semana!",
            FAKE_REQUESTER,
            1,
        )
        add_request(
            "War",
            FAKE_STARTDATE,
            FAKE_ENDDATE,
            "Queria um war emprestado para jogar com meus amigos neste fim de semana!",
            FAKE_REQUESTER,
            1,
        )

        with self.client:
            response = self.client.get(f"{REQUEST_BASE_URL}/1")
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn("success", data["status"])

            self.assertIn("Jogo da vida", data["data"]["requests"][0]["productname"])
            self.assertIn("War", data["data"]["requests"][1]["productname"])

    def test_update_lender_request(self):
        add_category("Eletrodomésticos")
        product = add_request(
            "Banco Imobiliario",
            FAKE_STARTDATE,
            FAKE_ENDDATE,
            "Queria um banco imobiliário emprestado para jogar com meus amigos neste fim de semana!",
            FAKE_REQUESTER,
            1,
        )

        with self.client:
            response = self.client.patch(
                f"{REQUEST_BASE_URL}/{product.requestid}",
                data=json.dumps({"lender": "maia@email.com"}),
                content_type="application/json",
            )

            data = json.loads(response.data.decode())
            self.assertIn("maia@email.com", data["request"]["lender"])

    def test_cannot_update_non_existing_request_lender(self):
        with self.client:
            response = self.client.patch(
                f"{REQUEST_BASE_URL}/8d27b6c1-ac8a-4f29-97b0-96cef6938267",
                data=json.dumps({"lender": "maia@email.com"}),
                content_type="application/json",
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)

    def test_finalize_request(self):
        add_category("Eletrodomésticos")
        product = add_request(
            "Banco Imobiliario",
            FAKE_STARTDATE,
            FAKE_ENDDATE,
            "Queria um banco imobiliário emprestado para jogar com meus amigos neste fim de semana!",
            FAKE_REQUESTER,
            1,
        )

        with self.client:
            response = self.client.patch(
                f"{REQUEST_BASE_URL}/{product.requestid}/finalize",
                content_type="application/json",
            )

            data = json.loads(response.data.decode())
            self.assertEqual(data["request"]["finalized"], True)

    def test_cannot_finalize_non_existing_request(self):
        with self.client:
            response = self.client.patch(
                f"{REQUEST_BASE_URL}/8d27b6c1-ac8a-4f29-97b0-96cef6938267/finalize",
                content_type="application/json",
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Request not found")

    def test_edit_request(self):
        add_category("Eletrodomésticos")
        request = add_request(
            "Uno",
            FAKE_STARTDATE,
            FAKE_ENDDATE,
            FAKE_DESCRIPTION,
            FAKE_EMAIL,
            1,
        )

        with self.client:
            response = self.client.put(
                f"{REQUEST_BASE_URL}/{request.requestid}",
                data=json.dumps(
                    {
                        "productname": "Uno",
                        "startdate": FAKE_STARTDATE,
                        "enddate": FAKE_ENDDATE,
                        "description": FAKE_DESCRIPTION,
                        "requester": FAKE_EMAIL,
                        "productcategoryid": 1,
                        "lender": None,
                    }
                ),
                content_type="application/json",
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)
            self.assertIn("Update completed!", data["data"]["update_status"])
            self.assertIn("success", data["status"])

    def test_edit_request_inexistent_id(self):
        with self.client:
            response = self.client.put(f"{REQUEST_BASE_URL}/8783472")
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 404)
            self.assertIn("fail", data["status"])
            self.assertIn("Invalid payload.", data["message"])

    def test_delete_request(self):
        add_category("Eletrodomésticos")
        request = add_request(
            "Uno",
            FAKE_STARTDATE,
            FAKE_ENDDATE,
            FAKE_DESCRIPTION,
            FAKE_EMAIL,
            1,
        )

        with self.client:
            response = self.client.delete(f"{REQUEST_BASE_URL}/{request.requestid}")

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn("Request deleted!", data["data"]["message"])
            self.assertIn("success", data["status"])

    def test_delete_request_inexistent_id(self):
        with self.client:
            response = self.client.delete(
                f"{REQUEST_BASE_URL}/8d27b6c1-ac8a-4f29-97b0-96cef6938267"
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 404)
            self.assertIn("fail", data["status"])
            self.assertIn("Could not found request to delete.", data["message"])
