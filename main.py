from flask import Flask, jsonify
from settings import URL, PORT
app = Flask(__name__)


@app.route('/', methods=["GET"])
def ping():
    return jsonify({
        "message": "pong.."
    })


if (__name__ == "__main__"):
    app.run(
        host=URL,
        port=PORT,
        debug=True
    )
