import requests

from flask import Blueprint, request, jsonify

from settings import URL_VOTACIONES

tables_bp = Blueprint("tables_blueprint", __name__)


@tables_bp.route("", methods=["GET"])
def get_all():
    response = requests.get(
        url="http://127.0.0.1:5001/tables",
        headers={
            "Content-Type": "application/json"
        }
    )

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({
            "messags": "se presento un error"
        })


@tables_bp.route("<string:id_tables>", methods=["GET"])
def get_by_id(id_tables):
    response = requests.get(
        url=f"{URL_VOTACIONES}/tables/{id_tables}",
        headers={
            "Content-Type": "application/json"
        }
    )

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({
            "messags": "se presento un error"
        }), 400


@tables_bp.route("", methods=["POST"])
def create():
    body = request.get_json()
    response = requests.request(
        method="POST",
        url=f"{URL_VOTACIONES}/tables",
        json=body,
        headers={
            "Content-Type": "application/json"
        }
    )
    if response.status_code == 201:
        return jsonify(response.json()), 201
    else:
        return jsonify({
            "msg": "error"
        }), 400


@tables_bp.route("<string:id_tables>", methods=["PUT"])
def update(id_tables):
    body = request.get_json()
    response = requests.request(
        method="PUT",
        url=f"{URL_VOTACIONES}/tables/{id_tables}",
        json=body,
        headers={
            "Content-Type": "application/json"
        }
    )
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({
            "msg": "error"
        }), 400


@tables_bp.route("<string:id_tables>", methods=["DELETE"])
def delete(id_tables):
    response = requests.request(
        method="DELETE",
        url=f"{URL_VOTACIONES}/tables/{id_tables}",
    )
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({
            "msg": "error"
        }), 400
