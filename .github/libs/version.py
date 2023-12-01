'''
Aims: 
    Action Parameters
    If:
        main branch - update the version metadata_loc
        see what files have changed 
        update the version number 
        reflect this
        
    Else:
        Create a blank header for the file_metadata_loc
        
    

'''


import glob,os,sys,re,json
from collections import OrderedDict
import argparse
from urllib.request import Request, urlopen
from checksum_tools import validate_checksum,calculate_checksum
from datetime import datetime

prefix = 'CMIP6Plus_'
main = 'main'
metadata_loc = 'Header'


##########################################
# load the maintainer file
##########################################

maintain_data = 'https://raw.githubusercontent.com/PCMDI/mip-cmor-tables/main/.github/maintainer_institutes.json'

with urlopen(maintain_data) as response:
    raw_data = response.read()

maintainers = json.loads(raw_data.decode('utf-8'))


##########################################
# get repo information
##########################################

tag = os.popen("git describe --tags --abbrev=0 --always").read().strip() or ''
# release_date = subprocess.check_output(["git", "log", "-1", "--format=%aI", tag]).strip().decode("utf-8")

files = glob.glob(f'{prefix}*.json')

##########################################
# read api keys
##########################################
parser = argparse.ArgumentParser(description="Retrieve details for the latest tag of a GitHub repository.")
parser.add_argument("-t","--token" ,help="token number")
parser.add_argument("-b","--branch" ,help="branch name")
parser.add_argument('-a','--all', action='store_false',help='If added, we will overwrite ALL the files. ')

args = parser.parse_args()


    ##########################################
    # Get the Tag information from the CVs
    ##########################################
def get_latest_repo(repo_owner, repo_name, github_token=None):
    tags_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    headers = {"Authorization": f"Bearer {github_token}"} if github_token else {}

    try:
        # Get the list of tags
        request = Request(tags_url, headers=headers)
        with urlopen(request) as response:
            tags_data = json.loads(response.read())

        if tags_data:
            # Select the latest tag
            latest_tag = tags_data
            tag_name = latest_tag['tag_name']
            published = latest_tag['published_at']
            # commit_sha = latest_tag['commit']['sha']
            html = latest_tag['html_url']


            return {"tag_name": tag_name, "date": published, "url":html}

    except Exception as e:
        print(f"Error: {e}")

    return None

CVs = get_latest_repo('WCRP-CMIP','CMIP6Plus_CVs',args.token)


    ##########################################
    # iterate over all the files. 
    ##########################################
for f in files:


    contents = json.load(open(f,'r'))


    if metadata_loc not in contents or not args.all:
        contents[metadata_loc] = dict(file = {"checksum":''},commit='')
        print('setting blank header on ',f)

    if validate_checksum(contents,metadata_loc):
        continue


    skip = 'CMIP-IPO: Automated GitHub Action <actions@wcrp-cmip.org>'  
    # commit_info = os.popen(f'git log -n 1 -- {f} ').read()
    full = os.popen(f'git log -- {f} ').read()


    previous_commit = ''
    commit_info = False
    
    
    '''
    commit 8f25db6f5551574eb826c21ce404d2e111bd2db2
    Merge: caa0888 124d96c
    Author: Daniel Ellis <daniel.ellis@ext.esa.int>
    Date:   Fri Jan 26 16:03:55 2024 +0000

    Merge remote-tracking branch 'origin/source_id_MPI-ESM1-2-LR' into merge_src_pull_requests


    '''

    commit_blocks = re.split(r'\n(?=commit\s)', full)
    for c in commit_blocks:
        if 'reset-checksum' in c:
            continue
        if 'Automated Versioning Update' in c:
            continue
        if skip not in c:
            if not commit_info:
                commit_info = c
            elif commit_info and not previous_commit:
                previous_commit = re.search(r"commit (\S+)", c)
                break

    if 'commit_info' not in locals():
        print(f)
        print(commit_blocks)
        print('no suitable commit found')
        sys.exit('no suitable commit found')


    ##########################################
    # extract commit info
    ##########################################

    commit_dict = {}

    # Extract information using regular expressions
    commit_match = re.search(r"commit (\S+)", commit_info)
    author_match = re.search(r"Author: (.+)", commit_info)
    date_match = re.search(r"Date: (.+)", commit_info)
    commit_message_match = re.search(r"    (.+)", commit_info)

    if commit_match:
        commit_dict["commit_sha"] = commit_match.group(1)

    if author_match:
        author_info = author_match.group(1).split(" <")
        commit_dict["author_name"] = author_info[0]
        try:
            commit_dict["author_institute"] = maintainers[author_info[0]]['institute']
            commit_dict["author_name"] = maintainers[author_info[0]]['published_name']
        except:
            commit_dict["author_name"] = author_match.group(1)
            
            print( f'Please add \n\t "{author_info[0]}": \n\t\t','{"institute": "", "published_name": "Name you wish to use"}')
            # this was a keyerror
            
        commit_dict["author_email"] = author_info[1][:-1]  

    if date_match:
        commit_dict["commit_date"] = date_match.group(1)

    if commit_message_match:
        commit_dict["commit_message"] = commit_message_match.group(1)


    ##########################################
    # create a new version metadata_loc 
    ##########################################

    # previous_commit = contents['version_metadata_loc'].get('commit','')
    short = f.replace('.json','').replace(prefix,'')

    template =  OrderedDict({
        # collection
        "collection":OrderedDict({
            "CV_collection_version":CVs['tag_name'],
            "CV_collection_modified":CVs['date'],
            "CV_collection_release":CVs['url'],
            "specs_doc": "v6.5.0"
        }),
        # file
        "file":OrderedDict({
            "checksum": 'checksum',
            f"{short}_update_commit":commit_dict['commit_sha'],
            f"{short}_modified":commit_dict['commit_date'].lstrip(),
            f"{short}_note":commit_dict['commit_message'],
        }),
            
        "author":commit_dict['author_name'],
        "institution_id":commit_dict.get('author_institute', 'unlisted'),
        })
        
        
    del contents[metadata_loc]
    previous = contents.copy()

    contents = OrderedDict({metadata_loc:template})
    
    if args.branch.split('/')[-1] != main:
        contents[metadata_loc]['file'] = OrderedDict({
            "checksum": f'Contents will be updated in branch {main} only.',
            f"{short}_update_commit":'',
            f"{short}_modified":'',
            f"{short}_note":'',
        })
        
    
    for key in sorted(previous):
        contents[key] = previous[key]

    contents = calculate_checksum(contents,checksum_location=metadata_loc,nest = 'file')

    print('writing',f)

    import pprint
    pprint.pprint(contents[metadata_loc])

    print('----------------------------\n\n')
    
   

    print(len(contents))
    with open(f,'w') as writef:
        json.dump(contents,writef,indent=4)
    # print (contents)



    ##########################################
    # keep the individualised commit messages
    ##########################################

    timestamp_obj = datetime.strptime(commit_dict['commit_date'].lstrip(), "%a %b %d %H:%M:%S %Y %z")
    formatted_timestamp = timestamp_obj.strftime("%y/%m/%d %H:%M")
    print(author_match.group(1))
    print(commit_dict['commit_message'])

    os.popen(f"git add {f}").read()
#     os.popen(f"git commit -m '{formatted_timestamp} - {commit_dict['commit_message'][:50]}'").read()
    os.popen(f'git commit --author="{author_match.group(1)}" -m "{commit_dict["commit_message"]}"').read()

    
    
    
os.popen(f'git push').read()

# checksum. If checksum is not the same, update.



'''
export PATH="${HOME}/Applications/Docker.app/Contents/Resources/bin:$PATH"

act -s GITHUB_TOKEN="$(gh auth token)" --container-architecture linux/amd64 -b & sleep 4 

'''
