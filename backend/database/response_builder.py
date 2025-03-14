from typing import Any, Dict
from database.model.models import AccessLog, User


class ResponseBuilder:
    def UserBasics(user: User, access_log: AccessLog) -> Dict[str, Any]:
        if not access_log or not user:
            return {}

        return {
            "Email": user.Email,
            "Name": f"{user.FirstName} {user.LastName}",
            "SignInTime": access_log.SignInTime,
            "IsMember": access_log.IsMember,
            "LastSignIn": access_log.SignInTime,
            "LogID": access_log.ID,
        }
