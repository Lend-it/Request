from flask import Blueprint, jsonify, request

from sqlalchemy import exc

from project.api.models import Request
from project.api.models import Category
from database_singleton import Singleton

db = Singleton().database_connection()

category_blueprint = Blueprint("categories", __name__)


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
        db.session.rollback()
        return jsonify(error_response), 400
