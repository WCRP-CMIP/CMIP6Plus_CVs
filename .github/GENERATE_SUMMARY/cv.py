# %%
import cmipld
import importlib,json
from collections import OrderedDict


repo_url = cmipld.utils.git.url()
io_url = cmipld.utils.git.url2io(repo_url)

branch = cmipld.utils.git.getbranch()
repopath = cmipld.utils.git.toplevel()
reponame = cmipld.utils.git.reponame()

whoami = cmipld.reverse_mapping()[io_url]
print('-'*50)
print(f'Parsing repo: {whoami}')
print(f'Location: {repo_url}')
print(f'Github IO link: {io_url}')
print('-'*50)

'''
To keep this set of functions generic, we create separate files containing all relevant functions for a repository to be processed. 
When running this script we determine the parent repository, and consequently its prefix. This is then used to grab all relevant functions for processing. 

Example usage: getattr(this,'activity')({'activity':[{"label":1,"id":'one'}]})

'''
# Dynamically import the target module and assign it to a variable
module_path = f"cmipld.cvs.{whoami}" # go to CMIPLD/CVs/<value of whoami>.py for functions
this = importlib.import_module(module_path)



# %%
# Set up offline override for the current repository

from cmipld.utils.offline import LD_server

ldpath = cmipld.utils.git.ldpath()


# create a temporary directory containing (a copy of) the current repository
# localserver = LD_server(copy = [[ldpath,'current_repo']])
repos= { 
        'https://wcrp-cmip.github.io/WCRP-universe/': 'universal',
        'https://wcrp-cmip.github.io/MIP-variables/': 'variables',
        'https://wcrp-cmip.github.io/CMIP6Plus_CVs/': 'cmip6plus'
        }

localserver = LD_server(repos = repos.items(),copy = [[ldpath,whoami]],override='y')

# localserver = LD_server(copy = [[ldpath,'cmip6plus']])


localhost = localserver.start_server(8089)


# %%
cmipld.processor.replace_loader(localhost,[list(i) for i in repos.items()]) 

# %%

CV = OrderedDict()
cmipld.processor.clear_cache()


es_data = {}

# %%


es_data['project'] = project = cmipld.processor.EmbeddedFrame(f'{io_url}project/graph.jsonld') 

for item in [
    'repo',
    'mip-era',
    'license',
    'activity',
    'drs',
    'product',
    'required-global-attributes',
    'tables',
    ]:
    
    print(item)
    # CV[item] = getattr(locals(),item)
    # ld  = cmipld.processor.expand_document(f'{io_url}project/{item}.json', depth=3)[0]
    # functions may be autogenrated in (reponame).py under the CVs dir. 
    
    result = project.frame({'id':f'{io_url}project/{item}-list'})
    # from pprint import pprint 
    # pprint(result)
    
    # print(item,getattr(this,item))
    
    item = item.replace('-','_')
    CV[item] = getattr(this,item)(result[0])
    

# %%


# %%

# adding the index properties
print('index')
CV.update(cmipld.processor.get(f'{io_url}/project/index-list.json')[0]['index'])

# %%
print('make a file for relevant realms and relevant realms')

for universe_item in ['realm','frequency']:
    # 'grid-label''nominal'
    print(universe_item)
    path = f'{cmipld.mapping["universal"]}{universe_item}/graph.jsonld'
    ld  = cmipld.jsonld.compact(path,path)['@graph']
    CV[universe_item] = getattr(this,universe_item)(ld)

# %%
# path = f'{cmipld.mapping["universal"]}resolution/graph.jsonld'
# data  = cmipld.jsonld.compact(path,path)['@graph']

# CV['nominal_resolution'] = [f"{r['value']} {r['unit']}" for r in sorted(data, key=lambda x: float(x['value']) if x['value'].replace('.', '', 1).isdigit() else float('inf'))]

print('make a file for relevant nominal resolution')

# %%
# url = cmipld.processor.resolve_prefix(file)

# loads the experiments graph and relevant dependancies. 
# cmipld.processor.clear_cache()
# localserver.copy_existing_repos([[ldpath,whoami]],override=True)
print(ldpath,whoami)

es_data = {}

for value in ['experiment', 'source']:
    # print(value)
    es_data[value] = cmipld.processor.EmbeddedFrame(f'{io_url}{value}/graph.jsonld') 
    result = es_data[value].frame({'@type':[f'wcrp:{value}']})
    print(result[1])
    CV[value] = getattr(this,value)(result)
    
    

# %%
org = getattr(this,'organisation')(es_data['source'].frame({'@type':f'wcrp:source',"@explicit":True, 'organisation':{}}))
CV['institution_id'] = {k: v for d in org for k, v in d.items()}
print('organisations')

# %%
CV['institution_id']

# %%
if branch == 'main':
    print('remove existing CVs here. ')
    outname = f'CVs/{repopath}/CV.json'
    
else:
    outname = f'CVs/{repopath}/CV_{branch}.json'


cmipld.utils.io.wjsn({"CV":CV}, outname)

# %%
# import glob,json
# files = glob.glob('../source/*.json')
# print(files)

# for f in files:
#     print(f)
#     data = json.load(open(f))
#     data['organisation'] = [data['organisation'][0].split('/')[-1]]
    
#     json.dump(data,open(f,'w'),indent=4)

# data

# %%




