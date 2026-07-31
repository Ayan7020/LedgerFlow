from google.oauth2 import id_token
from google.auth.transport import requests


class AuthService:
    def __init__(self,GOOGLE_CLIENT_ID: str):
        self._GOOGLE_CLIENT_ID = GOOGLE_CLIENT_ID

    def auth_google(self,token: str):
        try:
            self._verify_google_token(token)
            print("DONE")
        except Exception as E:
            print("NOT DONE: ",type(E))
            print(E)

    def _verify_google_token(self,token: str):
        id_info = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            self._GOOGLE_CLIENT_ID
        )

        return id_info