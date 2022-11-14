import requests

from flask import Blueprint, request, jsonify

from settings import URL_VOTACIONES, URL_SECURITY
party_bp = Blueprint("party_blueprint", __name__)


@party_bp.before_request
def middleware_party():
    print("middleware_party...")


@party_bp.route("", methods=["GET"])
def get_all():
    response = requests.get(
        url=f"{URL_VOTACIONES}/party",
        headers={
            "Content-Type": "application/json"
        }
    )
    if response.status_code == 200:
        data = response.json()
        return jsonify({
            "party": data.get("party", [])
        })
    else:
        return jsonify({
            "message": "error"
        }), 400


@party_bp.route("<string:id_party>", methods=["GET"])
def get_by_id(id_party):
    response = requests.get(
        url=f"{URL_VOTACIONES}/party/{id_party}",
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


@party_bp.route("", methods=["POST"])
def create():
    body = request.get_json()
    # 1. Crear el partido
    response = requests.request(
        method="POST",
        url=f"{URL_VOTACIONES}/party",
        json={
            "name": body["name"],
            "slogan": body["slogan"],
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
        party_role = None
        for role in roles:
            if role["name"] == "Partido":
                party_role = role
                break
        party = response.json()["party"]
        if party_role:
            user_response = requests.request(
                method="POST",
                url=f"{URL_SECURITY}/users?idRole={party_role['_id']}",
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
            # 3. Asignar el usuario al partido
            assign_response = requests.request(
                method="PUT",
                url=f"{URL_VOTACIONES}/party/{party['_id']}/auth/{user['_id']}",
                headers={
                    "Content-Type": "application/json"
                }
            )
            if assign_response.status_code == 200:
                return jsonify(assign_response.json()), 201

    return jsonify({
        "msg": "Error"
    }), 400


@party_bp.route("<string:id_candidates>", methods=["PUT"])
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
            "msg": "Error"
        }), 400


@party_bp.route("<string:id_party>", methods=["DELETE"])
def delete(id_party):
    response_registrations = requests.request(
        method="DELETE",
        url=f"{URL_VOTACIONES}/party/{id_party}/delete-registrations",
        headers={
            "Content-Type": "application/json"
        }
    )
    response_party = requests.request(
        method="GET",
        url=f"{URL_VOTACIONES}/party/{id_party}",
        headers={
            "Content-Type": "application/json"
        }
    )
    if response_party.status_code == 200:
        party = response_party.json()
        if party.get("auth_id"):
            requests.request(
                method="DELETE",
                url=f"{URL_SECURITY}/users/{party['auth_id']}",
                headers={
                    "Content-Type": "application/json"
                }
            )
    if response_registrations.status_code == 200:
        response = requests.request(
            method="DELETE",
            url=f"{URL_VOTACIONES}/party/{id_party}",
            headers={
                "Content-Type": "application/json"
            }
        )
        if response.status_code == 200:
            return jsonify({
                "msg": f"el partido con id: {id_party} fue borrado",
                "registrations": response_registrations.json()
            })

    return jsonify({
        "msg": "error"
    }), 400