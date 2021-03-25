from flask import Blueprint, jsonify, request

from sqlalchemy import exc, update

from project.api.models import Request
from project.api.models import Category
from database_singleton import Singleton

db = Singleton().database_connection()

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


@request_blueprint.route("/edit_request/<requestid>", methods=["PUT"])
def edit_request(requestid):
    try:
        put_data = request.get_json()
        request_obj = Request.query.filter_by(requestid=requestid).first()
        old_obj = request_obj.to_json()

        productname = put_data.get("productname")
        request_obj.productname = productname

        startdate = put_data.get("startdate")
        request_obj.startdate = startdate

        enddate = put_data.get("enddate")
        request_obj.enddate = enddate

        description = put_data.get("description")
        request_obj.description = description

        productcategoryid = put_data.get("productcategoryid")
        request_obj.productcategoryid = productcategoryid

        response = {
            "status": "success",
            "data": {
                "update_status": "Update completed!",
                "old_obj": old_obj,
                "after_change": request_obj.to_json(),
            },
        }

        return jsonify(response), 200
    except Exception as err:
        response = {
            "status": "fail",
            "data": {
                "update_status": "Update not complete!",
                "error_msg": err.to_json(),
            },
        }
        db.session.rollback()
        return jsonify(response), 400
