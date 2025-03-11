from routes.dependencies import get_badgr_connector


badgr = get_badgr_connector()


from pprint import pprint

pprint(badgr.get_by_entityId("k.k.miller@wustl.edu"))
