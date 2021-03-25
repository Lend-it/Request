from flask import Blueprint, jsonify, request

from sqlalchemy import exc

from project.api.models import Request
from project.api.models import Category
from database_singleton import Singleton
from project.api.models import  db

category_blueprint = Blueprint("categories", __name__)
request_blueprint = Blueprint("requests", __name__)


@category_blueprint.route("/product_category", methods=["GET"])
def get_all_request():
    response = {
        "status": "success",
        "data": {
            "categories": [category.to_json() for category in Category.query.all()]
        },
    }
    return jsonify(response), 200


@category_blueprint.route("/product_category", methods=["POST"])
def add_categories():
    if not post_data:
        return jsonify(error_response), 400

    name = post_data.get("name")

    try:
        db.session.add(Category(name))
        db.session.commit()

        response = {
            "status": "success",
            "data": {"message": f"Category {name} was created!"},
        }

        return jsonify(response), 201
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(error_response), 400


@request_blueprint.route("/requests", methods=["POST"])
def create_request():
    post_data = request.get_json()

    error_response = {"status": "fail", "message": "Invalid payload."}

    productname = (post_data.get("productname"),)
    startdate = (post_data.get("startdate"),)
    enddate = (post_data.get("enddate"),)
    description = (post_data.get("description"),)
    requester = (post_data.get("requester"),)
    productcategoryid = (post_data.get("productcategoryid"),)
    lender = None

    lending_request = Request(
        productname,
        startdate,
        enddate,
        description,
        requester,
        lender,
        productcategoryid,
    )

    try:
        db.session.add(lending_request)
        db.session.commit()

        response = {"status": "success", "data": {"request": lending_request.to_json()}}

        return jsonify(response), 201
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(error_response), 400


@request_blueprint.route("/requests/<requestid>", methods=["DELETE"])
def delete_request(requestid):
    product = Request.query.filter_by(requestid=requestid).first()
    db.session.delete(product)
    db.session.commit()

    response = {"status": "success", "data": {"message": "Product deleted!"}}

    return jsonify(response), 200
