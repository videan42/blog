#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import os
import sys

THISDIR = os.path.dirname(os.path.realpath(__file__))

if THISDIR not in sys.path:
    sys.path.insert(0, THISDIR)

AUTHOR = 'David Joy'
SITENAME = 'DarkStar Labs'
SITESUBTITLE = 'Python, Engineering, Magic Ponies'
SITEURL = ''

DEFAULT_CATEGORY = 'misc'

MARKUP = ('rst', )

DEFAULT_PAGINATION = 4
PDF_GENERATOR = False
REVERSE_CATEGORY_ORDER = True

TIMEZONE = 'US/New York'

DEFAULT_LANG = 'en'

LATEX = 'article'

DISPLAY_PAGES_ON_MENU = True

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

USE_FOLDER_AS_CATEGORY = True

# Blogroll
LINKS =  tuple()

# Social widget
SOCIAL = tuple()

# Static Paths
STATIC_PATHS = ['images', 'blog/images']

THEME = os.path.join(THISDIR, 'theme')

PLUGINS = ["plugins.latex"]

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
