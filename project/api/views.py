from flask import Blueprint, jsonify, request
from sqlalchemy import exc
from project.api.models import Request
from project.api.models import db
from project.api.models import Category
from project.api.utils import get_category_name


category_blueprint = Blueprint("categories", __name__)
request_blueprint = Blueprint("requests", __name__)


@category_blueprint.route("/product_category", methods=["GET"])
def get_all_categories():
    response = {
        "status": "success",
        "data": {
            "categories": [category.to_json() for category in Category.query.all()]
        },
    }
    return jsonify(response), 200


@category_blueprint.route("/product_category", methods=["POST"])
def add_categories():
    post_data = request.get_json()

    error_response = {"status": "fail", "message": "Invalid payload."}

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
        response = {
            "status": "fail",
            "data": {
                "status": "Could not create Category",
            },
        }
        db.session.rollback()
        return jsonify(response), 400


@request_blueprint.route("/requests", methods=["GET"])
def get_all_request():
    requests = get_category_name([request.to_json() for request in Request.query.all()])
    response = {
        "status": "success",
        "data": {"requests": requests},
    }
    return jsonify(response), 200


@request_blueprint.route("/requests/<productcategoryid>", methods=["GET"])
def get_filtered_request(productcategoryid):
    requests = get_category_name(
        [
            request.to_json()
            for request in Request.query.filter_by(
                productcategoryid=productcategoryid
            ).all()
        ]
    )

    response = {
        "status": "success",
        "data": {"requests": requests},
    }
    return jsonify(response), 200


@request_blueprint.route("/requests", methods=["POST"])
def create_request():
    post_data = request.get_json()

    error_response = {"status": "fail", "message": "Invalid payload."}

    if not post_data:
        return jsonify(error_response), 400

    productname = post_data.get("productname")
    startdate = post_data.get("startdate")
    enddate = post_data.get("enddate")
    description = post_data.get("description")
    requester = post_data.get("requester")
    productcategoryid = post_data.get("productcategoryid")
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


@request_blueprint.route("/requests/<requestid>", methods=["PATCH"])
def update_request_lender(requestid):
    post_data = request.get_json()

    error_response = {"status": "fail", "message": "Request not found"}

    lender = post_data.get("lender")

    product = Request.query.filter_by(requestid=requestid).first()

    if not product:
        return jsonify(error_response), 404

    product.lender = lender
    db.session.commit()

    response = {"status": "success", "request": product.to_json()}

    return jsonify(response), 200


@request_blueprint.route("/requests/<requestid>/finalize", methods=["PATCH"])
def finalize_request(requestid):
    error_response = {"status": "fail", "message": "Request not found"}

    product = Request.query.filter_by(requestid=requestid).first()

    if not product:
        return jsonify(error_response), 404

    product.finalized = True
    db.session.commit()

    response = {"status": "success", "request": product.to_json()}

    return jsonify(response), 200


@request_blueprint.route("/requests/<requestid>", methods=["PUT"])
def edit_request(requestid):

    put_data = request.get_json()
    error_response = {"status": "fail", "message": "Invalid payload."}

    if not put_data:
        return jsonify(error_response), 404

    request_obj = Request.query.filter_by(requestid=requestid).first()

    productname = put_data.get("productname")
    startdate = put_data.get("startdate")
    enddate = put_data.get("enddate")
    description = put_data.get("description")
    productcategoryid = put_data.get("productcategoryid")

    request_obj.productname = productname
    request_obj.startdate = startdate
    request_obj.enddate = enddate
    request_obj.description = description
    request_obj.productcategoryid = productcategoryid

    try:
        db.session.merge(request_obj)
        db.session.commit()

        response = {
            "status": "success",
            "data": {
                "update_status": "Update completed!",
            },
        }

        return jsonify(response), 201
    except exc.IntegrityError:
        response = {
            "status": "fail",
            "data": {
                "update_status": "Could not update Request",
            },
        }
        db.session.rollback()
        return jsonify(response), 400


@request_blueprint.route("/requests/<requestid>", methods=["DELETE"])
def delete_request(requestid):
    request = Request.query.filter_by(requestid=requestid).first()

    error_response = {"status": "fail", "message": "Could not found request to delete."}

    if not request:
        return jsonify(error_response), 404
    try:
        db.session.delete(request)
        db.session.commit()

        response = {"status": "success", "data": {"message": "Request deleted!"}}

        return jsonify(response), 200
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(error_response), 400
