import requests
import csv 
import time 

USERNAME = "makertech@wustl.edu"
KEY = "SfgpMyDTaFqJc"
ISSUER = "622371361638ea22089c6a49"


# https://{BADGR_DOMAIN}/v2/users/self' -H "Authorization: Bearer YOURACCESSTOKEN"

# Get the token for this session
tokenResponse = requests.post('https://api.badgr.io/o/token', data={'username': USERNAME, 'password': KEY})
tokenResponseJSON = tokenResponse.json()
token = tokenResponseJSON.get('access_token')

print(token)
def getFromBadger(endpoint):
 return requests.get('https://api.badgr.io'+endpoint, headers={'Authorization': 'Bearer ' + token})


# To get the issuer ID for the current user (username/password) --- the NDWAD9BtTsGWRKHivY7BxQ for Jubel
issuers = getFromBadger('/v2/issuers')
ISSUER = issuers.json()['result'][0]['entityId']    


allBadgesQuery = getFromBadger(f'/v2/issuers/{ISSUER}/badgeclasses')
from pprint import pprint
pprint(allBadgesQuery.json())
# Get all badge classes
# user = getFromBadger('/v2/users/self')

# Get all assertions for this issuer
# allBadgesQuery = getFromBadger(f'/v2/issuers/{ISSUER}/badgeclasses')
# allBadgeData = allBadgesQuery.json()['result']
# Create a map of badge ID to badge name for all badges
# allBadges = { b['entityId']:b['name'] for b in allBadgeData}
# badgesSortedByName = sorted(allBadges.items(), key=lambda x: x[1])
# sortedBadgeNames = [b[1] for b in badgesSortedByName]

# allAssertionsQuery = getFromBadger(f'/v2/issuers/{ISSUER}/assertions')
# allAssertionsData = allAssertionsQuery.json()['result']


# users = {}  # Map of email to {name, badgeIDs, isuedOns}

# # Create a map of users 
# for a in allAssertionsData:
#     # Get all the relevant fields or defaults
#     recipient = a['recipient']  
#     id = recipient.get('plaintextIdentity',"None")
#     if id not in users:
#         if 'extensions' in a and 'extensions:recipientProfile' in a['extensions'] and 'name' in a['extensions']['extensions:recipientProfile']:
#             name = a['extensions']['extensions:recipientProfile']['name']
#         else:
#             name = ""
#         users[id] = {'name': name, 'badgeIDs': [], 'issuedOns': []}
#     # Add this badge to the user
#     badgeID = a['badgeclass']
#     users[id]['badgeIDs'].append(badgeID)
#     issuedOn = a['issuedOn']
#     users[id]['issuedOns'].append(issuedOn)

# # Create a sorted list of users
# usersSortedByEmail = sorted(users.items(), key=lambda x: x[0])

# tableHeader = ['Email', 'Name']+sortedBadgeNames

# timestr = time.strftime("%Y-%m-%d-%H%M%S")
# fileName = "allBadges_" + timestr + ".csv"
# with open(fileName, 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(tableHeader)
#     for user in usersSortedByEmail:
#         email = user[0]
#         userData = user[1]
#         row = [email, userData['name']]
#         for badge in badgesSortedByName:
#             if badge[0] in userData['badgeIDs']:
#                 indexOfBadge = userData['badgeIDs'].index(badge[0]) 
#                 row.append('Completed - ' + userData['issuedOns'][indexOfBadge])
#             else:
#                 row.append('')
#         writer.writerow(row)



# response = requests.get('https://api.badgr.io', headers={'Authorization': 'bearer ' + token})

# print(response.json())

# response = requests.post('https://api.badgr.io/o/token', data={'username': 'client_credentials', 'password': 'myClientId'})
# print(response.json())