print('Create CV ')
import json
import os
from glob import glob
from urllib import request
from datetime import datetime, timedelta



###################################
# run script for testing actions 
###################################

'''
Github action test script:

 act -s GITHUB_TOKEN="$(gh auth token)" --container-architecture linux/amd64 -vact -s GITHUB_TOKEN="$(gh auth token)" --container-architecture linux/amd64 --verbose;
docker exec -it act-Generate-CV-file-create-branch-and-update-files-cabe81e196626eaf2f1a205b6f6f95341b0aa587d4d7127baba6ccfa7bef525a /usr/bin/bash -c "cd .github/workflows/;python create_cv.py;cd ../../CVs;more CV.json;exit"

*note* interactive docker shell can use id or name as a reference. 
'''

###################################
# tunable parameters
###################################

relative = '../../'
cv_prefix = 'CMIP6Plus'
file_path = f'{relative}CVs/CV.json'
sort_keys = True


###################################
# define functions
###################################

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




CV = {}
for key in 'source_type frequency realm grid_label'.split():

    CV={**CV,**read_json_from_github('PCMDI', 'mip-cmor-tables', 'additional_tables', f'MIP_{key}.json')}

institutions = read_json_from_github('PCMDI', 'mip-cmor-tables', 'additional_tables', f'MIP_institutions.json')



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
    
            CV['table_id'] = ['APmon']
            # [t.split('/')[-1].rstrip('.json') for t in glob(f'{tables}/Tables/*.json')]
        # ['APmon']



    elif os.path.exists(os.path.abspath(file)):


        CV[entry] = json.load(open(os.path.abspath(file),'r'))[entry]

        if 'experiment_id' in entry:

            # select only those that appear
            CV['source_type'] = list(set(CV['source_type']).union(set(component for experiment in CV[entry].values() if "required_model_components" in experiment for component in experiment["required_model_components"]+experiment["additional_allowed_model_components"])))
    
                            
            if entry == 'experiment_id':

                CV[entry] = listify(CV[ entry],['parent_experiment_id','parent)sub_experiment_id','parent_activity_id'])

                CV[entry] = notnull(CV[entry],['parent_experiment_id','parent)sub_experiment_id'], 'no parent')

        if entry == 'source_id':
            # this section updates the institutions

            CV['institution_id'] = {i: f"{institutions[i]['indentifiers']['ror']} - {institutions[i]['indentifiers']['institution_name']}" for i in sorted(
                {component for source in CV[entry].values() for component in source.get("institution_id", [])})}
            
            del CV['institutions']


                


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

#     #  update this to the correct format.
#     CV['source_type'] = dict([[s, source_type[s]]
#                                  for s in CV['source_type']])
#     print(CV['source_type'])
#     CV = prune(CV)

#     CVfile = f"{directory}{outloc}/{core.io.ensure_suffix(prefix,'_')}CV.json"
#     core.io.json_write(dict(CV=CV), CVfile, sort=True)

#     return CVfile






# Order the keys alphabetically
# CV = {k: CV[k] for k in sorted(CV)}


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

json.dump(CV, f, indent=4, sort_keys=sort_keys)
f.close()
