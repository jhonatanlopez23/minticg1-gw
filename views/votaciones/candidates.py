import requests

from flask import Blueprint, request, jsonify

from settings import URL_VOTACIONES, URL_SECURITY

candidates_bp = Blueprint("candidates_blueprint", __name__)


@candidates_bp.before_request
def middleware_candidates():
    print("middleware_candidates...")


@candidates_bp.route("", methods=["GET"])
def get_all():
    response = requests.get(
        url=f"{URL_VOTACIONES}/candidates",
        headers={
            "Content-Type": "application/json"
        }
    )
    if response.status_code == 200:
        data = response.json()
        return jsonify({
            "candidates": data.get("candidates", [])
        })
    else:
        return jsonify({
            "message": "error"
        }), 400


@candidates_bp.route("<string:id_candidates>", methods=["GET"])
def get_by_id(id_candidates):
    response = requests.get(
        url=f"{URL_VOTACIONES}/candidates/{id_candidates}",
        headers={
            "Content-Type": "application/json"
        }
    )
    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return jsonify({
            "message": "error"
        }), 400


@candidates_bp.route("", methods=["POST"])
def create():
    body = request.get_json()
    # 1. Crear el candidato
    response = requests.request(
        method="POST",
        url=f"{URL_VOTACIONES}/candidates",
        json={
            "resolution_number": body["resolution_number"],
            "names": body["names"],
            "last_names": body["last_names"],
            "identification": body["identification"],
        },
        headers={
            "Content-Type": "application/json"
        }
    )
    if response.status_code == 201:
        # 2.1 Asignar el rol al usuario
        # 2.1.1 Consultar los roles
        roles_response = requests.request(
            method="GET",
            url=f"{URL_SECURITY}/role",
            headers={
                "Content-Type": "application/json"
            }
        )
        roles = roles_response.json() if roles_response.status_code == 200 else []
        candidates_role = None
        for role in roles:
            if role["name"] == "Candidato":
                candidates_role = role
                break
        candidate = response.json()["candidates"]
        if candidates_role:
            user_response = requests.request(
                method="POST",
                url=f"{URL_SECURITY}/users?idRole={candidates_role['_id']}",
                json={
                    "username": body["username"],
                    "email": body["email"],
                    "password": body["password"]
                },
                headers={
                    "Content-Type": "application/json"
                }
            )
        else:
            user_response = requests.request(
                method="POST",
                url=f"{URL_SECURITY}/users",
                json={
                    "username": body["username"],
                    "email": body["email"],
                    "password": body["password"]
                },
                headers={
                    "Content-Type": "application/json"
                }
            )
        if user_response.status_code < 300:
            user = user_response.json()
            # 3. Asignar el usuario al candidato
            assign_response = requests.request(
                method="PUT",
                url=f"{URL_VOTACIONES}/candidates/{candidate['_id']}/auth/{user['_id']}",
                headers={
                    "Content-Type": "application/json"
                }
            )
            if assign_response.status_code == 200:
                return jsonify(assign_response.json()), 201

    return jsonify({
        "msg": "Error"
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
            "msg": "Error"
        }), 400


@candidates_bp.route("<string:id_candidates>", methods=["DELETE"])
def delete(id_candidates):
    response_registrations = requests.request(
        method="DELETE",
        url=f"{URL_VOTACIONES}/candidates/{id_candidates}/delete-registrations",
        headers={
            "Content-Type": "application/json"
        }
    )
    response_candidate = requests.request(
        method="GET",
        url=f"{URL_VOTACIONES}/candidates/{id_candidates}",
        headers={
            "Content-Type": "application/json"
        }
    )
    if response_candidate.status_code == 200:
        candidate = response_candidate.json()
        if candidate.get("auth_id"):
            requests.request(
                method="DELETE",
                url=f"{URL_SECURITY}/users/{candidate['auth_id']}",
                headers={
                    "Content-Type": "application/json"
                }
            )
    if response_registrations.status_code == 200:
        response = requests.request(
            method="DELETE",
            url=f"{URL_VOTACIONES}/candidates/{id_candidates}",
            headers={
                "Content-Type": "application/json"
            }
        )
        if response.status_code == 200:
            return jsonify({
                "msg": f"el candidato con id: {id_candidates} fue borrado",
                "registrations": response_registrations.json()
            })

    return jsonify({
        "msg": "error"
    }), 400
