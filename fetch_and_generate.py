import os
import requests

def fetch_github_stars(username, token):
    url = f'https://api.github.com/users/{username}/starred'
    headers = {'Authorization': f'token {token}'}
    stars = []

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for non-2xx responses
        stars.extend(response.json())

        while 'next' in response.links.keys():
            response = requests.get(response.links['next']['url'], headers=headers)
            response.raise_for_status()  # Raise exception for non-2xx responses
            stars.extend(response.json())

    except requests.exceptions.RequestException as e:
        print(f"Error fetching GitHub stars: {e}")
        return None

    return stars

def generate_markdown(stars):
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
    try:
        with open(filepath, 'w') as f:
            f.write(content)
    except IOError as e:
        print(f"Error saving markdown content: {e}")

def main():
    username = os.getenv('MY_GITHUB_USERNAME')
    token = os.getenv('RANDOKEY')
    if not username or not token:
        raise ValueError("MY_GITHUB_USERNAME and RANDOKEY environment variables must be set")

    stars = fetch_github_stars(username, token)
    if stars is None:
        print("Failed to fetch GitHub stars. Check your credentials and network connection.")
        return

    markdown_content = generate_markdown(stars)
    if markdown_content:
        save_markdown(markdown_content, 'index.md')
        print(markdown_content)
    else:
        print("No GitHub stars found or unable to generate markdown content.")

if __name__ == "__main__":
    main()
