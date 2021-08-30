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

outputFilename = "flaired_user_list.py"
urlApprove = 'https://oauth.reddit.com/r/'+conf['subreddit']+'/api/friend'

# user list to approve (from previous script)
from generatedFiles.flaired_user_list import userList


########################
### helper functions ###
########################

successCount = 0
errorCount = 0

def waitIfNeeded(response):
    headers = response.headers
    ratelimitRemaining = float(headers["x-ratelimit-remaining"])
    ratelimitReset = float(headers["x-ratelimit-reset"])
    if ratelimitRemaining < 5:
        print("WARNING: ratelimit close, sleep for "+str(ratelimitReset)+"s")
        time.sleep(ratelimitReset)
    
def processResponse(user, responseText):
    try:
        jsonData = json.loads(responseText)
        errors = jsonData["json"]["errors"]
        if len(errors) == 0:
            successCount += 1
            print(user+" approved successfully!")
        else:
            errorCount += 1
            print("ERROR approving "+user+". Error message: "+str(errors))
    except:
        errorCount += 1
        print("WARNING with approving "+user+"??? Response cannot be read!")


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

print("Approving users")
print("")

for user in userList:
    data = {'api_type': 'json', 'name': user, 'type': 'contributor'}
    x = requests.post(urlApprove, data = data, headers = headers)
    processResponse(user, x.text)
    waitIfNeeded(x)

print("")
print("Done!")
print("Successes: "+str(successCount)+" | Errors: "+str(errorCount))
print("Check https://www.reddit.com/r/"+conf['subreddit']+"/about/contributors/ to verify that everything went well, or use the last script to generate a list of all approved user to compare.")
