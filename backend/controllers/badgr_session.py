from typing import Any, Dict, Optional, Tuple
from controllers.badgr_connector import BadgrConnector


class BadgrSession:
    def __init__(self, email: str, connector: BadgrConnector, member_badge_id: str):
        self.badgr_connector = connector
        self.email = email
        self.session_badges = self.load_user_badges()
        self.member_status = False
        self.membership_years = []
        self.member_badge_id = member_badge_id
        self.organize_badges()  

    def load_user_badges(self):
        return self.badgr_connector.get_by_email(self.email)

    def _extract_membership_year(self, narrative: str) -> str:
        if not narrative or 'FY' not in narrative:
            return ''
        try:
            # Handle both "FY2024" and "FY 2024" formats
            fy_text = narrative.split('FY')[1].strip()
            # Extract first number sequence
            year = ''.join(char for char in fy_text if char.isdigit())[:4]
            return str(int(year))  # 
        except (IndexError, ValueError):
            return ''

    def _create_badge_structure(self, badge: Dict[str, Any], narrative: Tuple[str, str], access_log_id: Optional[int]) -> Dict[str, Any]:
        return {
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

    def _categorize_badge(self, narrative: str) -> str:
        if "unicorn" in narrative.lower():
            return "unicornBadges"
        elif "makertech training" in narrative.lower():
            return "makertechTraining"
        elif narrative.lower() in ["power tool", "powertool"]:
            return "powertoolTraining"
        return "trainingsCompleted"

    def organize_badges(self, access_log_id=None) -> Dict[str, Any]:
        years = set()
        badge_type = {
            "unicornBadges": [], 
            "trainingsCompleted": [], 
            "powertoolTraining": [], 
            "makertechTraining": []
        }

        for badge in self.session_badges:
            if badge.get('badgeclass') == self.member_badge_id:
                self.member_status = True
                
            year = self._extract_membership_year(badge.get('narrative', ''))
            if year:
                years.add(year)

            narrative_extract = badge.get("narrative")
            if not narrative_extract:
                continue

            narrative = self._get_badge_narrative_title(narrative_extract)
            badge_structure = self._create_badge_structure(badge, narrative, access_log_id)
            category = self._categorize_badge(narrative_extract)
            badge_type[category].append(badge_structure)

        self.membership_years = sorted(list(years), reverse=True)
        return badge_type

    def _get_badge_narrative_title(self, narrative: str) -> Tuple[str, str]:
        if not narrative:
            narrative = "No description available"

        narrative = narrative.replace(":", "")
        
        if "MakerTech" in narrative:
            narrative = narrative.split("MakerTech")
        else:
            narrative = narrative.split("Makerspace")
        
        if len(narrative) > 1:
            return narrative[1], narrative[0]
        
        return narrative[0], ""

    def get_user_badges(self, access_log_id: Optional[int] = None) -> Dict[str, Any]:
        return {"isMember": self.member_status, **self.organize_badges(access_log_id)}
