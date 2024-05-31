''' 
A python script to go through each JSONld file and extract the information. 
Rules; 
- no "_" in category names!



'''
import asyncio
import glob
import os
import json

shorthand = "cmip6plus:"

# mytag = os.popen('git describe --tags --abbrev=0').read()
cvtag = os.popen("curl -s https://api.github.com/repos/WCRP-CMIP/CMIP6Plus_CVs/tags| jq -r '.[0].name'").read().strip()
miptag = os.popen("curl -s https://api.github.com/repos/PCMDI/mip-cmor-tables/tags| jq -r '.[0].name'").read().strip()

repo = os.popen('git remote get-url origin').read().replace('.git','/blob/main/JSONLD/').strip()
print(repo)



async def githistory(file,root,rstr=True,location=''):
    '''
    Optional extras:
    "author": {"name": "%an", "email": "%ae"}
    "commit": "%h"
    "message": "%s",
    
    Can return object, or a string. 
    '''
    
    update = {}
    
    rtn = os.popen('git log -n 1 --pretty=format:\'{"version:date": "%cd","version:commit":{"hash": "%h","message": "%s","author": {"name": "%an", "email": "%ae"}}}\' --date=iso-strict -- '+root+'/'+file).read()
    
    ncommits = int(os.popen(f'git log --oneline -- "{root}/{file}" | wc -l').read().strip() or 0)
    
    if rtn:
        update = json.loads(rtn)       
    
    
    if rstr:
        version = f'{file.ljust(30)} - {update.get("mdate")}'
    else:
        version = {"@id":f'{location}/{file}',
            # f"{root.replace('../',shorthand)}/{file.rstrip('.json')}",
                   "@type":"version",
                   "version:file":file,
                   
                #    "version:url":f'{location}/{file}',
                   "version:release":{"mip-cmor-tables":miptag,"cmip6plus":cvtag},
                   "version:previous_updates":ncommits,
                   **update,
                   "version:data":{"@id":f"{root.replace('../',shorthand)}/{file.rstrip('.json')}"},}
    
    return version



async def read_json_file(file_path):
    with open(file_path, mode='r') as f:
        content = f.read()
        return json.loads(content)

async def read_json_files(file_paths):
    tasks = [read_json_file(file_path) for file_path in file_paths]
    return await asyncio.gather(*tasks)

async def categorize_files(directory):
    
    context_files = []
    combined=[]
    vcollection=[]

    for root, dirs, files in os.walk(directory):
        # print(root,dirs,files)
        print('>>>',root)
        skip = ['schema.json','graph.json', ".DS_Store",
        "create.ipynb","version.json"]
        
        files.sort()
        
        for skipfile in skip:
            if skipfile in files:
                files.remove(skipfile)
                
        if 'frame.json' in files:
            
            vocab = ''
            # context_file_path = os.path.join(root, 'context.json')
            # os.system(f'mv {root}/context.json; touch {root}/frame.json; ')
            # # context_files.append(context_file_path)
            # vocab = await read_json_file(root+'/context.json')
            # vocab = vocab.get('@vocab','')
            files.remove("frame.json")
        
            # Also add all JSON files in this directory to graph_files
            graph_files = (os.path.join(root, file) for file in files if file.endswith('.json') and not file.endswith('context.json'))
            
            
            graph_data = await read_json_files(graph_files) 
            
            
            
            complete_graph = {
                "@id":root.replace('../',repo),
                "@type": "cmip:graph",
                '@vocab':vocab,
                "ldroot":root[1:],
                "@graph": graph_data,
                "files": files
            }
            
            
            combined.append(complete_graph 
                            )
            # write
            json.dump(complete_graph, open(f"{root}/graph.json",'w') , indent=4)
                
                
            # Create version file:
            
            location = root.replace('../',repo+"/blob/main/")
            version = [await githistory(f,root,False,location) for f in files]
            json.dump(version, open(f"{root}/version.json",'w') , indent=4)
            
            vcollection.extend(version)
                
            
    
    context_data = {}

    # Loop through each entry in the contexts list
    for entry in await read_json_files(context_files):
        # Loop through each key-value pair in the entry dictionary
        for key, value in entry.items():
            if key in context_data and key != '@context':
                try:
                    context_data[key]['@context'].update(value['@context'])
                except: 
                    print('FAIL',key, context_data)
            else:
                context_data[key] = value
                
            
    context_data = context_data
    
    return {'graph': combined, 'context': context_data, 'version':vcollection}

async def main():
    lddata = await categorize_files('../')

    # Dumping the contents of each category to separate files
    json.dump(lddata['graph'], open('graph_data.json', 'w'), indent=4)
    json.dump(lddata['context'], open('context_data.json', 'w'), indent=4)
    
    
    def rmsp(graphs):
        for g in graphs:
            g['files'] = json.loads(json.dumps(g['files']).replace(' ',''))
        
        return graphs
    
    
    json.dump(lddata['graph'], open('graph_data.min.json', 'w'), separators=(',', ':'))
    
    json.dump(lddata['version'], open('version.min.json', 'w'), separators=(',', ':'))
    

    
    # print(list(entry['@id'] for entry in lddata['graph']))
    group = []
    for entry in lddata['graph']:
        try: 
            group.append(entry['@type'])
        except: print(entry)
    for i in set(group):
        print(i)
    # can try gziping too

# Create a new event loop and run the main coroutine until it completes
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
