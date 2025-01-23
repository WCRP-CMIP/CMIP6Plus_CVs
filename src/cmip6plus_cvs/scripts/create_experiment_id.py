

import requests
import json
import os

# URLs of the JSON files on GitHub
#json_url1 = 'https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/main/CMIP6_experiment_id.json'
json_url2 = 'https://raw.githubusercontent.com/WCRP-CMIP/CMIP6Plus_CVs/main/CMIP6Plus_experiment_id.json'

# Directory where the JSON files will be saved
save_dir = 'experiment_id'

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
experiment_ids2 = data2.get('experiment_id', {})
print(experiment_ids2)
# Create a dictionary with experiment ID as key and a dictionary with long_name and url set to None
for key,_ in experiment_ids2.items():

    experiment_dict = {
        "@context":"000_context.jsonld",
        "id" : key.lower(),
        "type":"experiment"
    }
    file_path = os.path.join(save_dir, f"{key.lower()}.json")
    with open(file_path, 'w') as f:
        json.dump(experiment_dict, f, indent=4)

#
# # Save each experiment as an individual JSON file
# for key, value in experiment_dict.items():
#     experiment_data = {
#         '@context': "000_context.jsonld",
#         'type':'experiment',
#         'id': key.lower(),
#         'name': key,
#         'cmip_acronym': key,
#         'long_name': value['long_name'],
#         'url': value['url']
#     }
#     file_path = os.path.join(save_dir, f"{key.lower()}.json")
#     with open(file_path, 'w') as f:
#         json.dump(experiment_data, f, indent=4)

print("experiment files saved to", save_dir)

context = {
    "@context": {
    "id": "@id",
    "type": "@type",
    "@base": "https://espri-mod.github.io/mip-cmor-tables/experiment/",
    "experiment": "https://espri-mod.github.io/mip-cmor-tables/experiment"
    
  }
}
file_path = os.path.join(save_dir, "000_context.jsonld")
with open(file_path, 'w') as f:
        json.dump(context, f, indent=4)
