from typing import Any, Dict, Optional, Tuple
from controllers.badgr_connector import BadgrConnector


class BadgrSession:
    def __init__(self, email: str, badgr_connector: BadgrConnector, membership_id: Optional[str] = None):
        self.badgr_connector = badgr_connector
        self.email = email
        self.session_badges = self.load_user_badges()
        self.member_status = self.get_member_status(membership_id)

    def load_user_badges(self):
        return self.badgr_connector.get_by_email(self.email)

    def get_member_status(self, membership_id: Optional[str] = None) -> bool:
        if membership_id is None:
            return False
        
        return membership_id in [badge["badgeclass"] for badge in self.session_badges]

    def organize_badges(self, access_log_id=None) -> Dict[str, Any]:
        def get_badge_narrative_title(narrative: str) -> Tuple[str, str]:
            if not narrative:
                narrative = "No description available"

            narrative = narrative.replace(":", "").split("Makerspace")
            
            if len(narrative) > 1:
                return narrative[1], narrative[0]
            
            return narrative[0], ""

        badge_type = {"unicornBadges": [], "trainingsCompleted": [], "powertoolTraining": [], "makertechTraining": []}

        for badge in self.session_badges:
            narrative_extract = badge.get("narrative")

            if not narrative_extract:
                continue
            
            narrative = get_badge_narrative_title(narrative_extract)

            badge_structure = {
                "Narrative_Title": narrative[1],
                "Narrative_Detail": narrative[0],
                "CreatedAt": badge.get("createdAt"),
                "IssuedOn": badge.get("issuedOn"),
                "Revoked": badge.get("revoked"),
                "Revocation_Reason": badge.get("revocationReason"),
                "BadgeClass": badge.get("badgeclass"),
                "ImageURL": badge.get("image"),
                "AccessLogID": access_log_id,
            }

            if "unicorn" in narrative_extract.lower():
                badge_type["unicornBadges"].append(badge_structure)
            elif "makertech training" in narrative_extract.lower():
                badge_type['makertechTraining'].append(badge_structure)
            elif "powertool" in narrative_extract.lower():
                badge_type['powertoolTraining'].append(badge_structure)
            else:            
                badge_type["trainingsCompleted"].append(badge_structure)

        return badge_type

    def get_user_badges(self, access_log_id: Optional[int] = None) -> Dict[str, Any]:
        return {"isMember": self.member_status, **self.organize_badges(access_log_id)}
