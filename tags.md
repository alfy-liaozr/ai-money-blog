---
layout: default
permalink: /tags/
title: "Tags"
---

# 🏷️ Browse by Category

{% assign tags = site.tags | sort %}
<ul>
{% for tag in tags %}
  <li><a href="{{ '/tag/' | relative_url }}{{ tag[0] | slugify }}/"><strong>{{ tag[0] }}</strong></a> ({{ tag[1].size }} posts)</li>
{% endfor %}
</ul>
