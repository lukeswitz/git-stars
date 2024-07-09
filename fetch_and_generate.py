import os
import requests

def fetch_github_stars(username, token):
    url = f'https://api.github.com/users/{username}/starred'
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    stars = response.json()
    
    while 'next' in response.links.keys():
        response = requests.get(response.links['next']['url'], headers=headers)
        stars.extend(response.json())
        
    return stars

def generate_markdown(stars):
    markdown_lines = ["# GitHub Stars\n"]
    for repo in stars:
        markdown_lines.append(f"## [{repo['name']}]({repo['html_url']})\n")
        markdown_lines.append(f"{repo['description']}\n")
        markdown_lines.append(f"**Stars:** {repo['stargazers_count']} | **Language:** {repo['language']}\n")
        markdown_lines.append(f"**Last Updated:** {repo['updated_at']}\n")
        markdown_lines.append("\n---\n")
    return "\n".join(markdown_lines)

def save_markdown(content, filepath):
    with open(filepath, 'w') as f:
        f.write(content)

def sort_repositories(stars, sort_by='stars'):
    # Example sorting by stars count
    stars_sorted = sorted(stars, key=lambda x: x['stargazers_count'], reverse=True)
    return stars_sorted

def filter_repositories(stars, min_stars=0, language=None):
    # Example filtering by minimum stars and optional language
    stars_filtered = [repo for repo in stars if repo['stargazers_count'] >= min_stars]
    if language:
        stars_filtered = [repo for repo in stars_filtered if repo['language'] == language]
    return stars_filtered

def search_repositories(stars, keyword):
    # Example searching by keyword in repository name or description
    stars_searched = [repo for repo in stars if keyword.lower() in repo['name'].lower() or 
                      (repo['description'] and keyword.lower() in repo['description'].lower())]
    return stars_searched

def main():
    username = os.getenv('MY_GITHUB_USERNAME')
    token = os.getenv('RANDOKEY')
    if not username or not token:
        raise ValueError("MY_GITHUB_USERNAME and RANDOKEY environment variables must be set")

    stars = fetch_github_stars(username, token)
    
    # Example usage of sort, filter, and search
    stars_sorted = sort_repositories(stars, sort_by='stars')
    stars_filtered = filter_repositories(stars_sorted, min_stars=1000, language='Python')
    stars_searched = search_repositories(stars_filtered, keyword='awesome')

    markdown_content = generate_markdown(stars_searched)
    save_markdown(markdown_content, 'index.md')
    print(markdown_content)

if __name__ == "__main__":
    main()
