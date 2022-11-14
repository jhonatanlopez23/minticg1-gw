import requests

from flask import Blueprint, request, jsonify

from settings import URL_VOTACIONES

party_bp = Blueprint("party_blueprint", __name__)

@party_bp.route("", methods=["GET"])
def get_all():
    response = requests.get(
        url=f"{URL_VOTACIONES}/party",
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

@party_bp.route("<string:id_party>", methods=["GET"])
def get_by_id(id_party):
    response = requests.get(
        url=f"{URL_VOTACIONES}/party/{id_party}",
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


@party_bp.route("", methods=["POST"])
def create():
    body = request.get_json()
    response = requests.request(
        method="POST",
        url=f"{URL_VOTACIONES}/party",
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


@party_bp.route("<string:id_party>", methods=["PUT"])
def update(id_party):
    body = request.get_json()
    response = requests.request(
        method="PUT",
        url=f"{URL_VOTACIONES}/party/{id_party}",
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


@party_bp.route("<string:id_party>", methods=["DELETE"])
def delete(id_party):
    response = requests.request(
        method="DELETE",
        url=f"{URL_VOTACIONES}/departments/{id_party}",
    )
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({
            "msg": "error"
        }), 400
