#!/usr/bin/env python3
"""Add Amazon affiliate tag to all links in Jekyll posts."""
import re
import os

POSTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '_posts')
AMAZON_TAG = 'alfyliaozr20-20'

def normalize_amazon_url(match):
    """Replace amazon.com links with tagged versions."""
    url = match.group(0)
    
    # Skip if already tagged
    if AMAZON_TAG in url:
        return url
    
    # Handle URLs that already have query parameters
    if '?' in url:
        if url.endswith(')') or url.endswith('"') or url.endswith("'"):
            sep = '&'
        else:
            sep = '&'
        # Insert before any trailing punctuation
        # First check for URL-embedded patterns
        url = url.replace(')', f'?tag={AMAZON_TAG})')
        return url
    else:
        # No query params - add ?
        # Handle markdown closing paren
        if url.endswith(')'):
            url = url[:-1] + f'?tag={AMAZON_TAG})'
        else:
            url = url + f'?tag={AMAZON_TAG}'
        return url

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Match amazon.com URLs in markdown links [...]() or bare URLs
    # Pattern: https://amazon.com/... up to closing ) or whitespace
    pattern = r'https://amazon\.com/[^\s)]+'
    
    original = content
    content = re.sub(pattern, normalize_amazon_url, content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    count = 0
    for fname in os.listdir(POSTS_DIR):
        if fname.endswith('.md'):
            fpath = os.path.join(POSTS_DIR, fname)
            if process_file(fpath):
                print(f"✅ Updated: {fname}")
                count += 1
    print(f"\n📊 Total files updated: {count}")

if __name__ == '__main__':
    main()
