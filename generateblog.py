import requests
import re
from pathlib import Path
import sys
import os
import markdown

# Register the custom Asa lexer
from asa_lexer import AsaLexer
from pygments import lexers

# Import custom horizontal rule extension
from hr_preprocessor import HorizontalRuleExtension

# Import custom inline note extension
from inline_note_preprocessor import InlineNoteExtension

# Register the lexer class
def get_asa_lexer():
    return AsaLexer

# Patch the get_lexer_by_name function to handle 'asa'
original_get_lexer_by_name = lexers.get_lexer_by_name
def patched_get_lexer_by_name(name, **options):
    if name == 'asa':
        return AsaLexer(**options)
    return original_get_lexer_by_name(name, **options)
lexers.get_lexer_by_name = patched_get_lexer_by_name


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

def extract_description_from_html(html_content, max_chars=256):
    """Extract text from <p> tags that are direct children of blog-body div."""
    # Find the blog-body div
    start_match = re.search(r'<div class="blog-body">', html_content)
    if not start_match:
        return ""

    # Extract everything from blog-body to </body> (since blog-body div isn't closed)
    start_pos = start_match.end()
    end_match = re.search(r'</body>', html_content[start_pos:])
    if not end_match:
        return ""

    blog_content = html_content[start_pos:start_pos + end_match.start()]

    # Now extract direct <p> children only
    text = ""
    depth = 0
    i = 0

    while i < len(blog_content):
        if blog_content[i] == '<':
            tag_match = re.match(r'<(\w+)[^>]*>', blog_content[i:])
            if tag_match:
                tag_name = tag_match.group(1).lower()

                # Track depth for non-paragraph tags
                if tag_name not in ['p', 'br', 'img', 'hr']:
                    depth += 1
                    i += len(tag_match.group(0))
                    continue

                # Found a <p> tag at depth 0 (direct child)
                if tag_name == 'p' and depth == 0:
                    # Extract the full <p>...</p> content
                    p_match = re.match(r'<p>(.*?)</p>', blog_content[i:], re.DOTALL)
                    if p_match:
                        p_content = p_match.group(1)

                        # Check if this <p> only directly contains tags (no text outside tags)
                        # This matches content that is entirely wrapped in tags: ^\s*<.+>\s*$
                        # E.g., "<title>...</title>" or "<img src='...'>" but not "text <title>...</title>"
                        only_contains_tags = bool(re.match(r'^\s*<.+>\s*$', p_content, re.DOTALL))

                        # Skip this <p> if it only contains tags with no direct text
                        if only_contains_tags:
                            i += len(p_match.group(0))
                            continue

                        # Remove any HTML tags within the <p>
                        clean_text = re.sub(r'<[^>]+>', '', p_content)
                        # Decode HTML entities
                        clean_text = clean_text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
                        clean_text = clean_text.strip()

                        if clean_text:
                            text += clean_text + "\n"
                            if len(text) >= max_chars:
                                break

                        i += len(p_match.group(0))
                        continue

            # Check for closing tags
            close_match = re.match(r'</(\w+)>', blog_content[i:])
            if close_match:
                tag_name = close_match.group(1).lower()
                if tag_name not in ['p', 'br', 'img', 'hr']:
                    depth = max(0, depth - 1)
                i += len(close_match.group(0))
                continue

        i += 1

    return text[:max_chars].strip()


def convert_markdown_with_css(markdown_file, css_file, output_file):
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_text = f.read()

        html_body = markdown.markdown(
            markdown_text,
            extensions=['fenced_code', 'codehilite', 'pymdownx.inlinehilite', 'pymdownx.details', 'toc', 'extra', 'admonition', 'nl2br', InlineNoteExtension(), HorizontalRuleExtension()],
            extension_configs={
                'codehilite': {
                    'guess_lang': False
                }
            }
        )

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

                <br>

                <script src="https://giscus.app/client.js"
        data-repo="achillium/samuelhp.com"
        data-repo-id="R_kgDOP6m6Dw"
        data-category="Announcements"
        data-category-id="DIC_kwDOP6m6D84Cwezl"
        data-mapping="title"
        data-strict="1"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="top"
        data-theme="light"
        data-lang="en"
        data-loading="lazy"
        crossorigin="anonymous"
        async>
</script>
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

        # Read the HTML file for clean description text
        html_filename = filename.replace(".md", ".html")
        html_path = os.path.join(out_path, html_filename)
        if os.path.exists(html_path):
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            post_str = extract_description_from_html(html_content, max_chars=500)
        else:
            # Fallback to old method if HTML doesn't exist yet
            post_str = convert_post_to_string(post)[:256]

        block = f'''
        <div class="blog-item">
          <a href="{html_filename}" class="blog-container">
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
