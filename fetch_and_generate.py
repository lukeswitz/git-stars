import os
import requests
import json

# Fetch GitHub Stars
def fetch_github_stars(username, token):
    url = f'https://api.github.com/users/{username}/starred'
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    stars = response.json()
    
    while 'next' in response.links.keys():
        response = requests.get(response.links['next']['url'], headers=headers)
        stars.extend(response.json())
        
    return stars

# Generate Markdown Content
def generate_markdown(stars):
    markdown_lines = ["# GitHub Stars\n"]
    for repo in stars:
        markdown_lines.append(f"## [{repo['name']}]({repo['html_url']})\n")
        markdown_lines.append(f"{repo['description']}\n")
        markdown_lines.append(f"**Stars:** {repo['stargazers_count']} | **Language:** {repo['language']}\n")
        markdown_lines.append(f"**Last Updated:** {repo['updated_at']}\n")
        markdown_lines.append("\n---\n")
    return "\n".join(markdown_lines)

# Save Markdown to a file
def save_markdown(content, filepath):
    with open(filepath, 'w') as f:
        f.write(content)

def main():
    username = os.getenv('MY_GITHUB_USERNAME')
    token = os.getenv('RANDOKEY')
    if not username or not token:
        raise ValueError("MY_GITHUB_USERNAME and RANDOKEY environment variables must be set")

    stars = fetch_github_stars(username, token)
    markdown_content = generate_markdown(stars)
    save_markdown(markdown_content, 'index.md')
    print("Markdown file generated successfully.")

if __name__ == "__main__":
    main()
