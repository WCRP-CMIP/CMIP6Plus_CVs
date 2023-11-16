import os,json
from typing import Dict
from urllib import request

def get_latest_commit(repo_owner: str, repo_name: str) -> Dict[str, str]:
    """
    Retrieve information about the latest commit of a GitHub repository using GITHUB_TOKEN.

    Args:
        repo_owner (str): Owner of the repository.
        repo_name (str): Repository name.

    Returns:
        dict: Dictionary containing details of the latest commit.
    """
    try:
        # Access the GITHUB_TOKEN directly within the GitHub Actions environment
        github_token = os.environ.get("GITHUB_TOKEN")
        if not github_token:
            print("GITHUB_TOKEN not available.")
            # return {}
            headers = {}
        else:
            headers = {"Authorization": f"Bearer {github_token}"}

        api_url_commits = f'https://api.github.com/repos/{repo_owner}/{repo_name}/commits'
        

        api_url = f'https://www.github.com/repos/{repo_owner}/{repo_name}'

        with request.urlopen(request.Request(api_url_commits, headers=headers)) as response:
            if response.getcode() == 200:
                commits_data = json.loads(response.read().decode('utf-8'))
                if commits_data:
                    latest_commit = commits_data[0]
                    commit_info = {
                        "SHA": latest_commit["sha"],
                        "Message": latest_commit["commit"]["message"],
                        "Author": f"{latest_commit['commit']['author']['name']} <{latest_commit['commit']['author']['email']}>",
                        "Committer": f"{latest_commit['commit']['committer']['name']} <{latest_commit['commit']['committer']['email']}>",
                        "Date": latest_commit["commit"]["author"]["date"]
                    }
                else:
                    commit_info = {}
            else:
                print(f"Failed to retrieve commit data. Status code: {response.getcode()}")
                return {}

        api_url_releases = f'https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest'
        with request.urlopen(request.Request(api_url_releases, headers=headers)) as response:
            if response.getcode() == 200:
                release_data = json.loads(response.read().decode('utf-8'))
                if release_data:
                    tag_info = {
                        "TagName": release_data["tag_name"],
                        "ReleaseName": release_data.get("name", ""),
                        "ReleaseBody": release_data.get("body", ""),
                        "ReleaseDate": release_data["published_at"]
                    }
                else:
                    tag_info = {}
            else:
                print(f"Failed to retrieve release data. Status code: {response.getcode()}")
                return {}

        return {**commit_info,**tag_info,**{'url':api_url}}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}




# # Example usage
# repo_owner = ''
# repo_name = ''
# result = get_latest_commit(repo_owner, repo_name)

# if result:
#     print("Latest Commit Information:")
#     commit_info = result.get("CommitInfo", {})
#     for key, value in commit_info.items():
#         print(f"{key}: {value}")

#     print("\nLatest Tag Release Information:")
#     tag_info = result.get("TagInfo", {})
#     for key, value in tag_info.items():
#         print(f"{key}: {value}")