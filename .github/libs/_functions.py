

import urllib.request
import json
from collections import OrderedDict
import sys,os

import os,json,time
from typing import Dict,Any
from urllib import request


def sort_dict_recursive(input_dict):
    if isinstance(input_dict, dict):
        return OrderedDict((key, sort_dict_recursive(value)) for key, value in sorted(input_dict.items()))
    elif isinstance(input_dict, list):
        return [sort_dict_recursive(item) for item in input_dict]
    else:
        return input_dict
    
def airtable_request(base_id,table_name,view_name,api_key):
    url = f'https://api.airtable.com/v0/{base_id}/{table_name}?view={view_name}'
    # Set up headers with your Airtable API key
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    # Create a request with headers
    request = urllib.request.Request(url, headers=headers)
    return request


def airtable_record(base,table,api_key,record):
    url = f'https://api.airtable.com/v0/{base}/{table}/{record}'
    # Set up headers with your Airtable API key
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    time.sleep(.1)
    # Create a request with headers
    request = urllib.request.Request(url, headers=headers)


    with urllib.request.urlopen(request) as response:
        # Process the response as needed
        if response.status == 200:
            data = json.loads(response.read().decode('utf-8'))['fields']
            return data



def fetch_json_from_github(username, repo, path):
    try:
        # Construct the raw JSON URL
        raw_json_url = f"https://raw.githubusercontent.com/{username}/{repo}/main/{path}"
    # https://raw.githubusercontent.com/PCMDI/mip-cmor-tables/main/Auxillary_files/MIP_model_components.json
        # Make a GET request to fetch the raw content
        with urllib.request.urlopen(raw_json_url) as response:
            # Check if the request was successful (status code 200)
            if response.getcode() == 200:
                # Read the content
                raw_data = response.read().decode('utf-8')

                # Parse the JSON content
                json_data = json.loads(raw_data)

                # Return the parsed JSON data
                return json_data
            else:
                # Print an error message if the request was not successful
                print(f"Failed to fetch data. Status code: {response.getcode()}")
    except Exception as e:
        # Handle any exceptions that might occur during the request or parsing
        print(f"An error occurred: {e}")

        


def get_latest_commit(repo_owner: str, repo_name: str, github_token: str) -> Dict[str,Any]:
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
        # github_token = api
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
