import sys
import urllib.request
import gzip
import ssl
import re

if len(sys.argv) < 2:
    print("Usage: python fetch.py <url>")
    sys.exit(1)

url = sys.argv[1]

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    url, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
)
try:
    with urllib.request.urlopen(req, context=ctx) as response:
        html = response.read()
        if response.info().get('Content-Encoding') == 'gzip':
            html = gzip.decompress(html)
        
        html_str = html.decode('utf-8', errors='ignore')
        
        # Extract title
        title_match = re.search(r'<meta property="og:title" content="(.*?)"', html_str)
        title = title_match.group(1) if title_match else "Unknown Title"
        
        # Extract author
        author_match = re.search(r'<meta property="og:article:author" content="(.*?)"', html_str)
        author = author_match.group(1) if author_match else "Unknown Author"

        # Extract content
        content_match = re.search(r'id="js_content"[^>]*>(.*?)</div>', html_str, re.DOTALL)
        if content_match:
            content = content_match.group(1)
            # Remove scripts and styles
            content = re.sub(r'<script.*?</script>', '', content, flags=re.DOTALL)
            content = re.sub(r'<style.*?</style>', '', content, flags=re.DOTALL)
            # Remove html tags
            text = re.sub(r'<[^>]+>', '\n', content)
            # Replace multiple newlines with a single newline
            text = re.sub(r'\n+', '\n', text)
            print(f"Title: {title}")
            print(f"Author: {author}\n")
            print(text.strip())
        else:
            print(f"Title: {title}")
            print(f"Author: {author}\n")
            print("Content could not be automatically extracted or the article has a different structure.")
except Exception as e:
    print("ERROR:", e)
