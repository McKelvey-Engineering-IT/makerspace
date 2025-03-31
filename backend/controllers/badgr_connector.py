from typing import Any, Dict, Optional
import requests


class BadgrConnector:
    def __init__(self, username, key, issuer=None):
        self.username = username
        self.key = key
        self.token = self.get_token()
        self.issuer = issuer if issuer else self.get_issuer()

    def get_token(self) -> str:
        token_request = requests.post(
            "https://api.badgr.io/o/token", data={"username": self.username, "password": self.key}
        )
        token_request_json = token_request.json()

        return token_request_json.get("access_token")

    def make_request(self, endpoint, reattempt=False):
        if not self.token:
            self.token = self.get_token()

            if not self.token:
                raise RuntimeError("Unable to establish connection to Badgr API")

        try:
            response = requests.get(
                "https://api.badgr.io" + endpoint,
                headers={"Authorization": "Bearer " + self.token},
            )

            if response.status_code == 401 and not reattempt:
                self.token = self.get_token()

                return self.make_request(endpoint, reattempt=True)

            response.raise_for_status()

            return response

        except requests.exceptions.RequestException as e:
            if reattempt:
                raise RuntimeError(f"Error making request to Badgr API: {e}")

    def get_issuer(self) -> str:
        issuers = self.make_request("/v2/issuers")

        return issuers.json()["result"][0]["entityId"]

    def get_issues(self) -> None:
        return self.make_request(f"/v2/issuers/{self.issuer}/assertions").json()[
            "result"
        ]

    def get_by_email(self, email: str) -> list:
        user_data = self.make_request(
            f"/v2/issuers/{self.issuer}/assertions?recipient={email}"
        )

        return user_data.json()["result"]
