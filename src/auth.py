import os
import requests
import flask
import base64
import re
import hashlib
from collections import namedtuple
from urllib.parse import urljoin, urlencode, urlparse, urlunparse

route = flask.Blueprint("auth_route", __name__)

CLIENT_ID = os.environ.get("AUTHAI_CLIENT_ID")
CLIENT_SECRET = os.environ.get("AUTHAI_CLIENT_SECRET")

SCOPES = [
    "https://bujn864x17.execute-api.us-east-1.amazonaws.com/staging/read:key",
    "openid",
]

RETURN_URI = os.getenv("RETURN_URI")


@route.route("/authorize")
def authorize():
    Components = namedtuple(
        typename="Components",
        field_names=["scheme", "netloc", "url", "path", "query", "fragment"],
    )

    redirect_uri = flask.url_for("auth_route.oauth2callback", _external=True)

    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode("utf-8")
    code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)

    flask.session["code_verifier"] = code_verifier

    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
    code_challenge = code_challenge.replace("=", "")

    query_params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "redirect_uri": redirect_uri,
        "code_challenge_method": "S256",
        "code_challenge": code_challenge,
    }

    url = urlunparse(
        Components(
            scheme="https",
            netloc="authai-staging.auth.us-east-1.amazoncognito.com",
            query=urlencode(query_params),
            path="",
            url="oauth2/authorize",
            fragment="",
        )
    )

    print(url)

    return flask.redirect(url)


@route.route("/oauth2callback", endpoint="oauth2callback")
def oauth2callback():
    error = flask.request.args.get("error", default=None, type=str)
    if error:
        print(f"There was an error: {error}")
        raise Exception(error)

    print(flask.request.args)

    code = flask.request.args.get("code", default=None, type=str)
    redirect_uri = flask.url_for("auth_route.oauth2callback", _external=True)

    code_verifier = flask.session["code_verifier"]

    print(code)

    query_params = {
        "grant_type": "authorization_code",
        "code": code,
        "code_verifier": "1234567890",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": " ".join(SCOPES),
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier,
    }

    url = urljoin(
        "https://authai-staging.auth.us-east-1.amazoncognito.com", "oauth2/token"
    )

    r = requests.post(url, data=query_params)
    body = r.json()

    return body


@route.route("/revoke")
def revoke():
    pass


@route.route("/clear")
def clear_credentials():
    if "credentials" in flask.session:
        del flask.session["credentials"]

    return "Credentials have been cleared.<br><br>"


def credentials_to_dict(access_token):
    return {"access_token": access_token}
