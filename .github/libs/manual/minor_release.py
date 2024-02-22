'''
WARNING this script force pushes to the main branch, and should only be used by those with familiarity of what it does. 


We increment the z version number by one, and list the intermediatary commits. We then update the staus message. When the automation sees this, the versioning should be increased. 

'''

import os, sys
import pprint


# cleans the current repository from automated commits 
import remove_automated_commits


import json, os 
from datetime import datetime, timezone
from collections import OrderedDict
def runread(cmd):
    print(os.popen(cmd).read())

url = os.popen('git config --get remote.origin.url').read().strip()
owner,repo = url.replace('.git','').split('/')[-2:]
store = f'../../../.github/status_{owner}_{repo}.json'

# open the old status file
status = json.load(open(store,'r'))
pprint.pprint(status)


tag = status['repo']['version']

# the commits that have happened since the last release
updates = ['- '+u for u in os.popen(f'git log --oneline {tag}..HEAD').read().split('\n')][:-1]

# make sure we have some commits since the last update
assert len(updates)

newtag = tag.split('.')
newtag[-1] = str(int(newtag[-1])+1)
newtag = '.'.join(newtag)

commits = [f'## Minor Version Update: {tag} → {newtag}']
commits.extend(updates)

# Get the current UTC timestamp
current_utc_timestamp = datetime.utcnow().replace(tzinfo=timezone.utc)
# Format the timestamp as 'YY/MM/DD HH:MM UTC'
formatted_timestamp = current_utc_timestamp.strftime('%Y/%m/%d %H:%M UTC')

# update the changelog
status['changelog'] = dict(last_changed=formatted_timestamp,comment=commits)
status['repo']['version'] = newtag
# update the status 


# overwrite the status. 
json.dump(status ,open(store,'w'),indent=4)

runread('git add -A')
runread(f'git commit -m "Manually triggering release {newtag} by updating status file."')

# forcepush 
remove_automated_commits.forcepush()



