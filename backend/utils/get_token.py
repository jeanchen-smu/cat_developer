from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session
import sys

client_id = "11e9b41c833d7182a8ca8907a6eb71"
client_secret = "2ed790a1e9abbd059051e0144f8946"
token_url = "https://sg.baseride.com/oauth2/token"


def get_access_token(username="AXA_trial", password="@xatri@l1234"):
    oauth = OAuth2Session(
        client=LegacyApplicationClient(client_id=client_id)
    )
    token = oauth.fetch_token(
        token_url=token_url,
        username=username,
        password=password,
        client_id=client_id,
        client_secret=client_secret
    )

    return token["access_token"]


if __name__ == "__main__":
    if len(sys.argv) == 3:
        print get_access_token(sys.argv[1], sys.argv[2])
    else:
        print get_access_token()
