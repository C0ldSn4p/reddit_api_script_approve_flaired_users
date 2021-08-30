# About

Python3 script to approve (= add as contributor) all non banned user of a subreddit having a flair

Approved users can be allowed to access a private subreddit

This program is free software. It comes without any warranty.


# Scripts

All scripts can be found in the scripts folder and run with python3 (e.g. `python3 0_setup_configuration.py`)

* 0_setup.py: setup the script collection. Requires the setup of a reddit app (guided in the script).
* 1_getFlairedUserList.py: generate a list of all user with a flair and not currently banned from the subreddit. Can be reviewd in the generatedFiles folder
* 2_approveUserList.py: approve all the users in the list created by the previous script
* 9_getApprovedUserList.py: get the list of all approved user, can be usefull to make a backup before using the other scripts or checking that everything worked (warning: it overrides existing list so if you made a backup copy it somewhere else before running this script again)
