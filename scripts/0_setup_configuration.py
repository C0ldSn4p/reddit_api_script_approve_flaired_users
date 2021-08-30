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

intro = """
This script will help you set up the required configuration file.

You need to have set up a developer app on reddit:

  1. Go to https://www.reddit.com/prefs/apps
  2. Click on create an app
  3. Choose a name, a description (optional), choose script, leave the about url empty and put "http://localhost:8080" as redirect uri
  4. You should see the app auth-ID under "personal use script" and the app secret, you will need it later.
  
  THE APP ID AND SECRET SHOULD STAY A SECRET! DO NOT POST THEM ON A PUBLIC WEBPAGE OR PEOPLE COULD USE YOUR ACCESS!
"""

print(intro)

client_id = input("Input the application's auth-ID: ")
client_secret = input("Input the application's secret: ")
redirect_uri = input("Input the application's redirect_uri (should be http://localhost:8080): ")
user_agent = input("Choose a user agent (for example: MyName Script): ")

duration="permanent" # the token will be permanent
response_type="code"
state="StateGenerateTokenSuccess"
scope="modflair%20modcontributors%20read" # required scope

url = "https://www.reddit.com/api/v1/authorize?client_id="+client_id+"&response_type="+response_type+"&state="+state+"&redirect_uri="+redirect_uri+"&duration="+duration+"&scope="+scope

print("")
print("Use this url in a webbrowser where you are logged on reddit: "+ url)
print("")
print("You should be automatically redirected to a page asking you to allow your app to use your account's rights.")
print("Click allow and you will be redirected to a blank page.")
print("Note the url of the blank page, it contains a code (...code=THECODE#... the # is not included in the code)")
print("")

code = input("Input the response's code: ")

print("")
print("Generating the token...")
headers = requests.utils.default_headers()
headers.update({'User-Agent': user_agent})
auth=HTTPBasicAuth(client_id, client_secret)
url = 'https://www.reddit.com/api/v1/access_token'
data = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': redirect_uri}
x = requests.post(url, data = data, auth = auth, headers = headers)
responseJson = json.loads(x.text)
refresh_token = responseJson['refresh_token']
print("Token generated successfully, refresh token: "+refresh_token)
print("DO NOT SHARE THE REFRESH TOKEN!")

print("")
subreddit = input("Input the name of the subreddit you wish to modify (you can change this in the configuration.py file later), for example 'all' for 'r/all': ")
print("")

with open("generatedFiles/configuration.py", "w") as out_file:
    out_file.write("conf = {\n")
    out_file.write("    'user_agent': '"+user_agent+"',\n")
    out_file.write("    'auth_id': '"+client_id+"',\n")
    out_file.write("    'auth_secret': '"+client_secret+"',\n")
    out_file.write("    'refresh_token': '"+refresh_token+"',\n")
    out_file.write("    'subreddit': '"+subreddit+"'\n")
    out_file.write("}\n")

print("Configuration file configuration.py successfully generated!")

