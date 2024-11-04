import glob
import json 
from collections import OrderedDict
import os
import subprocess





remote_url = subprocess.check_output(["git", "remote", "get-url", "origin"], text=True).strip()
user_repo = remote_url.split("github.com")[-1].replace(":", "/").replace(".git", "").strip("/")
pages_url = f"https://{user_repo.split('/')[0]}.github.io/{user_repo.split('/')[1]}"

# print(remote_url)
# print(user_repo)
# print(pages_url)
# https://github.com/WCRP-CMIP/WCRP-UNIVERSE.git
# WCRP-CMIP/WCRP-UNIVERSE
# https://WCRP-CMIP.github.io/WCRP-UNIVERSE


folders = glob.glob('*/')


for folder in folders:
    print(folder)
    files = glob.glob(folder + '*.json')
    try:
        for file in files:
            with open(file, 'r') as f:
                
                js = json.load(f)
                
                if '@type' not in js: 
                    continue
                js['id'] = file.split('/')[-1]
                js['type'] = js['@type'].replace('-', '_')
                js['@context'] = f'{pages_url}/data_descriptors/{folder}_context'
                del js['@type'], js['@id']
                
                js = OrderedDict(sorted(js.items()))
                
            
            json.dump(js, open(file,'w') , indent=4)
            # print(file)
    except: 
        continue    
        
    # context new file
    location = f"{pages_url}/data_descriptors/{folder}"
    context = {
        
        "@context": {
            "@base": location,
            "@vocab": location,
            "id": "@id",
            "type": "@type"
        },
        "@embed": "@always"
        }
                    
    json.dump(context, open(f"{folder}_context.json", 'w'), indent=4)
    
    
    os.system('rm -f ' + folder + '*.jsonld')
       