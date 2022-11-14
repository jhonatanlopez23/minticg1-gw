import requests

from flask import Blueprint, request, jsonify

from settings import URL_VOTACIONES

results_bp = Blueprint("results_blueprint", __name__)


@results_bp.route("", methods=["GET"])
def get_all():
    response = requests.get(
        url=f"{URL_VOTACIONES}/results",
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


@results_bp.route("<string:id_results>", methods=["GET"])
def get_by_id(id_results):
    response = requests.get(
        url=f"{URL_VOTACIONES}/results/{id_results}",
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


@results_bp.route("", methods=["POST"])
def create():
    body = request.get_json()
    response = requests.request(
        method="POST",
        url=f"{URL_VOTACIONES}/results",
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


@results_bp.route("<string:id_results>", methods=["PUT"])
def update(id_results):
    body = request.get_json()
    response = requests.request(
        method="PUT",
        url=f"{URL_VOTACIONES}/results/{id_results}",
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


@results_bp.route("<string:id_results>", methods=["DELETE"])
def delete(id_results):
    response = requests.request(
        method="DELETE",
        url=f"{URL_VOTACIONES}/results/{id_results}",
    )
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({
            "msg": "error"
        }), 400
