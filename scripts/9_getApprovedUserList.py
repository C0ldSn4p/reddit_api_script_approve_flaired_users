#!/usr/bin/python3

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.
#
# @author C0ldSn4p


import requests
from requests.auth import HTTPBasicAuth
import json
import time


#####################
### Inputs & Conf ###
#####################

# local configuration
from generatedFiles.configuration import conf

outputFilename = "generatedFiles/contributors_list.py"
urlContributor = 'http://oauth.reddit.com/r/'+conf['subreddit']+'/about/contributors?limit=100'

userList = []



########################
### helper functions ###
########################


def processResponseJSON(response_text):
    jsonData = json.loads(response_text)
    if 'data' not in jsonData or 'children' not in jsonData['data']:
        print("Error no users")
        return ''
    users = jsonData['data']['children']
    for user in users:
        username = user['name']
        userList.append(username)
    next = jsonData['data'].get('after', '')
    if not next:
        next = ''
    return next

def waitIfNeeded(response):
    headers = response.headers
    ratelimitRemaining = float(headers["x-ratelimit-remaining"])
    ratelimitReset = float(headers["x-ratelimit-reset"])
    if ratelimitRemaining < 5:
        print("WARNING: ratelimit close, sleep for "+str(ratelimitReset)+"s")
        time.sleep(ratelimitReset)



####################
###### Set Up ######
####################

# Set user agent
headers = requests.utils.default_headers()
headers.update({'User-Agent': conf['user_agent']})

# Auth and get token
auth=HTTPBasicAuth(conf['auth_id'], conf['auth_secret'])
url = 'https://www.reddit.com/api/v1/access_token'
data = {'grant_type': 'refresh_token', 'refresh_token': conf['refresh_token']}
x = requests.post(url, data = data, auth = auth, headers = headers)
response = json.loads(x.text)
access_token = response['access_token']

# update header
headers.update({'Authorization': 'bearer '+access_token})
print("token refreshed: "+x.text)



###############
#### Main  ####
###############


# Get contributors data
print("Fetch contributors data")
k=1

url = urlContributor
x = requests.get(url, headers = headers)
next = processResponseJSON(x.text)

print(str(k)+" | "+url+" | "+next)

while next != '':
    k+=1
    url = urlContributor+'&after='+next
    x = requests.get(url, headers = headers)
    next = processResponseJSON(x.text)
    print(str(k)+" | "+url+" | "+next)
    waitIfNeeded(x)
    
print("Found "+str(len(userList))+" contributors.")


# Generate output file
with open(outputFilename, 'w') as out_file:
    out_file.write('contributorList = [')
    for i in range(len(userList)-1):
        out_file.write('"'+userList[i]+'",')
    out_file.write('"'+userList[len(userList)-1]+'"')
    out_file.write(']\n')
    
print("User list generated in "+outputFilename)
