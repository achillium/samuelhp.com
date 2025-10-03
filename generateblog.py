import requests
import re
from pathlib import Path
import sys
import os


def get_readme_image_url(content):
    # find an image that is manually set for use in blog with class="blog"
    match = re.search(r'class\s*=\s*"blog"\s*src\s*=\s*"(.+?)"', content)
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
        # Normalize path by stripping leading '/'
        url = url.lstrip('/')
        # Construct the raw URL to this file on main branch
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/" + url
        print(f"Image: {url}")
        return url

def convert_pages_to_html(source_path="./b_md", out_path="./b"):
    import markdown
    for file in os.listdir(source_path):
        if file.endswith(".md"):
            markdown.markdownFromFile(input=os.path.join(source_path, file), output=os.path.join(out_path, file.replace(".md", ".html")))

def generate_blog_home(style_path="./samuelhp_files/styles.css", source_path="./b_md", out_path="./b/index.html"):
    

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
            thumb_url = "placeholder.jpg"
        if not desc:
            continue
        if name in hiddenRepos:
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
          margin-bottom:40px;
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
    print(f"Blog generated: {out_path}")

convert_pages_to_html()
#generate_portfolio("sam-astro", sys.argv)
