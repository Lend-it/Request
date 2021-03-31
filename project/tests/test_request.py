import json
import unittest

from project.tests.base import BaseTestCase
from database_singleton import Singleton

from project.api.models import Request

db = Singleton().database_connection()


def add_request(
    productname, startdate, enddate, description, requester, productcategoryid
):
    lender = None

    request = Request(
        productname,
        startdate,
        enddate,
        description,
        requester,
        lender,
        productcategoryid,
    )

    db.session.add(request)
    db.session.commit()
    return request


class TestRequest(BaseTestCase):
    def test_get_all_requests(self):
        add_request(
            "Banco Imobiliario",
            "2020-09-12 00:00:00.000",
            "2020-09-30 00:00:00.000",
            "Queria um banco imobiliário emprestado para jogar com meus amigos neste fim de semana!",
            "matheus@email.com",
            3,
        )
        add_request(
            "Jogo da vida",
            "2020-09-12 00:00:00.000",
            "2020-09-30 00:00:00.000",
            "Queria um jogo da vida emprestado para jogar com meus amigos neste fim de semana!",
            "matheus@email.com",
            3,
        )
        add_request(
            "War",
            "2020-09-12 00:00:00.000",
            "2020-09-30 00:00:00.000",
            "Queria um war emprestado para jogar com meus amigos neste fim de semana!",
            "matheus@email.com",
            3,
        )

        with self.client:
            response = self.client.get("/requests")
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn("success", data["status"])

            self.assertIn(
                "Banco Imobiliario", data["data"]["requests"][0]["productname"]
            )
            self.assertIn("Jogo da vida", data["data"]["requests"][1]["productname"])
            self.assertIn("War", data["data"]["requests"][2]["productname"])
