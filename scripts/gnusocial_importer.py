#!/usr/bin/env python3

# This script requires the following python packages:
#   * requests
#   * dateutils
#   * html2text
#   * awesome-slugify
#
# It is recommended that you install the packages within a virtualenv and run
# the script from within the virtualenv:
#   $ python3 -m venv venv
#   $ venv/bin/pip install requests dateutils html2text awesome-slugify
#   $ venv/bin/python scripts/gnusocial_importer.py
#   $ rm -rf venv

import os

import requests
from dateutil.parser import parse as date_parse
from dateutil.tz import gettz
from html2text import html2text
from slugify import slugify

URL = 'https://taslug.org.au/api/statuses/user_timeline/2.as'
TIMEZONE = 'Australia/Hobart'
OUTPUT = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    '..',
    '_posts',
    '{}')

tzinfo = gettz(TIMEZONE)
req = requests.get(URL)
items = req.json().get('items', [])

for item in items:
    if item.get('verb') != 'post':
        continue

    published = date_parse(item['published']).astimezone(tzinfo)
    content = html2text(item['content'])

    if not content.startswith('##'):
        # Hack for non-conforming post
        if not content.startswith('Before October'):
            continue
        title = ('Hobart October 19th Meeting - ' +
                 'Brewing Beer with Open Source (Peter Lawler)')
    else:
        parts = content.split('\n\n')
        title = ' '.join(parts[0].strip(' #').split('\n'))
        content = '\n\n'.join(parts[1:])

    if title.lower().startswith('hobart'):
        category = 'hobart'
    elif title.lower().startswith('launceston'):
        category = 'launceston'
    elif 'esp8266 hackfest' in title.lower():
        category = 'hobart'
    else:
        category = ''

    filename = '{}-{}.md'.format(published.strftime('%Y-%m-%d'),
                                 slugify(title, to_lower=True))
    with open(OUTPUT.format(filename), 'w') as output:
        output.write("""
---
layout: post
title: "{title}"
date: {date}
categories: {category}
---

{content}""".format(
            title=title,
            date=published.strftime('%Y-%m-%d %H:%M %z'),
            category=category,
            content=content).strip())
