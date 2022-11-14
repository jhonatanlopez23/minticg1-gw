import requests

from flask import Blueprint, request, jsonify

from settings import URL_VOTACIONES

candidates_bp = Blueprint("candidates_blueprint", __name__)

@candidates_bp.route("", methods=["GET"])
def get_all():
    response = requests.get(
        url=f"{URL_VOTACIONES}/candidates",
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

@candidates_bp.route("<string:id_candidates>", methods=["GET"])
def get_by_id(id_candidates):
    response = requests.get(
        url=f"{URL_VOTACIONES}/candidates/{id_candidates}",
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


@candidates_bp.route("", methods=["POST"])
def create():
    body = request.get_json()
    response = requests.request(
        method="POST",
        url=f"{URL_VOTACIONES}/candidates",
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


@candidates_bp.route("<string:id_candidates>", methods=["PUT"])
def update(id_candidates):
    body = request.get_json()
    response = requests.request(
        method="PUT",
        url=f"{URL_VOTACIONES}/candidates/{id_candidates}",
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


@candidates_bp.route("<string:id_candidates>", methods=["DELETE"])
def delete(id_candidates):
    response = requests.request(
        method="DELETE",
        url=f"{URL_VOTACIONES}/candidates/{id_candidates}",
    )
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({
            "msg": "error"
        }), 400
