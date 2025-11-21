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
    repos = {"username":username, "repos":[]}
    while repos_url:
        r = requests.get(repos_url, headers=headers)
        if r.status_code != 200:
            print(f"Error getting repositories for user: {username}")
        r.raise_for_status()
        repos["repos"].extend(r.json())
        # Pagination
        repos_url = r.links.get('next', {}).get('url')
    return repos

def get_readme_image_url(owner, token, repo, branch="main"):
    """Fetch README raw content and extract first image URL, resolving relative and absolute paths."""
    readme_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    headers = {'Accept': 'application/vnd.github.raw+json', 'X-GitHub-Api-Version': '2022-11-28'}
    if token != None:
        headers['Authorization'] = 'Bearer ' + token
    r = requests.get(readme_url, headers=headers)
    if r.status_code != 200:
        print(f"Error getting readme for {repo}")
        print(f"\t >  status code: {r.status_code}")
        print(f"\t >  text: {r.text}")
        print(f"\t >  url: {readme_url}")
        print(f"\t >  headers: {headers}")
        return None
    content = r.text
    # find an image that is manually set for use in portfolio with class="portfolio"
    match = re.search(r'class\s*=\s*"portfolio"\s*src\s*=\s*"(.+?)"', content)
    # If not found, look for images using markdown
    if not match:
        match = re.search(r'!\[.*?\]\((.*?)\)', content)
    # If not found, look for images using img tags
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
    else:
        print("NO TOKEN PROVIDED")
    
    userRepos = []

    repos = get_repositories(username, token)
    userRepos.append(repos)

    # Manual repos
    repos = get_repositories("The-Distributed-Computing-Project", token)
    userRepos.append(repos)
    repos = get_repositories("Asa-Programming-Language", token)
    userRepos.append(repos)

    starsOffset = {"vault":50, "LMark":20, "CPP-Key-Logger":-100, "AetherGrid":30, "Asa":200}
    hiddenRepos = {"TPT-Biological-Mod", "RedditMaker"}

    # Only display repositories I own, not forks
    allRepos = []
    for u in userRepos:
        u["repos"] = [r for r in u["repos"] if (not r.get('fork'))]
        for r in u["repos"]:
            r["username"] = u["username"]
            allRepos.append(r)
    allRepos.sort(key=lambda r: r.get('stargazers_count', 0) + (starsOffset[r["name"]] if r["name"] in starsOffset else 0), reverse=True)

    items = []
    for repo in allRepos:
        username = repo["username"]
        name = repo['name']
        desc = repo.get('description', '')
        stars = repo.get('stargazers_count', 0)
        html_url = repo['html_url']
        thumb_url = get_readme_image_url(username, token, name)
        if not thumb_url:
            thumbnail_image = ""
        else:
            thumbnail_image = f'''
                <div class="portfolio-thumb">
                  <img src="{thumb_url}" alt="{name} thumbnail"/>
                </div>
            '''
        if not desc:
            continue
        if name in hiddenRepos:
            continue
        block = f'''
        <div class="portfolio-item">
          <a href="{html_url}" target="_blank">
            {thumbnail_image}
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
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-XZ1MVQZY32"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date());
          gtag('config', 'G-XZ1MVQZY32');
        </script>

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
          margin-bottom:40px;
        }}
      </style>
    </head>
    <body>
        <div class="">
        <div>
            <a href="./" class="h1link">
                <h1 class="title">
                SAMUEL HP
                </h1>
            </a>
        </div>
		<br/>
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
