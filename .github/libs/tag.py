import json, os 
from datetime import datetime, timezone
from collections import OrderedDict


branch = os.popen('git rev-parse --abbrev-ref HEAD').read().strip().replace(' ','')
'''
Versioning:
w, x, y, z - 
w :: mip era
x :: structural change  | new activity_id | new spec 
y :: experiment 
z :: other | source | institution
'''


UPDATE_REQUIRED = False

url = os.popen('git config --get remote.origin.url').read().strip()
owner,repo = url.replace('.git','').split('/')[-2:]

store = f'.github/status_{owner}_{repo}.json'


MIPERA = 'CMIP6Plus'
new = OrderedDict(repo=dict(mipera=MIPERA,repo=repo,url=url),changelog={})
comment = ''
new['repo']['version'] = 'none'


try:
    old = json.load(open(store,'r'))
    version = old['repo']['version']
    tvers = os.popen('git tag -l').read().strip().split('\n')[-1]
    if version > tvers:
        print('WARNING VERSION MISMATCH',version, tvers)
        UPDATE_REQUIRED = True
        new.update(old)
        comment = '\n'.join(new['changelog'].get('comment',''))
    else: 
        version = tvers
    
except Exception as err:
    print(err)
    old = None
    version = os.popen('git tag -l').read().strip().split('\n')[-1]
    UPDATE_REQUIRED = True
    
w,x,y,z = map(int,version.strip('v').strip().split('.'))

if branch == 'main':
  
    #  If not wcrp-cmip, do not create this. 

    files = ['activity_id','experiment_id','source_id']
    files.reverse() # do this as new activites or experiments reset the following version numbers 

    for f,vnum in zip(files,'z y x'.split()):
        repos = json.load(open(f'{MIPERA}_{f}.json'))[f]
        keys = list(repos.keys())
        new[f] = dict(counts = len(keys), keys = keys)

        if old:
            diff = set(new[f].get('keys')) - set(old.get(f,new[f]).get('keys'))
            if len(diff):
                # and old:
                # increment sequentially
                locals()[vnum] += bool(len(diff))

                    
                UPDATE_REQUIRED = True
                for i in diff:
                    comment += f'- [x] **{vnum}** version number ↑ :: *{f} ({i.strip()})*\n'
                
                if vnum == 'x':
                    locals()['y'] = 0 
                    locals()['z'] = 0 
                    comment += f'__A change in x resets y and z values__\n>[!NOTE]\n  '
                elif vnum == 'y':
                    locals()['z'] = 0 
                    comment += f'__A change in y resets z values__\n>[!NOTE]  \n'
    
                comment += f'#### <ins>Updating version index "{vnum}"</ins>\n'

    # Get the current UTC timestamp
    current_utc_timestamp = datetime.utcnow().replace(tzinfo=timezone.utc)
    # Format the timestamp as 'YY/MM/DD HH:MM UTC'
    formatted_timestamp = current_utc_timestamp.strftime('%Y/%m/%d %H:%M UTC')


    new['repo']['version'] = f'v{w}.{x}.{y}.{z}'

    if UPDATE_REQUIRED:
        
        comment += " \n\nFor further information: [see the wiki](https://wiki.mipcvs.dev)\n>> \` v{w}.{x}.{y}.{z} \`\n\n"
        
        comment += f"## Version Updated: {version} \u2192 {new['repo']['version']}\n\n"
        comment = comment.split('\n')
        comment.reverse()
        print('\n'.join(comment))

    new['changelog'] = dict(last_changed=formatted_timestamp,comment=comment)
        





if UPDATE_REQUIRED and branch == 'main':   
    print('write!')
    json.dump(new,open(store,'w'),indent=4)
    
    email = "actions@wcrp-cmip.org"
    author = "CMIP-IPO: Automated GitHub Action"
    message = f"Updating stats for {new['repo']['version']}"
    os.popen(f"git add {store}").read()
    os.popen(f'git commit --author="{author} <{email}>" -m "{message}"').read()
    print(os.popen(f'git push').read())
    
    
# elif old:
#     if old['repo']['version'] != new['repo']['version']:
#         # this does not trigger if old version is already updated
#         # thus update triggered at the start. 
#         UPDATE_REQUIRED = True
#         print('\n'.join(old['changelog']['comment']))
#         new = old

        
NEWVERSION = new['repo']['version']
print(f'\n\n{NEWVERSION} :: needs update: {UPDATE_REQUIRED}')

CONTENTS = new['changelog']['comment']

if branch != 'main': 
    print('automations only run on main branch. You are on:', branch)
    
print(branch)

# git tag -d old-tag-name
# git push origin :refs/tags/old-tag-name



# import pprint
# pprint.pprint(new)


