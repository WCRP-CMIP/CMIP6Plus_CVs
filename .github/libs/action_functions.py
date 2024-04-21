
import os,sys,json,ast
import re,configparser
from io import StringIO


def parse_md(body):
    # remove comments
    pattern = r'<!---(.*?)--->'

    # Remove comments using re.sub
    body = re.sub(r'/r/n',r'/n', re.sub(pattern, '', body, flags=re.DOTALL))
    

    config_str = re.search(r'```\sconfigfile(.*?)```',body, re.DOTALL).group(1)
    print(config_str)

    # Create a file-like object from the string
    config_file = StringIO(config_str)
    
    # Create a ConfigParser object
    config = configparser.ConfigParser()
    
    # Read configuration from the file-like object
    config.read_file(config_file)

    # Initialize an empty dictionary to hold the configuration data
    config_dict = {}

    # Iterate over sections and options
    for section in config.sections():
        config_dict[section] = {}
        for option in config.options(section):
            config_dict[section][option] = ast.literal_eval(config.get(section, option))
    
    return config_dict


def dispatch(token,payload,repo):

    import json
    from urllib import request

    # Construct the request headers
    headers = {
        "Accept": "application/vnd.github.everest-preview+json",
        "Authorization": f"token {token}",
        "Content-Type": "application/json"
    }

    # Encode the payload
    datapayload = json.dumps(payload).encode('utf-8')

    # Make the POST request
    req = request.Request(f"{repo}/dispatches", data=datapayload, headers=headers, method='POST')

    # Perform the request
    try:
        with request.urlopen(req) as response:
            if response.getcode() == 204:
                print("Dispatch event triggered successfully.")
            else:
                print(f"Failed to trigger dispatch event. Status code: {response.getcode()}")
                print(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")


def update_issue_title (issue_number,kind,payload):
    # change issue name to reflect contents. 
    print(os.popen(f'gh issue edit {issue_number} --title "Add {kind}: {payload["client_payload"]["name"]}"').read())


def update_issue(issue_number,comment,err=True):
    out = os.popen(f'gh issue comment {issue_number} --body "{comment}"')
    if err: 
        print(out)
        sys.exit(comment)

def close_issue(issue_number, comment,err=True):
    print(os.popen(f'gh issue close {issue_number} -c "{comment}"'))
    if err: sys.exit(comment)
    
def jr(file):
    return json.load(open(file,'r'))

def jw(data,file):
    return json.dump(data,open(file,'w'), indent=4)

def getfile(fileend):
    import glob
    return glob.glob(f'*{fileend}.json')

def pp(js):
    import pprint
    pprint.pprint(js)