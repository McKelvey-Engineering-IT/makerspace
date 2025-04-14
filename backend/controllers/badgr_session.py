from typing import Any, Dict, Optional, Tuple, List
from controllers.badgr_connector import BadgrConnector
from datetime import datetime

BADGE_LEVELS = {
        "Red Level": {
            "expanded": True,
            "color": "#FF6B6B",  # Softer red
            "terms": [
                'Mini-Mill (CNC)',
                'Laser Cutting',
                'Power Tools - Band Saw',
                'Power Tools - Drill Press',
                '3D Scanner'
            ]
        },
        "Yellow Level": {
            "expanded": True,
            "color": "#FFD93D",  # Warmer yellow
            "terms": [
                'Handheld Power Tool - Cordless Drill',
                'Handheld Power Tool - Dremel',
                'Handheld Power Tool - Jigsaw',
                'Sewing',
                'Soldering',
                'Vinyl Cutting'
            ]
        },
        "Green Level": {
            "expanded": False,
            "color": "#4CAF50",  # Softer green
            "terms": [
                '3D Printing - Know the Basics',
                '3D Slicing with Prusa Slicer',
                '3D Slicing with PreForm (Form 3)',
                'Button Maker',
                'Laser Cutting with Inkscape',
                'Laser Cutting with Illustrator',
                'Heat Press',
                'Heat Press - Mini',
                'Mug Press'
            ]
        }
    }

class BadgrSession:
    @staticmethod
    def format_badges(badges: List[Dict[str, Any]], member_badge_id: str = None) -> Dict[str, Any]:
        """
        Static method to format badges into the expected response structure.
        Can be used with badges from either Badgr API or database.
        
        Expected badge dict format:
        {
            'id': str,
            'narrative': str,  # or Narrative_Detail
            'badgeclass': str, # or BadgeClass
            'createdAt': str,
            'issuedOn': str,
            'revoked': bool,
            'revocationReason': str,
            'image': str
        }
        """
        levels = {level: [] for level in BADGE_LEVELS.keys() | {"White Level"}}
        years = set()
        level_narratives = {level: set() for level in levels.keys()}
        is_member = False

        for badge in badges:
            # Handle different field names between Badgr API and DB
            narrative = badge.get('narrative') or badge.get('Narrative_Detail', '')
            badge_class = badge.get('badgeclass') or badge.get('BadgeClass', '')
            
            if member_badge_id and badge_class == member_badge_id:
                is_member = True
                
            year = BadgrSession._extract_membership_year(narrative)
            if year:
                years.add(year)

            if not narrative or "makertech" in narrative.lower():
                continue

            category = BadgrSession._categorize_badge(narrative)
            if narrative.lower() in level_narratives[category]:
                continue

            narrative_parts = BadgrSession._get_badge_narrative_title(narrative)
            badge_structure = {
                "Narrative_Title": narrative_parts[1],
                "Narrative_Detail": narrative_parts[0],
                "CreatedAt": badge.get("createdAt") or badge.get("CreatedAt"),
                "IssuedOn": badge.get("issuedOn") or badge.get("IssuedOn"),
                "Revoked": badge.get("revoked") or badge.get("Revoked", False),
                "Revocation_Reason": badge.get("revocationReason") or badge.get("RevocationReason"),
                "BadgeClass": badge_class,
                "ImageURL": badge.get("image") or badge.get("ImageURL"),
                "AccessLogID": badge.get("AccessLogID"),
            }
            
            level_narratives[category].add(narrative.lower())
            levels[category].append(badge_structure)

        membership_years = sorted(list(years), reverse=True)
        membership_status = BadgrSession._determine_membership_status(membership_years)
        
        levels_order = ["Red Level", "Yellow Level", "Green Level", "White Level"]
        formatted_levels = sorted([{
            "name": level,
            "expanded": BADGE_LEVELS.get(level, {"expanded": False, "color": "#FFFFFF"})["expanded"],
            "color": BADGE_LEVELS.get(level, {"expanded": False, "color": "#FFFFFF"})["color"],
            "badges": badges
        } for level, badges in levels.items()], 
        key=lambda x: levels_order.index(x["name"]))

        return {
            "isMember": is_member,
            "membershipStatus": membership_status,
            "badges": formatted_levels
        }

    @staticmethod
    def _determine_membership_status(membership_years: List[str]) -> str:
        if not membership_years:
            return "Non-member"
            
        current_date = datetime.now()
        check_year = current_date.year + (1 if current_date.month > 7 else 0)
        
        return "Current Member" if str(check_year) in membership_years else "Expired"

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

    def _extract_membership_year(narrative: str) -> str:
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

    def _create_badge_structure(badge: Dict[str, Any], narrative: Tuple[str, str], access_log_id: Optional[int]) -> Dict[str, Any]:
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

    def _categorize_badge(narrative: str) -> str:
        narrative = narrative.lower().strip()

        for level, config in BADGE_LEVELS.items():
            if narrative in [term.lower() for term in config["terms"]]:
                return level
                
        return "White Level"

    def organize_badges(self, access_log_id=None) -> List[Dict[str, Any]]:
        levels = {level: [] for level in BADGE_LEVELS.keys() | {"White Level"}}
        years = set()
        level_narratives = {level: set() for level in levels.keys()}  # Track narratives per level

        for badge in self.session_badges:
            badge_id = badge.get('id')
            
            if badge.get('badgeclass') == self.member_badge_id:
                self.member_status = True
                
            year = BadgrSession._extract_membership_year(badge.get('narrative', ''))
            if year:
                years.add(year)

            narrative_extract = badge.get("narrative")
            if not narrative_extract or "makertech" in narrative_extract.lower():
                continue

            category = BadgrSession._categorize_badge(narrative_extract)
            if narrative_extract.lower() in level_narratives[category]:
                continue

            narrative = BadgrSession._get_badge_narrative_title(narrative_extract)
            badge_structure = BadgrSession._create_badge_structure(badge, narrative, access_log_id)
            
            level_narratives[category].add(narrative_extract.lower())
            levels[category].append(badge_structure)

        self.membership_years = sorted(list(years), reverse=True)
        
        levels_order = ["Red Level", "Yellow Level", "Green Level", "White Level"]
        return sorted([{
            "name": level,
            "expanded": BADGE_LEVELS.get(level, {"expanded": False, "color": "#FFFFFF"})["expanded"],
            "color": BADGE_LEVELS.get(level, {"expanded": False, "color": "#FFFFFF"})["color"],
            "badges": badges
        } for level, badges in levels.items()], 
        key=lambda x: levels_order.index(x["name"]))

    def _get_badge_narrative_title(narrative: str) -> Tuple[str, str]:
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

    def _get_membership_status(self) -> str:
        """
        Determines detailed membership status:
        - "Current Member": Has current year's orientation
        - "Expired": Has past orientation but not current
        - "Non-member": Never had orientation
        """
        if self._system_date_membership():
            return "Current Member"
        elif self.membership_years:
            return "Expired"
        return "Non-member"

    def get_user_badges(self, access_log_id: Optional[int] = None) -> Dict[str, Any]:
        return {
            "isMember": self._system_date_membership(),
            "membershipStatus": self._get_membership_status(),
            "badges": self.organize_badges(access_log_id)
        }
