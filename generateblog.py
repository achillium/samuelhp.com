import requests
import re
from pathlib import Path
import sys
import os
import markdown


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
        return url

def convert_post_to_string(post):
    o = ""
    for line in post.split("\n"):
        if line.startswith("#"):
            o+= line.split("#")[-1]
        elif line.startswith("<"):
            continue
        else:
            o+=line+"\n"
    return o


def convert_markdown_with_css(markdown_file, css_file, output_file):
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_text = f.read()

        html_body = markdown.markdown(markdown_text, extensions=['fenced_code', 'codehilite'])

        # Create the full HTML structure with a link to the CSS file
        full_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>Samuel HP's Blog</title>
            <link rel="stylesheet" type="text/css" href="{css_file}">
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
            </div>



            <div class="blog-body">
                {html_body}
            </div>
        </body>
        </html>
        """

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_html)

def convert_pages_to_html(source_path="./b_md", out_path="./b"):
    import markdown
    for file in os.listdir(source_path):
        if file.endswith(".md"):
            print(f"Converting {file} to HTML...")
            convert_markdown_with_css(os.path.join(source_path, file),"../samuelhp_files/styles.css",os.path.join(out_path, file.replace(".md", ".html")))
            #markdown.markdownFromFile(input=os.path.join(source_path, file), output=os.path.join(out_path, file.replace(".md", ".html")))
    print(f"DONE!\n")

def generate_blog_home(style_path="./samuelhp_files/styles.css", source_path="./b_md", out_path="./b/"):
    posts = []
    for file in os.listdir(source_path):
        if file.endswith(".md"):
            with open(os.path.join(source_path, file)) as f:
                posts.append((str(file),f.read()))

    items = []
    for filename,post in posts:
        print(f"Adding {filename} to home...")
        match = re.search(r'<title>(.+?)<\/title>', post)
        if not match:
            name = "Untitled"
            print(f"\t ! No title found for {filename}")
        else:
            name = match.group(1).strip()
        thumb_url = get_readme_image_url(post)
        if not thumb_url:
            thumb_url = "../placeholder.jpg"
            print(f"\t ! No thumbnail found for {filename}")
        post_str = convert_post_to_string(post)
        block = f'''
        <div class="blog-item">
          <a href="{filename.replace(".md", ".html")}" class="blog-container">
            <div class="blog-thumb">
              <img src="{thumb_url}" alt="{name} thumbnail"/>
            </div>
            <div class="blog-synopsis">
                <div class="blog-title">{name}</div>
                <div class="blog-description">{post_str}</div>
            </div>
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
        <title>Samuel HP's Blog</title>
        <link rel="stylesheet" type="text/css" href="../samuelhp_files/styles.css">
        
        <link rel="apple-touch-icon" sizes="180x180" href="../apple-touch-icon.png">
        <link rel="icon" type="image/png" sizes="32x32" href="../favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="16x16" href="../favicon-16x16.png">
        <link rel="manifest" href="../site.webmanifest">
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
            <a href="../" class="h1link">
                <h1>
                SAMUEL HP
                </h1>
            </a>
          <div class="blog-grid">
            {''.join(items)}
          </div>
        </div>
    </body>
    </html>
    '''
    print(f"DONE!\n")
    Path(out_path+"/index.html").write_text(html, encoding="utf-8")
    print(f"Blog generated: {out_path}/index.html\n")

convert_pages_to_html()
generate_blog_home()
#generate_portfolio("sam-astro", sys.argv)
