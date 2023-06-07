from dotenv import load_dotenv

load_dotenv()

import os
import json
from flask import Flask, request, send_from_directory

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")

from src.auth import route

app.register_blueprint(route)


@app.route("/")
def index():
    return "The Auth AI Example Server"


@app.route("/favicon.ico")
def favicon():
    # Favicon Setup
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


if __name__ == "__main__":
    # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    # context.load_cert_chain('domain.crt', 'domain.key')
    # app.run(port = 5000, debug = True, ssl_context = context)
    app.run(host="localhost", port=5001, debug=True)
