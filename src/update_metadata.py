import json
from  cv_checksums import calculate_checksum
import os

FILES = [
    'CMIP6Plus_DRS.json', 
    'CMIP6Plus_experiment_id.json', 
    'CMIP6Plus_mip_era.json', 
    'CMIP6Plus_required_global_attributes.json', 
    'CMIP6Plus_sub_experiment_id.json', 
    'CMIP6Plus_activity_id.json', 
    'CMIP6Plus_license.json', 
    'CMIP6Plus_product.json', 
    'CMIP6Plus_source_id.json', 
    'CMIP6Plus_tracking_id.json']

new_version = "v6.5.2.0"
collection = {
    "CV_collection_version": new_version,
    "CV_collection_modified": "2024-12-12T11:32:12Z",
    "CV_collection_release": "https://github.com/WCRP-CMIP/CMIP6Plus_CVs/releases/tag/{}".format(new_version),
    "specs_doc": "v6.5.0"
}

for filename in FILES:
    with open(filename) as fh:
        data = json.load(fh)
    data['Header']['collection'] = collection
    calculate_checksum(data,checksum_location="file")
    with open(filename, 'w') as fh:
        json.dump(data, fh, indent=4, sort_keys=False)#, separators=(',', ':'))