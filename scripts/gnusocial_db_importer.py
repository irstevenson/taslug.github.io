#!/usr/bin/env python3

# This script requires the following python packages:
#   * awesome-slugify
#   * dateutils
#   * html2text
#   * sqlalchemy

import os
from dateutil.tz import gettz
from html2text import html2text
from slugify import slugify
from sqlalchemy import create_engine, MetaData
from sqlalchemy.sql import select, and_

OUTPUT = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    '..',
    '_posts',
    '{}')

tz_utc = gettz('UTC')
tz_local = gettz('Australia/Hobart')

engine = create_engine('mysql+pymysql://root:root@localhost/taslug_social')
conn = engine.connect()
schema = MetaData(bind=engine)
schema.reflect()

table = schema.tables['user']
query = (
    select([table.c.id])
    .where(table.c.nickname == 'taslug')
)
profile_id = conn.execute(query).fetchone().id

table = schema.tables['notice']
query = (
    select([
        table.c.content,
        table.c.rendered,
        table.c.created,
        table.c.modified,
        table.c.object_type,
        table.c.verb,
    ])
    .where(
        and_(
            table.c.profile_id == profile_id,
            table.c.object_type == 'http://activitystrea.ms/schema/1.0/note',
            table.c.verb == 'http://activitystrea.ms/schema/1.0/post',
        )
    )
)

rows = conn.execute(query).fetchall()

for row in rows:
    published = row.created.replace(tzinfo=tz_utc).astimezone(tz_local)
    modified = row.modified.replace(tzinfo=tz_utc).astimezone(tz_local)
    content = html2text(row.rendered)

    if not content.startswith('##'):
        if content.startswith('Before October'):
            title = ('Hobart October 19th Meeting - ' +
                     'Brewing Beer with Open Source (Peter Lawler)')
            content = '\n' + content
        elif content.startswith('Hobart Meeting'):
            pass
        else:
            # not interested in this post
            continue
        parts = content.split('\n')
        content = '\n'.join(parts[1:])
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
        category = None

    title = title.replace('&amp;', '&')
    content = content.replace('&amp;', '&')
    content = content.replace('<br />', '\n')
    content = '\n'.join([l.rstrip() for l in content.split('\n')])

    filename = '{}-{}.md'.format(published.strftime('%Y-%m-%d'),
                                 slugify(title))
    print("Outputting:", filename)
    with open(OUTPUT.format(filename), 'w') as output:
        output.write("""
---
layout: post
title: "{title}"
date: {date}
categories: {category}
---

{content}""".format(
            title=title.strip(),
            date=published.strftime('%Y-%m-%d %H:%M %z'),
            category=category.strip(),
            content=content.strip()).strip())
