#!/usr/bin/env python3
import os, re

tag_posts = {}
for f in sorted(os.listdir('_posts')):
    if not f.endswith('.md'): continue
    with open(f'_posts/{f}', 'r') as fp:
        content = fp.read()
        m = re.search(r'^title:\s*"([^"]+)"', content, re.MULTILINE)
        title = m.group(1) if m else f
        m2 = re.search(r'^date:\s*([\d-]+)', content, re.MULTILINE)
        date = m2.group(1) if m2 else ""
        m3 = re.search(r'^tags:\s*\[([^\]]+)\]', content, re.MULTILINE)
        if m3:
            for t in m3.group(1).split(','):
                tag = t.strip().strip('"')
                tag_clean = re.sub(r'\s+', '-', tag).lower()
                if tag_clean not in tag_posts:
                    tag_posts[tag_clean] = {'title': tag, 'posts': []}
                tag_posts[tag_clean]['posts'].append({'title': title, 'date': date, 'slug': f.replace('.md','.html')})

homepage_tags = ['wireless-earbuds', 'tech', 'home-gym', 'kitchen-gadgets', 'dog-toys', 'robot-vacuum']
os.makedirs('_pages', exist_ok=True)

cat_desc = {
    'wireless-earbuds': 'Wireless Earbuds',
    'tech': 'Tech & Gadgets',
    'home-gym': 'Home Gym Equipment',
    'kitchen-gadgets': 'Kitchen Gadgets & Appliances',
    'dog-toys': 'Dog Toys & Pet Care',
    'robot-vacuum': 'Robot Vacuums & Smart Cleaning',
}

for tag in homepage_tags:
    if tag not in tag_posts:
        print(f"WARNING: no posts for tag '{tag}'")
        continue
    posts = tag_posts[tag]['posts']
    title_clean = cat_desc.get(tag, tag_posts[tag]['title']).strip('"')
    
    posts_html = ''
    for p in posts:
        posts_html += '  <li class="post-list-item">\n'
        posts_html += '    <a href="/ai-money-blog/' + p["slug"] + '" class="post-list-title">' + p["title"] + '</a>\n'
        posts_html += '    <span class="post-list-meta">' + p["date"] + '</span>\n'
        posts_html += '  </li>\n'
    
    out = '''---
layout: default
permalink: /tag/''' + tag + '''/
title: "''' + title_clean + ''' Reviews & Guides"
---

# ''' + title_clean + '''

<div class="tag-intro">
  <p>Honest reviews, comparisons, and buying guides for ''' + title_clean.lower() + '''. Updated for 2026.</p>
</div>

<h2>Latest Articles</h2>
<ul class="post-list">
''' + posts_html + '''</ul>

<p><a href="/ai-money-blog/blog/">&#8592; Browse All Posts</a></p>

{% include affiliate-disclosure.html %}
'''
    with open('_pages/tag-' + tag + '.html', 'w') as f:
        f.write(out)
    print("Created: _pages/tag-" + tag + ".html (" + str(len(posts)) + " posts)")

print("\nDone!")
