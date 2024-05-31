''' 
A python script to go through each JSONld file and extract the information. 
Rules; 
- no "_" in category names!



'''
import asyncio
import glob
import os
import json
from pprint import pprint
from tqdm import tqdm


repo = os.popen('git remote get-url origin').read().replace('.git','/JSONLD/').strip()
print(repo)


async def githistory(file,root):
    rtn = os.popen('git log -n 1 --pretty=format:\'{"commit": "%h", "message": "%s", "date": "%cd"}\' --date=iso-strict -- '+root+'/'+file).read()
    print('aa',file,rtn,'git log -n 1 --pretty=format:\'{"commit": "%h", "message": "%s", "date": "%cd"}\' --date=iso-strict -- '+root+'/'+file)
    
    update = json.loads(rtn)
    # version = {"file":file,**update}
    return update



async def read_json_file(file_path):
    with open(file_path, mode='r') as f:
        content = f.read()
        return json.loads(content)

async def read_json_files(file_paths):
    tasks = [read_json_file(file_path) for file_path in file_paths]
    return await asyncio.gather(*tasks)

async def categorize_files(directory):
    
    context_files = []
    graph_data=[]

    for root, dirs, files in os.walk(directory):
        # print(root,dirs,files)
        print('d',root.replace('../',repo),files)
        skip = ['schema.json','graph.json', ".DS_Store",
        "create.ipynb"]
        for skipfile in skip:
            if skipfile in files:
                files.remove(skipfile)
                
        if 'context.json' in files:
            context_file_path = os.path.join(root, 'context.json')
            context_files.append(context_file_path)
            vocab = await read_json_file(root+'/context.json')
            vocab = vocab.get('@vocab','')
            files.remove("context.json")
        
            # Also add all JSON files in this directory to graph_files
            graph_files = (os.path.join(root, file) for file in files if file.endswith('.json') and not file.endswith('context.json'))
            
            
            graph_data = await read_json_files(graph_files) 
            
            complete_graph = {
                "@id":root.replace('../',repo),
                "@type": "cmip:graph",
                '@vocab':vocab,
                "ldroot":root[1:],
                "files": {"@nest":[await githistory(f,root) for f in files]},
                "@graph": graph_data
            }
            
            # write
            json.dump(complete_graph, open(f"{root}/graph.json",'w') , indent=4)
                
                
            


    
    
    
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
    
    return {'graph': complete_graph, 'context': context_data}

async def main():
    lddata = await categorize_files('../')

    # Dumping the contents of each category to separate files
    json.dump(lddata['graph'], open('graph_data.json', 'w'), indent=4)
    json.dump(lddata['context'], open('context_data.json', 'w'), indent=4)
    
    json.dump(lddata['graph'], open('graph_data.min.json', 'w'), separators=(',', ':'))
    

    
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
