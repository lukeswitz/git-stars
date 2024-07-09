import os
import requests
from datetime import datetime

def fetch_github_stars(username, token):
    """
    Fetches all starred repositories for a given GitHub user.

    Args:
    - username (str): GitHub username
    - token (str): Personal access token with 'repo' scope

    Returns:
    - list: List of dictionaries representing starred repositories
    """
    url = f'https://api.github.com/users/{username}/starred'
    headers = {'Authorization': f'token {token}'}
    stars = []

    try:
        # Fetch the first page of starred repositories
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for non-2xx responses
        stars.extend(response.json())

        # Paginate through additional pages if they exist
        while 'next' in response.links.keys():
            response = requests.get(response.links['next']['url'], headers=headers)
            response.raise_for_status()  # Raise exception for non-2xx responses
            stars.extend(response.json())

        return stars

    except requests.exceptions.RequestException as e:
        print(f"Error fetching GitHub stars: {e}")
        return None

def sort_and_filter(stars, sort_by='stars', language=None):
    """
    Sorts and filters the list of starred repositories.

    Args:
    - stars (list): List of dictionaries representing starred repositories
    - sort_by (str): Field to sort by ('stars', 'name', 'updated_at')
    - language (str): Language to filter by

    Returns:
    - list: Sorted and filtered list of repositories
    """
    if not stars:
        return []

    # Filter by language if specified
    if language:
        stars = [repo for repo in stars if repo['language'] == language]

    # Sort by specified field
    if sort_by == 'stars':
        stars.sort(key=lambda x: x['stargazers_count'], reverse=True)
    elif sort_by == 'name':
        stars.sort(key=lambda x: x['name'].lower())
    elif sort_by == 'updated_at':
        stars.sort(key=lambda x: datetime.strptime(x['updated_at'], '%Y-%m-%dT%H:%M:%SZ'), reverse=True)

    return stars

def search_stars(stars, keyword):
    """
    Searches through starred repositories by matching keyword against repository names and descriptions.

    Args:
    - stars (list): List of dictionaries representing starred repositories
    - keyword (str): Keyword to search for in repository names and descriptions

    Returns:
    - list: Filtered list of repositories matching the search keyword
    """
    if not stars or not keyword:
        return []

    keyword = keyword.lower()
    return [repo for repo in stars if keyword in repo['name'].lower() or (repo['description'] and keyword in repo['description'].lower())]

def generate_markdown(stars):
    """
    Generates Markdown content from a list of starred repositories.

    Args:
    - stars (list): List of dictionaries representing starred repositories

    Returns:
    - str: Markdown content
    """
    if not stars:
        return ""

    markdown_lines = ["# GitHub Stars\n"]
    for repo in stars:
        markdown_lines.append(f"## [{repo['name']}]({repo['html_url']})\n")
        markdown_lines.append(f"{repo['description']}\n")
        markdown_lines.append(f"**Stars:** {repo['stargazers_count']} | **Language:** {repo['language']}\n")
        markdown_lines.append(f"**Last Updated:** {repo['updated_at']}\n")
        markdown_lines.append("\n---\n")
    return "\n".join(markdown_lines)

def save_markdown(content, filepath):
    """
    Saves Markdown content to a file.

    Args:
    - content (str): Markdown content to be saved
    - filepath (str): Filepath where the content will be saved
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Markdown content saved to {filepath}")

    except IOError as e:
        print(f"Error saving markdown content: {e}")

def main():
    """
    Main function to fetch GitHub stars, apply sorting, filtering, search, generate Markdown, and save to file.
    """
    username = os.getenv('MY_GITHUB_USERNAME')
    token = os.getenv('RANDOKEY')
    if not username or not token:
        raise ValueError("MY_GITHUB_USERNAME and RANDOKEY environment variables must be set")

    stars = fetch_github_stars(username, token)
    if stars is None:
        print("Failed to fetch GitHub stars. Check your credentials and network connection.")
        return

    # Sort by stars count in descending order, filter by Python language
    sorted_stars = sort_and_filter(stars, sort_by='stars', language='Python')

    # Search for repositories containing 'library' in name or description
    search_results = search_stars(sorted_stars, 'library')

    markdown_content = generate_markdown(search_results)
    if markdown_content:
        save_markdown(markdown_content, 'index.md')
    else:
        print("No GitHub stars found matching search criteria or unable to generate markdown content.")

if __name__ == "__main__":
    main()
