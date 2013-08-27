#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of gitcal and is © the contributors, listed in README.txt

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see http://www.gnu.org/licenses/.
"""

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('gitcal.views',
    url(r'(?P<repo_slug>[\w\.\-_]+)\.ics$', 'render'),
)
