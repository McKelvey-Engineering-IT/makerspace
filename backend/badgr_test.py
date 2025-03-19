from routes.dependencies import get_badgr_connector

badgr = get_badgr_connector()

from pprint import pprint

pprint(
    [
        item["narrative"]
        for item in badgr.get_issues()
        if item["badgeclass"] == "5xGhJ6y0RC6n7H1tM7nRCg"
    ]
)
