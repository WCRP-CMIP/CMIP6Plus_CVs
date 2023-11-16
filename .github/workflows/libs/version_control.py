import json
from typing import Dict
from urllib import request

def last_commit(repo_owner: str, repo_name: str) -> Dict[str, str]:
    """
    Retrieve information about the latest commit of a GitHub repository.

    Args:
        repo_owner (str): Owner of the repository.
        repo_name (str): Repository name.

    Returns:
        dict: Dictionary containing details of the latest commit.
    """
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/commits'
    
    try:
        with request.urlopen(api_url) as response:
            if response.getcode() == 200:
                commits_data = json.loads(response.read().decode('utf-8'))
                if commits_data:
                    latest_commit = commits_data[0]
                    commit_info = {
                        "api_url": api_url,
                        "SHA": latest_commit["sha"],
                        "Message": latest_commit["commit"]["message"],
                        "Author": f"{latest_commit['commit']['author']['name']} <{latest_commit['commit']['author']['email']}>",
                        "Committer": f"{latest_commit['commit']['committer']['name']} <{latest_commit['commit']['committer']['email']}>",
                        "Date": latest_commit["commit"]["author"]["date"]
                    }
                    return commit_info
            else:
                print(f"Failed to retrieve data. Status code: {response.getcode()}")
    except Exception as e:
        print(f"An error occurred: {e}")