import requests
import re
from pathlib import Path
import sys

GITHUB_API = "https://api.github.com"

def get_repositories(username, token):
    repos_url = f"{GITHUB_API}/users/{username}/repos?per_page=100"
    headers = {}
    if token != None:
        headers = {'Authorization': 'Bearer ' + token, 'X-GitHub-Api-Version': '2022-11-28'}
    repos = []
    while repos_url:
        r = requests.get(repos_url, headers=headers)
        r.raise_for_status()
        repos.extend(r.json())
        # Pagination
        repos_url = r.links.get('next', {}).get('url')
    return repos

def get_readme_image_url(owner, token, repo, branch="main"):
    """Fetch README raw content and extract first image URL, resolving relative and absolute paths."""
    readme_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    headers = {'Accept': 'application/vnd.github.v3.raw', 'X-GitHub-Api-Version': '2022-11-28'}
    if token != None:
        headers['Authorization'] = 'Bearer ' + token
    r = requests.get(readme_url, headers=headers)
    if r.status_code != 200:
        print(f"Error getting readme for {repo}")
        return None
    content = r.text
    # Find first markdown image like ![alt](url)
    match = re.search(r'!\[.*?\]\((.*?)\)', content)
    if not match:
        match = re.search(r'src\s*=\s*"(.+?)"', content)
    if not match:
        return None
    url = match.group(1).strip()
    if url.startswith("http://") or url.startswith("https://"):
        # Absolute URL, use as-is
        print(f"Image: {url}")
        return url
    else:
        # Relative or GitHub repo-rooted path (starting with '/')
        # Normalize path by stripping leading '/'
        url = url.lstrip('/')
        # Construct the raw URL to this file on main branch
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/" + url
        print(f"Image: {url}")
        return url


def generate_portfolio(username, args, style_path="./samuelhp_files/styles.css", out_path="portfolio.html"):
    token = None
    if len(args)>1:
        token = args[1]
        print("Using token: " + token)
    repos = get_repositories(username, token)
    repos.extend(get_repositories("The-Distributed-Computing-Project", token))
    repos.extend(get_repositories("Asa-Programming-Language", token))
    # Only display repositories I own, not forks
    repos = [r for r in repos if (not r.get('fork')) and r.get('stargazers_count', 0) > 1]
    repos.sort(key=lambda r: r.get('stargazers_count', 0), reverse=True)
    items = []
    for repo in repos:
        name = repo['name']
        desc = repo.get('description', '')
        stars = repo.get('stargazers_count', 0)
        html_url = repo['html_url']
        thumb_url = get_readme_image_url(username, token, name)
        if not thumb_url:
            thumb_url = "placeholder.jpg"
        if not desc:
            continue
        block = f'''
        <div class="portfolio-item">
          <a href="{html_url}" target="_blank">
            <div class="portfolio-thumb">
              <img src="{thumb_url}" alt="{name} thumbnail"/>
            </div>
            <div class="portfolio-title">{name}</div>
            <div class="portfolio-desc">{desc if desc else '<i>No description</i>'}</div>
            <div class="portfolio-stars">★ {stars}</div>
          </a>
        </div>
        '''
        items.append(block)
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Samuel HP's Portfolio</title>
        <link rel="stylesheet" type="text/css" href="./samuelhp_files/styles.css">
        
        <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
        <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
        <link rel="manifest" href="/site.webmanifest">
      <style>
      body {{
          min-height: 100vh;
          overflow: auto;
        }}
      </style>
    </head>
    <body style="overflow:auto; min-height:100vh;">
    <div>
    </div>
    
    
    
    
        <div class="">
            <a href="index.html" class="h1link">
                <h1>
                SAMUEL HP
                </h1>
            </a>
          <div class="portfolio-grid">
            {''.join(items)}
          </div>
        </div>
    </body>
    </html>
    '''
    Path(out_path).write_text(html, encoding="utf-8")
    print(f"Portfolio generated: {out_path}")


generate_portfolio("sam-astro", sys.argv)