import json, os, sys
from collections import OrderedDict

# Get the parent directory of the current file
parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir)

from action_functions import update_issue,jr,jw,getfile,close_issue,pp

# data
issue_number = os.environ['ISSUE']
data = os.environ['PAYLOAD_DATA']
data = json.loads(str(data))


# Load Existing
activities = jr(getfile('activity_id')[0])
alist = activities['activity_id']


import urllib.request

def url_exists(url):
    try:
        urllib.request.urlopen(url)
        return True
    except urllib.error.HTTPError:
        return False
    except urllib.error.URLError:
        return False
      
      

if data['name'] in activities:
  close_issue(issue_number,f'# Closing issue. \n {data["name"]} already exists in the activity list. \n\n Please review request and resubmit.')
      
if not url_exists(data['url']):
  update_issue(issue_number,f"#Invalid URL \n {data['url']} does not appear to be valid")


# add
alist[data['name']] = OrderedDict({'URL': data['url'],'long_name': data['long_name']})
pp(alist[data['name']])
# sort and update
activities['activity_id'] = OrderedDict(sorted(alist.items()))



# Serialize back to JSON
new_json_data = jw(data, getfile('activity_id')[0])









