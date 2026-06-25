---
layout: default
title: "All Blog Posts"
permalink: /blog/
---

# 📝 All Posts

{% assign sorted = site.posts | sort: 'date' | reverse %}
{% assign current_year = '' %}

{% for post in sorted %}
  {% assign post_year = post.date | date: "%Y" %}
  {% if post_year != current_year %}
    {% assign current_year = post_year %}
    {% unless forloop.first %}</ul>{% endunless %}
    <h2>{{ post_year }}</h2>
    <ul class="post-list">
  {% endif %}
  <li class="post-list-item">
    <a href="{{ post.url | relative_url }}" class="post-list-title">{{ post.title }}</a>
    <span class="post-list-meta">{{ post.date | date: "%B %-d, %Y" }} 
      {% if post.tags.size > 0 %}
      — Tags: {% for tag in post.tags limit:3 %}{{ tag }}{% unless forloop.last %}, {% endunless %}{% endfor %}
      {% endif %}
    </span>
  </li>
{% endfor %}
</ul>
