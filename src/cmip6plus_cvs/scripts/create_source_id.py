


import requests
import json
import os
from pprint import pp
# URLs of the JSON files on GitHub
json_url2 = 'https://raw.githubusercontent.com/WCRP-CMIP/CMIP6Plus_CVs/refs/heads/main/CMIP6Plus_source_id.json'
# Already adapted to jsonld here
jsonld_url3 = 'https://raw.githubusercontent.com/WCRP-CMIP/CMIP6Plus_CVs/refs/heads/jsonldIII/JSONLD/source/id/graph.jsonld '

# But .. not in main 
# + only 6 .. not entire Universe
# so useable to check the final data to save ? 


# Directory where the JSON files will be saved
save_dir = 'source_id'

# Create the directory if it doesn't exist
os.makedirs(save_dir, exist_ok=True)

# Function to fetch and load JSON data from a URL
def fetch_json(url):
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors
    return response.json()

# Fetch the JSON data from both URLs
data2 = fetch_json(json_url2)

# Extract the experiment_id dictionaries from both JSON files
ids2 = data2.get('source_id', {})

# Merge both datasets into a single dictionary
#_dict = ids1 | ids2
_dict = ids2

#pp(_dict)

#pp(_dict.keys())

knownK = []

for key, value in _dict.items():
    print("source :", key)
    data={}
    data['@context']='000_context.jsonld'
    data['id']=key.lower()
    data['type']="source"

    file_path = os.path.join(save_dir, f"{key.lower()}.json")
    with open(file_path, 'w') as f:
        print("   save :",key)
        json.dump(data, f, indent=4)
print(knownK)
print("source files saved to", save_dir)

    


context = {
     
      "@context": {
        "id":"@id",
        "type":"@type",
      "@base":"https://espri-mod.github.io/mip-cmor-tables/source/",
      "source":"https://espri-mod.github.io/mip-cmor-tables/source"}
    }
file_path = os.path.join(save_dir, "000_context.jsonld")
with open(file_path, 'w') as f:
    json.dump(context, f, indent=4)



