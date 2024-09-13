import cmipld
import cmipld.utils.git
base = cmipld.utils.git.toplevel()

print(base)

lddata = cmipld.CMIPFileUtils.load(['mip_cmor_tables_ld',base + '/compiled/graph_data.min.json'])


#  cmipld.sync(lddata)




''' Export out! '''


import subprocess
import hashlib, json


def get_md5_checksum(input_string):
    # Create an MD5 hash object
    md5_hash = hashlib.md5()
    
    # Encode the input string and update the hash object
    md5_hash.update(input_string.encode('utf-8'))
    
    # Return the hexadecimal digest of the hash
    return md5_hash.hexdigest()

def finalise(data,name):
    
    datastr = json.dumps(data, indent=4),
    
    # Get the current version tag (if any)
    version_tag = subprocess.check_output(["git", "describe", "--tags", "--abbrev=0"]).strip().decode()
    # Get the latest commit hash
    commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode()
    # Get the previous commit hash
    previous_commit = subprocess.check_output(["git", "rev-parse", "HEAD~1"]).strip().decode()
    # Get the latest commit message
    commit_message = subprocess.check_output(["git", "log", "-1", "--pretty=%B"]).strip().decode()
    # Get the date of the latest commit
    commit_date = subprocess.check_output(["git", "log", "-1", "--pretty=%cd", "--date=rfc"]).strip().decode()

    checksum = get_md5_checksum(str(datastr))
    content = {}
    content[name] = data

    content['version_metadata'] =  {
        "version_tag": version_tag,
        "checksum": checksum,
        "commit": commit_hash,
        "previous_commit": previous_commit,
        f"{name}_modified": commit_date,
        f"{name}_note": commit_message
    }
    
    return content
    
