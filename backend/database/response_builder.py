from typing import Any, Dict, Tuple
from database.model.models import AccessLog, User


class ResponseBuilder:
    def UserBasics(user: User, access_log: AccessLog) -> Dict[str, Any]:
        if not access_log or not user:
            return {}
        
        if access_log.IsMember:
            membership_status = "Current Member"
        elif access_log.membershipYears:
            membership_status = "Expired"
        else:
            membership_status = "Non-member"

        return {
            "Email": user.Email,
            "Name": f"{user.FirstName} {user.LastName}",
            "SignInTime": access_log.SignInTime,
            "IsMember": access_log.IsMember,
            "membershipStatus": membership_status,
            "LastSignIn": access_log.SignInTime,
            "LogID": access_log.ID,
            "AccessLogID": access_log.ID,
            "membershipYears": access_log.membershipYears
        }

    def BadgeToDatabase(badge: Dict[str, Any], log_id: int) -> Dict[str, Any]:
        return {
            "Narrative_Detail": badge.get("description"),
            "Narrative_Title": badge.get("name"),
            "CreatedAt": badge.get("createdAt"),
            "IssuedOn": badge.get("issuedOn"),
            "Revoked": badge.get("revoked"),
            "RevocationReason": badge.get("revocationReason"),
            "BadgeClass": badge.get("badgeClass"),
            "ImageURL": badge.get("image"),
            "AccessLogID": log_id,
        }
