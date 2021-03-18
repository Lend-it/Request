from flask import Blueprint, jsonify, request

from sqlalchemy import exc

from project.api.models import Request
from project.api.models import Category
from project import db

category_blueprint = Blueprint("categories", __name__)


@category_blueprint.route("/api/product_category", methods=["GET"])
def get_all_request():
    response = {
        "status": "success",
        "data": {"categories": [request.to_json() for request in Category.query.all()]},
    }
    return jsonify(response), 200
