import urllib.request
import json
from collections import OrderedDict
import sys,os,time
from _functions import fetch_json_from_github, airtable_record
import argparse

#  arguments

parser = argparse.ArgumentParser(description='Process Airtable key and JSON string')
parser.add_argument('-k','--airtable-key', help='Airtable API key', required=True)
parser.add_argument('-r','--record', help='airtable record', required=True)

args = parser.parse_args()

# https://api.airtable.com/v0/{baseId}/{tableIdOrName}/{recordId}



# definitions
prefix = 'CMIP6Plus'
base,table = 'appaZflpqbFjA6pwV/tblsD56Ic2mHoAiTz'.split('/')
api_key=args.airtable_key
record = args.record

data = airtable_record(base,table,api_key,record)

# recursively get linked records. 
for i in data:
    if isinstance(data[i],list):
        data[i] = [airtable_record(base,table,api_key,rc)  if rc[:3] == 'rec' else rc  for rc in data[i]]

model_components = OrderedDict()
component_list = [
 'aerosol',
 'atmos',
 'atmosChem',
 'land',
 'landIce',
 'ocean',
 'ocnBgchem',
 'seaIce'
 ]

# sort out the model components
for c in component_list:
    cdummy = data[c][0]
    model_components[c] = OrderedDict({"description": cdummy.get('description','none'),
                         "native_nominal_resolution": cdummy.get('resolution','none') })

license = data['license(automated)'][0]

# create the template. 
template = OrderedDict(
    {
            "activity_participation": [x['Name'] for x in data.get('activity_id', [])],
            "cohort": [
                "unknown"
            ],
            "institution_id": [x['Name'] for x in data.get('Source Institution', [])],
            "label": data['label'],
            "label_extended": data['label_extended'],
            "license_info": OrderedDict({

                "id": license['id'],
                "license": license['license_id'],
                "url": license['license_url'],
                "exceptions_contact": "@%s <- %s"%tuple(data['license_exceptions_contact'].split('@')[::-1]),
                "history": data.get('license_history',''),
                "source_specific_info": data.get("source_specific_info",''),
                
            }),
            "model_component": model_components,
            "release_year": data['release_year'],
            "source_id": data['source_id']
        }
)

# print output for diagnostics. 
formatted = json.dumps(template, indent=4)
print(formatted)


# update existing file
filename = f'{prefix}_source_id.json'
with open(filename,'r') as f:
    
    source = json.load(f)
    source['source_id'][data['source_id']] = template
            
    newid = OrderedDict()
    for s in sorted(source['source_id']):
        newid[s] = source['source_id'][s]

    source['source_id'] = newid
    
# write to file
with open(filename,'w') as f:
    json.dump(source, indent=4)
    