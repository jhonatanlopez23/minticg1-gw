from utils import clean_path
from settings import URL, PORT, URL_SECURITY, JWT_SECRET_KEY, EXCLUDED_URLS
from flask_jwt_extended import JWTManager, create_access_token, verify_jwt_in_request, get_jwt_identity
from flask import Flask, jsonify, request
import requests
import datetime
from views.votaciones import party_bp, candidates_bp, results_bp, tables_bp

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
jwt = JWTManager(app)


@app.route("/", methods=["GET"])
def ping():
    return jsonify({
        "message": "pong..."
    })


@app.route("/login", methods=["POST"])
def login():
    body = request.get_json()
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(
        url="http://localhost:8082/users/auth",
        json=body,
        headers=headers
    )

    if response.status_code == 200:
        user = response.json()
        expire = datetime.timedelta(hours=24)  # 1 dia de vencimiento
        access_token = create_access_token(
            identity=user,
            expires_delta=expire
        )
        return jsonify({
            "token": access_token,
        })
    else:
        return jsonify({
            "message": "Bad username or password"
        }), 400


def validate_permission(role_id, url, method) -> bool:

    response = requests.post(
        "http://localhost:8082/role-permission/validate/role/"+role_id,
        json={
            "url": url,
            "method": method
        }
    )
    return response.status_code == 200


@app.before_request
def middleware():
    print("middleware ppal")
    if request.path not in EXCLUDED_URLS:
        if verify_jwt_in_request():
            user = get_jwt_identity()
            role = user.get("role")
            role_id = role.get("_id")
            if not validate_permission(role_id, clean_path(request.path), request.method):
                return jsonify({
                    "msg": "Recurso no autorizado"
                }), 403


app.register_blueprint(party_bp, url_prefix="/party")
app.register_blueprint(candidates_bp, url_prefix="/candidates")
app.register_blueprint(tables_bp, url_prefix="/tables")
app.register_blueprint(results_bp, url_prefix="/results")


if __name__ == "__main__":
    app.run(
        host=URL,
        port=PORT,
        debug=True
    )
