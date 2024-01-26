from flask import redirect, request, render_template, session, abort, Flask
import requests
from urllib.parse import urlencode
import jwt
import json

app = Flask(__name__)

CLIENT_SECRET = "YOUR_CLIENT_SECRET"

testAuthEndpoint = "https://eid2.oesterreich.gv.at/auth/idp/profile/oidc/authorize"
testTokenEndpoint = "https://eid2.oesterreich.gv.at/auth/idp/profile/oidc/token"

args3 = {
    "scope": "openid profile eid",
    "redirect_uri": "https://eidtest.entarc.eu/authpoint",
    "client_id": "https://eid.entarc.eu",
    "response_type" : "code",
    "state": "123498736"
}
print(testAuthEndpoint + "?" + urlencode(args3))

@app.route('/authpoint')
def authpoint():
    print(request.args.get("code"))

    payl = {
        "code" : request.args.get("code"),
        "grant_type" : "authorization_code",
        "client_secret" : CLIENT_SECRET,
        "redirect_uri" : "https://eidtest.entarc.eu/authpoint",
        "client_id" : "https://eid.entarc.eu"
    }

    print(str(payl))

    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

    response = requests.post(testTokenEndpoint, headers=headers, data=payl)

    dt = json.loads(response.content.decode("utf-8"))

    decoded = jwt.decode(dt["id_token"], options={"verify_signature": False})

    return render_template("authpoint.html",
                           family_name = decoded["family_name"],
                           given_name = decoded["given_name"],
                           response = decoded)

@app.route('/')
def index():

    args = {
        "scope": "openid profile",
        "redirect_uris": ["https://eidtest.entarc.eu/authpoint"],
        "client_id": "https://eid.entarc.eu",
        "client_secret": CLIENT_SECRET,
        "token_endpoint_auth_method": "client_secret_post",
        "response_types": ["code", "id_token"],
        "grant_types": "authorization_code"
    }

    args2 = {
        "scope": "openid profile eid",
        "redirect_uri": "https://eidtest.entarc.eu/authpoint",
        "client_id": "https://eid.entarc.eu",
        "response_type" : "code",
        "state": "123498736"
    }

    print(testAuthEndpoint + "?" + urlencode(args2))

    return render_template("index.html", redirectUrl = testAuthEndpoint + "?" + urlencode(args2))

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5001)
