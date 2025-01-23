# for now Nov2024 the idea for institution, varible and table is that everything is possible for cmip6plus 
# therefore it is just a copy of the universe with only id inside 



import requests,os,json

def list_files_in_branch(repo_owner, repo_name, directory_path, branch_name, token=None):
    """
    List files in a GitHub directory for a specific branch.

    Args:
        repo_owner (str): Owner of the repository (username or organization name).
        repo_name (str): Name of the repository.
        directory_path (str): Path to the directory in the repo.
        branch_name (str): Name of the branch.
        token (str, optional): GitHub Personal Access Token for authentication.

    Returns:
        list: A list of file names in the directory.
    """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{directory_path}"
    headers = {}

    if token:
        headers["Authorization"] = f"token {token}"

    # Add the branch as a query parameter
    params = {"ref": branch_name}
    print(url)
    print(params)

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        contents = response.json()
        files = [item["name"] for item in contents if item["type"] == "file"]
        return files
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

repo_owner = "ESPRI-Mod"  # Replace with the repository owner's username
repo_name = "mip-cmor-tables"  # Replace with the repository name
branch_name = "uni_proj_ld"  # Replace with your branch name



todo = ["organisation", "variable","table"]

for directory_path in todo:


    save_dir = ""
    match directory_path:
        case "organisation":
            save_dir = "institution_id"
        case "variable": 
            save_dir = "variable_id"
        case "table" : 
            save_dir = "table_id"
        case _:
            print("PROBLEM")
            #return

    os.makedirs(save_dir, exist_ok=True)


#directory_path = "organisation"  # Root directory or specify a sub-directory path
    files = list_files_in_branch(repo_owner, repo_name, directory_path, branch_name, None)
    print("Files in branch:", branch_name, "directory:", files)
    
    for file in files:
        if file != "000_context.jsonld":
            id = file.split(".")[0] 

            if directory_path=="grid_label":
                directory_path = "grid" 
            data = {
                "@context": "000_context.jsonld",
                "id": id,
                "type": directory_path
            }
            
            file_path = os.path.join(save_dir, f"{data["id"]}.json")
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
        else: #it is the context

            context = {
     
                "@context": {
                "id":"@id",
                "type":"@type",

                "@base":f"https://espri-mod.github.io/mip-cmor-tables/{directory_path}/",
                f"{directory_path}":f"https://espri-mod.github.io/mip-cmor-tables/{directory_path}"
                }
                
            }

            file_path = os.path.join(save_dir, "000_context.jsonld")
            with open(file_path, 'w') as f:
                json.dump(context, f, indent=4)


