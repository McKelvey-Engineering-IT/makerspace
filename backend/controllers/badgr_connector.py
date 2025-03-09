from typing import Any, Dict
import requests


class BadgrConnector:
    def __init__(self, username, key):
        self.token = self.get_token(username, key)
        self.issuer = self.get_issuer()

    def get_issuer(self) -> str:
        if not self.token:
            raise RuntimeError("No token established")

        issuers = self.make_request("/v2/issuers")

        return issuers.json()["result"][0]["entityId"]

    def get_token(self, username: str, key: str) -> str:
        token_request = requests.post(
            "https://api.badgr.io/o/token", data={"username": username, "password": key}
        )
        token_request_json = token_request.json()

        return token_request_json.get("access_token")

    def make_request(self, endpoint):
        return requests.get(
            "https://api.badgr.io" + endpoint,
            headers={"Authorization": "Bearer " + self.token},
        )

    def get_badges(self, email: str) -> list:
        assertions = self.make_request(f"/v2/issuers/{self.issuer}/assertions")
        assertions_data = assertions.json()["result"]

        return [
            badge
            for badge in assertions_data
            if badge["recipient"]["plaintextIdentity"] == email
        ]

    def organize_badges(self, login_badges: list) -> Dict[str, Any]:
        badge_type = {"unicornBadges": [], "trainingsCompleted": []}

        for badge in login_badges:
            badge_name = badge["narrative"].split(":")[-1].strip()

            if "unicorn" in badge_name.lower():
                badge_type["unicornBadges"].append(
                    {"name": badge_name, "image": badge["image"]}
                )
            else:
                badge_type["trainingsCompleted"].append(
                    {"name": badge_name, "image": badge["image"]}
                )

        return badge_type

    def get_user(self, email: str) -> Dict[str, Any]:
        badges = self.get_badges(email)
        response = {"email": email, "isMember": False, **self.organize_badges(badges)}

        if badges:
            response.update(
                {
                    "name": badges[0]["extensions"]["extensions:recipientProfile"][
                        "name"
                    ],
                    "isMember": True,
                }
            )
        else:
            response.update({"name": "Unregistered"})

        return response
