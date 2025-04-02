from typing import Any, Dict, Optional, Tuple, List
from controllers.badgr_connector import BadgrConnector
from datetime import datetime


class BadgrSession:
    BADGE_LEVELS = {
        "Red Level": {
            "expanded": True,
            "terms": [
                'bantam', 'mini-mill', 'cnc',
                'laser cut', 
                'band saw', 'bandsaw',
                'drill press', 'drillpress',
                '3d scan', 'scanner'
            ]
        },
        "Yellow Level": {
            "expanded": True,
            "terms": [
                'cordless drill', 'drill',
                'dremel', 
                'jigsaw', 'jig saw',
                'sewing', 'sew',
                'solder',
                'vinyl cut', 'vinylcut'
            ]
        },
        "Green Level": {
            "expanded": False,
            "terms": [
                '3d print', 
                'prusa', 'slicer',
                'preform', 'form 3',
                'button maker', 'buttonmaker',
                'inkscape',
                'illustrator',
                'heat press', 'heatpress',
                'mug press', 'mugpress'
            ]
        }
    }

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
        narrative = narrative.lower()
        
        for level, config in self.BADGE_LEVELS.items():
            if any(term in narrative for term in config["terms"]):
                return level
                
        return "White Level"

    def organize_badges(self, access_log_id=None) -> List[Dict[str, Any]]:
        levels = {level: [] for level in self.BADGE_LEVELS.keys() | {"White Level"}}
        years = set()
        level_narratives = {level: set() for level in levels.keys()}  # Track narratives per level

        for badge in self.session_badges:
            badge_id = badge.get('id')
            
            if badge.get('badgeclass') == self.member_badge_id:
                self.member_status = True
                
            year = self._extract_membership_year(badge.get('narrative', ''))
            if year:
                years.add(year)

            narrative_extract = badge.get("narrative")
            if not narrative_extract or "makertech" in narrative_extract.lower():
                continue

            category = self._categorize_badge(narrative_extract)
            if narrative_extract.lower() in level_narratives[category]:
                continue

            narrative = self._get_badge_narrative_title(narrative_extract)
            badge_structure = self._create_badge_structure(badge, narrative, access_log_id)
            
            level_narratives[category].add(narrative_extract.lower())
            levels[category].append(badge_structure)

        self.membership_years = sorted(list(years), reverse=True)
        
        levels_order = ["Red Level", "Yellow Level", "Green Level", "White Level"]
        return sorted([{
            "name": level,
            "expanded": self.BADGE_LEVELS.get(level, {"expanded": False})["expanded"],
            "badges": badges
        } for level, badges in levels.items()], 
        key=lambda x: levels_order.index(x["name"]))

    def _get_badge_narrative_title(self, narrative: str) -> Tuple[str, str]:
        if not narrative:
            narrative = "No description available"

        narrative = narrative.replace(":", "").split("Makerspace")
        
        if len(narrative) > 1:
            return narrative[1], narrative[0]
        
        return narrative[0], ""
    
    def _system_date_membership(self) -> bool:
        """
        Determines if user is a current member based on system date:
        Aug-Dec: Check against next year's membership
        Jan-Jul: Check against current year's membership
        """
        current_date = datetime.now()
        check_year = current_date.year
        
        if current_date.month > 7:
            check_year += 1
            
        return str(check_year) in self.membership_years

    def get_user_badges(self, access_log_id: Optional[int] = None) -> Dict[str, Any]:
        return {
            "isMember": self._system_date_membership(),
            "badges": self.organize_badges(access_log_id)
        }
