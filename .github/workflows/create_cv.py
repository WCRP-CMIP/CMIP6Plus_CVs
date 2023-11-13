print('Create CV ')
import json
import os,re
from glob import glob
from urllib import request
from datetime import datetime, timedelta

from collections import OrderedDict

CV = OrderedDict()

###################################
# run script for testing actions 
###################################

'''
Github action test script:

export PATH="${HOME}/Applications/Docker.app/Contents/Resources/bin:$PATH"

act -s GITHUB_TOKEN="$(gh auth token)" --container-architecture linux/amd64 --verbose -b & sleep 4 &&


docker exec -it act-Generate-CV-file-create-branch-and-update-files-cabe81e196626eaf2f1a205b6f6f95341b0aa587d4d7127baba6ccfa7bef525a /bin/bash

docker exec -it act-Generate-CV-file-create-branch-and-update-files-cabe81e196626eaf2f1a205b6f6f95341b0aa587d4d7127baba6ccfa7bef525a /bin/bash -c "fq '.CV.table_id' CVs/CV.json";

-S /usr/bin/bash -c "cd .github/workflows/;python create_cv.py;cd ../../CVs;more CV.json;exit"

sudo apt-update
sudo apt install snapd
sudo snap install fx
fx CVs/CV.json


*note* interactive docker shell can use id or name as a reference. 
'''

###################################
# tunable parameters
###################################

relative = '../../'
cv_prefix = 'CMIP6Plus'
file_path = f'{relative}CVs/CV.json'

mip_tables = 'mip-cmor-tables'
table_prefix = 'MIP_'

pattern = re.compile(f'^{re.escape(table_prefix)}_*|\.json$')

###################################
# define functions
###################################

def read_contents_from_github(username, repo, directory, token=None):
    base_url = f"https://api.github.com/repos/{username}/{repo}/contents/{directory}"
    response = request.urlopen(base_url)
    json_data = json.loads(response.read().decode('utf-8'))

    return json_data
    # https://api.github.com/repos/PCMDI/mip-cmor-tables/contents/Tables

def read_json_from_github(username, repository, branch, path):
    raw_url = f'https://raw.githubusercontent.com/{username}/{repository}/{branch}/{path}'
    # response = requests.get(raw_url)

    response = request.urlopen(raw_url)
    json_data = json.loads(response.read().decode('utf-8'))

    return json_data


def listify(dictionary, keys):
    if not isinstance(keys, list): keys = [keys]
    for key in keys:
        if key in dictionary:
            if not isinstance(dictionary[key], list):
                dictionary[key] = [dictionary[key]]
    return dictionary

def notnull(dictionary, keys,replace='none'):
    if not isinstance(keys, list): keys = [keys]
    for key in keys:
        if key in dictionary:
            if isinstance(dictionary[key], list):
                dictionary[key] = [ str(i or replace) for i in dictionary[key]]
            print(key)
    return dictionary





###################################
# read from mip tables
###################################


for key in 'source_type frequency realm grid_label'.split():

    CV={**CV,**read_json_from_github('PCMDI', mip_tables, 'additional_tables', f'{table_prefix}{key}.json')}

institutions = read_json_from_github('PCMDI', mip_tables, 'additional_tables', f'{table_prefix}institutions.json')



###################################
# read from CMIP6Plus
###################################


structure = ['required_global_attributes',
 'version_metadata',
 'license',
 'activity_id',
 'institution_id',
 'source_id',
 'source_type',
 'frequency',
 'grid_label',
 'nominal_resolution',
 'realm',
 'table_id',
 'DRS',
 'mip_era',
 'sub_experiment_id',
 'experiment_id',
 'product',
 'tracking_id',
#  'further_info_url',
 'realization_index',
 'variant_label',
 'data_specs_version',
 'Conventions',
 'forcing_index',
 'initialization_index',
 'physics_index']




###################################
# main section
###################################
f = open(file_path, 'w')


for entry in structure:
    file = f"{relative}{cv_prefix}_{entry}.json"

    if entry == 'table_id':
            # extract tables using github api
            CV['table_id'] = [ pattern.sub('', t.get('name')) for t in read_contents_from_github('PCMDI',mip_tables,'Tables') ]


    elif os.path.exists(os.path.abspath(file)):


        CV[entry] = json.load(open(os.path.abspath(file),'r'))[entry]

        if 'experiment_id' in entry:

            # select only those that appear
            CV['source_type'] = list(set(CV['source_type']).union(set(component for experiment in CV[entry].values() if "required_model_components" in experiment for component in experiment["required_model_components"]+experiment["additional_allowed_model_components"])))
    
                            
            if entry == 'experiment_id':

                CV[entry] = listify(CV[ entry],['parent_experiment_id','parent)sub_experiment_id','parent_activity_id'])

                CV[entry] = notnull(CV[entry],['parent_experiment_id','parent)sub_experiment_id'], 'no parent')

        elif entry == 'activity_id':
            CV[entry] = {f"{key}": value["long_name"] for key, value in CV[entry].items()}


        elif entry == 'source_id':
            # this section updates the institutions

            CV['institution_id'] = {i: f"{institutions[i]['indentifiers']['ror']} - {institutions[i]['indentifiers']['institution_name']}" for i in sorted(
                {component for source in CV[entry].values() for component in source.get("institution_id", [])})}
            
            for model in CV[entry]:
                model_info = CV[entry][model]
                components = []
                for component, info in model_info['model_component'].items():
                    
                    description = info.get("description", "none")
                    components.append(f"{component}: {description}")

                components_str = "\n".join(components)

                CV[entry][model]['source'] = f"{model_info['source_id']} ({model_info['release_year']}: \n{components_str})"

                for d in 'model_component release_year label label_extended'.split():
                    del CV[entry][model][d]






#         elif entry in template:
#             CV[entry] = template[entry]

#         else:
#             missing.append(entry)

#     #  final check
#     diff = set(missing) - set(CV)

#     if diff:
#         raise core.stdout.MissingValueError(
#             f'The following fields are required:{diff} ')

#     core.stdout.MissingValueError(f'The following fields are required:{diff} ')




del CV['version_metadata']

# Order the keys alphabetically
# CV = {k: CV[k] for k in sorted(CV)}

sorted_keys = sorted(CV.keys(), key=lambda x: x.lower())
# f.write(str(sorted_keys))
# Creating a new OrderedDict with sorted keys
CV = { "CV" : OrderedDict((key, CV[key]) for key in sorted_keys) }



###################################
# metadata
###################################


CV['version_metadata'] = {
    "file_updated" : datetime.utcnow().strftime("%A %B %d %H:%M UTC"),
    "CVs"          : { "updated"  : '', "tag" :'', "commit":'' },
    'MIP tables'   : { "updated"  : '', "tag" :'', "commit":'' },
    "autogenerated" : 'True'
}



# Write the JSON data to the file with an indentation of 4 spaces and sorted keys

json.dump(CV, f, indent=4, sort_keys=False)
f.close()
