from flask import Blueprint, jsonify, request

from sqlalchemy import exc

from project.api.models import Request
from project import db

test_blueprint = Blueprint("tasks", __name__)


@test_blueprint.route("/api/requests", methods=["GET"])
def get_all_request():
    response = {
        "status": "success",
        "data": {"tasks": [request.to_json() for request in Request.query.all()]},
    }
    return jsonify(response), 200
