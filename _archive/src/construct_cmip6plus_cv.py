from copy import deepcopy
import glob
import json
import os
import sys

from cv_checksums import calculate_checksum, validate_checksum


def get_mip_era(cv_directory):
    filenames = glob.glob(os.path.join(cv_directory, '*_mip_era.json'))
    if not len(filenames) == 1:
        raise RuntimeError('Found multiple mip era files: {}'.format(repr(filenames)))
    
    with open(filenames[0]) as fhandle:
        mip_era_data = json.load(fhandle)
    
    validate_checksum(mip_era_data)
    
    mip_era = mip_era_data['mip_era']
    return mip_era


def main():
    # lazy, should replace with argparse
    location = sys.argv[1]
    if not os.path.exists(location):
        raise RuntimeError('Location "{}" not found'.format(location))
    # get MIP era
    mip_era = get_mip_era(location)
    # look for CV files
    json_files_in_location = glob.glob(os.path.join(location, '{}*.json'.format(mip_era)))
    
    
    if not len(json_files_in_location) > 1:
        raise RuntimeError('Could not find more one JSON file in location "{}"'.format(location))
    
    output_dictionary = {}
    checksums = {}
    for filename in json_files_in_location:

        with open(filename) as fhandle:
            file_data = json.load(fhandle)
        if filename.endswith('_CV.json'):
            previous_cv_checksum = file_data['version_metadata']['checksum']
            checksums['previous {}'.format(os.path.basename(filename))] = previous_cv_checksum
            continue
        checksums[os.path.basename(filename)] = file_data['version_metadata']['checksum']
        
        if 'experiment_id' in file_data:
            strip_experiment_id_info(file_data)
        elif 'source_id' in file_data:
            strip_source_id_info(file_data)
        
        for entry in file_data:
            if entry != 'version_metadata':
                output_dictionary[entry] = file_data[entry]
        
        
            
    
    # add version_metadta from last file -- may need to be updated depending on processes
    output_dictionary['version_metadata'] = file_data['version_metadata']
    output_dictionary['version_metadata']['file_checksums'] = checksums
    calculate_checksum(output_dictionary)
    
    output_file_name = os.path.join(location, '{}_CV.json'.format(mip_era))
    with open(output_file_name, 'w') as fhandle:
        json.dump(output_dictionary, fhandle, indent=2, sort_keys=True)


EXPERIMENT_ID_FIELDS_FOR_CV_FILE = [
    'activity_id', 'additional_allowed_model_components', 'experiment', 'experiment_id', 
    'parent_activity_id', 'parent_experiment_id', 'required_model_components', 'sub_experiment_id',
]

def strip_experiment_id_info(experiment_id_file_data):
    experiment_id_info = experiment_id_file_data['experiment_id']
    for experiment_id, info in experiment_id_info.items():
        fields_to_delete = [i for i in info if i not in EXPERIMENT_ID_FIELDS_FOR_CV_FILE]
        for field in fields_to_delete:
            del info[field]
        

SOURCE_ID_FIELDS_FOR_CV_FILE = [
    "activity_participation", "cohort", "institution_id", "license_info", "source", "source_id"
]

def strip_source_id_info(source_id_file_data):
    
    source_id_info = source_id_file_data['source_id']
    source_ids = source_id_info.keys()
    for source_id in source_ids:
        info = source_id_info[source_id]
        component_string = '\n'.join(['{}: {}'.format(k, v['description']) for k,v in info['model_component'].items()])
        # had problems with strange source strings here, so take a copy of the dictionary modify that and then overwrite
        new_info = deepcopy(info)
        new_info['source'] = '{} ({}): \n{}'.format(info['label'], info['release_year'], component_string)
        fields_to_delete = [i for i in new_info if i not in SOURCE_ID_FIELDS_FOR_CV_FILE]
        for field in fields_to_delete:
            del new_info[field] 
        source_id_info[source_id] = new_info


if __name__ == '__main__':
    main()

        
    
                        



