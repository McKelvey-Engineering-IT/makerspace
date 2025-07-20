import re
from typing import Any, Dict, Optional, Tuple, List
from controllers.badgr_connector import BadgrConnector
from datetime import datetime
from config import BADGE_LEVELS

class BadgeUtility:
    @staticmethod
    def extract_year_ay_format(text: str) -> str:
        """
        Extracts the end year (new academic year) from AY formats like 'AY25-26'
        Returns '2026'
        """
        match = re.search(r'AY\s?(\d{2})-(\d{2})', text)
        if not match:
            return ''
        start, end = match.groups()
        base_century = 2000        
        
        return str(base_century + int(end))

    @staticmethod
    def extract_year_fy_format(text: str) -> str:
        """
        Extracts fiscal year from FY formats like 'FY2024'
        Returns '2024'
        """
        match = re.search(r'FY\s?(\d{4})', text)
        if not match:
            return ''
        return match.group(1)
    
    @staticmethod
    def extract_membership_year(narrative: str) -> str:
        if not narrative or ('FY' not in narrative and 'AY' not in narrative):
            return ''
        
        try:
            if 'AY' in narrative:
                return BadgeUtility.extract_year_ay_format(narrative)
            elif 'FY' in narrative:
                return BadgeUtility.extract_year_fy_format(narrative)
        except Exception:
            return ''
        
    @staticmethod
    def create_badge_structure(badge: Dict[str, Any], narrative: Tuple[str, str], access_log_id: Optional[int]) -> Dict[str, Any]:
        return {
            "Narrative_Title": narrative[0],
            "Narrative_Detail": narrative[1],
            "CreatedAt": badge.get("createdAt") or badge.get('CreatedAt'),
            "IssuedOn": badge.get("issuedOn") or badge.get('IssuedOn'),
            "Revoked": badge.get("revoked") or badge.get('Revoked'),
            "Revocation_Reason": badge.get("revocationReason") or badge.get('Revocation_Reason'),
            "BadgeClass": badge.get("badgeclass") or badge.get('BadgeClass'),
            "ImageURL": badge.get("image") or badge.get('ImageURL'),
            "AccessLogID": access_log_id,
        }
    
    @staticmethod
    def categorize_badge(narrative: str) -> str:
        narrative = narrative.lower().strip()

        for level, config in BADGE_LEVELS.items():
            if narrative in [term.lower() for term in config["terms"]]:
                return level
                
        return "White Level"
    
    @staticmethod
    def get_badge_narrative_title(narrative: str) -> Tuple[str, str]:
        if not narrative:
            narrative = "No description available"

        narrative = narrative.replace(":", "").split("Makerspace")
        
        if len(narrative) > 1:
            return narrative[1], narrative[0]
        
        return narrative[0], ""
    
class BadgrSession:
    def __init__(self, email: str, connector: BadgrConnector, badge_snapshot: Optional[dict] = None, preprocess: Optional[bool] = False):
        self.badgr_connector = connector
        self.email = email
        self.session_badges = badge_snapshot or self._load_badges_from_api()
        self.member_status = False
        self.membership_years = []

        if preprocess:
            self.process_badges_and_status()

    def _load_badges_from_api(self) -> List[Dict[str, Any]]:
        """
        Load badges from Badgr API using the provided email.
        Returns a list of badge dictionaries.
        """
        return self.badgr_connector.get_by_email(self.email)

    def _generate_string_membership_status(self) -> str:
        """
        Determines detailed membership status:
        - "Current Member": Has current year's orientation
        - "Expired": Has past orientation but not current
        - "Non-member": Never had orientation
        """
        if self._determine_membership():
            return "Current Member"
        elif self.membership_years:
            return "Expired"
        return "Non-member"

    def _determine_membership(self) -> bool:
        """
        Determines if user is a current member based on system date:
        Aug-Dec: Check against next year's membership
        Jan-Jul: Check against current year's membership
        """
        current_date = datetime.now()
        check_year = current_date.year
        
        if current_date.month >= 7:
            check_year += 1

        return str(check_year) in self.membership_years

    def generate_response_format(self, session_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Generates a UI-formatted response with badges categorized by levels.
        Returns a dictionary with badge levels and their respective badges.
        """
        return {
            "badges": self.process_badges_and_status(session_id),
            "member_status": self._generate_string_membership_status(),
            "membership_years": self.membership_years
        }

    def process_badges_and_status(self, access_log_id=None) -> List[Dict[str, Any]]:
        levels = {level: [] for level in BADGE_LEVELS.keys() | {"White Level"}}
        years = set()
        level_narratives = {level: set() for level in levels.keys()}  # Track narratives per level

        for badge in self.session_badges:
            year = BadgeUtility.extract_membership_year(badge.get('narrative', ''))

            if year:
                years.add(year)

            narrative_extract = badge.get('narrative') or badge.get('Narrative_Title', '')
            
            if not narrative_extract or "makertech" in narrative_extract.lower():
                continue

            category = BadgeUtility.categorize_badge(narrative_extract)
            if narrative_extract.lower() in level_narratives[category]:
                continue

            narrative = BadgeUtility.get_badge_narrative_title(narrative_extract)
            badge_structure = BadgeUtility.create_badge_structure(badge, narrative, access_log_id)
            
            level_narratives[category].add(narrative_extract.lower())
            levels[category].append(badge_structure)

        self.membership_years = sorted(list(years), reverse=True)
        self.member_status = self._determine_membership()
        levels_order = ["Red Level", "Yellow Level", "Green Level", "White Level"]

        return sorted([{
            "name": level,
            "expanded": BADGE_LEVELS.get(level, {"expanded": False, "color": "#FFFFFF"})["expanded"],
            "color": BADGE_LEVELS.get(level, {"expanded": False, "color": "#FFFFFF"})["color"],
            "badges": badges
        } for level, badges in levels.items()], 
        key=lambda x: levels_order.index(x["name"]))

    def response_format_with_session_id(self, session_id: int) -> Dict[str, Any]:
        """
        Injects the session ID into each badge's AccessLogID field.
        Returns the processed badges with session ID included.
        """
        return self.generate_response_format(session_id=session_id)