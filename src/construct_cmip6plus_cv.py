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
        checksums[os.path.basename(filename)] = file_data['version_metadata']['checksum']
        
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


if __name__ == '__main__':
    main()

        
    
                        



