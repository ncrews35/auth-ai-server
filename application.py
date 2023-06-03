import os
import json
# import ssl
import urllib.parse as urlparse

from src import (authenticate_user_credentials, authenticate_client,
                 generate_access_token, generate_authorization_code,
                 verify_authorization_code, verify_client_info,
                 JWT_LIFE_SPAN, CODE_LIFE_SPAN, ErrorCode, error)
from flask import Flask, redirect, render_template, request, send_from_directory
from urllib.parse import urlencode

app = Flask(__name__)


@app.route('/')
def index():
    return "The AuthAI Server"

# Favicon Setup


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/auth')
def auth():
    # Describe the access request of the client and ask user for approval
    client_id = request.args.get('client_id')
    redirect_url = request.args.get('redirect_url')
    code_challenge = request.args.get('code_challenge')

    if None in [client_id, redirect_url, code_challenge]:
        return error(ErrorCode.INVALID_REQUEST, "Missing required parameters")

    if not verify_client_info(client_id, redirect_url):
        return error(ErrorCode.INVALID_CLIENT, "Invalid client information")

    return render_template('./src/templates/AC_PKCE_grant_access.html',
                           client_id=client_id,
                           redirect_url=redirect_url,
                           code_challenge=code_challenge)


def process_redirect_url(redirect_url, authorization_code):
    # Prepare the redirect URL
    url_parts = list(urlparse.urlparse(redirect_url))
    queries = dict(urlparse.parse_qsl(url_parts[4]))
    queries.update({"authorization_code": authorization_code})
    url_parts[4] = urlencode(queries)
    url = urlparse.urlunparse(url_parts)
    return url


@app.route('/login', methods=['POST'])
def login():
    # Issues authorization code
    username = request.form.get('username')
    password = request.form.get('password')
    client_id = request.form.get('client_id')
    redirect_url = request.form.get('redirect_url')
    code_challenge = request.form.get('code_challenge')

    if None in [username, password, client_id, redirect_url, code_challenge]:
        return error(ErrorCode.INVALID_REQUEST, "Missing required parameters")

    if not verify_client_info(client_id, redirect_url):
        return error(ErrorCode.INVALID_CLIENT, "Invalid client information")

    if not authenticate_user_credentials(username, password):
        return error(ErrorCode.INVALID_GRANT, "Invalid user credentials")

    authorization_code = generate_authorization_code(client_id, redirect_url,
                                                     code_challenge)

    url = process_redirect_url(redirect_url, authorization_code)

    return redirect(url, code=303)


@app.route('/token', methods=['POST'])
def exchange_for_token():
    # Issues access token
    authorization_code = request.form.get('authorization_code')
    client_id = request.form.get('client_id')
    code_verifier = request.form.get('code_verifier')
    redirect_url = request.form.get('redirect_url')

    if None in [authorization_code, client_id, code_verifier, redirect_url]:
        return error(ErrorCode.INVALID_REQUEST, "Missing required parameters")

    if not verify_authorization_code(authorization_code, client_id, redirect_url,
                                     code_verifier):
        return error(ErrorCode.INVALID_GRANT, "Invalid authorization code")

    access_token = generate_access_token()
    return json.dumps({
        "access_token": access_token,
        "token_type": "JWT",
        "expires_in": JWT_LIFE_SPAN
    })


if __name__ == '__main__':
    # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    # context.load_cert_chain('domain.crt', 'domain.key')
    # app.run(port = 5000, debug = True, ssl_context = context)
    app.run(port=5001, debug=True)
