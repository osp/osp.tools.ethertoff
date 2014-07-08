# -*- coding: utf-8 -*-

# Python imports

import os
import codecs
import json
from urllib2 import HTTPError

# PyPi imports

import rdflib

# Django imports

from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string

# Django Apps import

from etherpadlite.models import Pad, PadAuthor
from relearn.settings import BACKUP_DIR

"""
We scrape all the pages, construct a graph, and ask the RDF store to return us all the metadata.

The result will looks something like this:

+----------------------------------------------------------------------+--------------------------------------------+---------------------------------------------------+
| subject                                                              | predicate                                  | object                                            |
+----------------------------------------------------------------------+--------------------------------------------+---------------------------------------------------+
| http://127.0.0.1:8000/r/06_Elodie_Royer_Yoann_Gourmel_The_Play_FR.md | http://purl.org/dc/terms/creator           | Élodie Royer et Yoann Gourmel                     |
| http://127.0.0.1:8000/r/06_Elodie_Royer_Yoann_Gourmel_The_Play_FR.md | http://purl.org/dc/terms/title             | The Play/ザ・プレイ                                 |
| http://127.0.0.1:8000/r/06_Elodie_Royer_Yoann_Gourmel_The_Play_FR.md | http://www.w3.org/ns/md#item               | http://www.w3.org/1999/02/22-rdf-syntax-ns#nil    |
| http://127.0.0.1:8000/r/06_Elodie_Royer_Yoann_Gourmel_The_Play_FR.md | http://purl.org/dc/terms/created           | 2012-06-02T00:00:00                               |
| http://127.0.0.1:8000/r/06_Elodie_Royer_Yoann_Gourmel_The_Play_FR.md | http://www.w3.org/1999/xhtml/vocab#license | http://creativecommons.org/licenses/by-nd/3.0/fr/ |
| http://127.0.0.1:8000/r/B_Bernadette-Mayer_Utopia_FR.md              | http://purl.org/dc/terms/title             | Utopia                                            |
| http://127.0.0.1:8000/r/B_Bernadette-Mayer_Utopia_FR.md              | http://purl.org/dc/terms/creator           | Bernadette Mayer                                  |
| http://127.0.0.1:8000/r/B_Bernadette-Mayer_Utopia_FR.md              | http://www.w3.org/1999/xhtml/vocab#license |                                                   |
| http://127.0.0.1:8000/r/B_Bernadette-Mayer_Utopia_FR.md              | http://purl.org/dc/terms/created           | 2014-10-02T00:00:00                               |
| http://127.0.0.1:8000/r/B_Bernadette-Mayer_Utopia_FR.md              | http://www.w3.org/ns/md#item               | http://www.w3.org/1999/02/22-rdf-syntax-ns#nil    |
+----------------------------------------------------------------------+--------------------------------------------+---------------------------------------------------+

We then use python to construct a list that is easy to use in a template, something like:

[
  {
    "date": "2012-06-02T00:00:00", 
    "title": "The Play/ザ・プレイ", 
    "href": "http://127.0.0.1:8000/r/06_Elodie_Royer_Yoann_Gourmel_The_Play_FR.md", 
    "license": "http://creativecommons.org/licenses/by-nd/3.0/fr/", 
    "author": "Élodie Royer et Yoann Gourmel"
  }, 
  {
    "date": "2014-10-02T00:00:00", 
    "href": "http://127.0.0.1:8000/r/B_Bernadette-Mayer_Utopia_FR.md", 
    "author": "Bernadette Mayer", 
    "license": "", 
    "title": "Utopia"
  }
]

"""


# This SPARQL QUERY it simply gets all the metadata in triples
sparql_query = """PREFIX dc: <http://purl.org/dc/elements/1.1/>
select ?subject ?predicate ?object
where { ?subject ?predicate ?object .\n
}
order by ?subject 
"""

# Map between predicate uris and more easy names to use in the template
short_names = {
    "http://www.w3.org/1999/xhtml/vocab#license" : "license",
    "http://purl.org/dc/terms/title" : "title",
    "http://purl.org/dc/terms/creator" : "author",
    "http://purl.org/dc/terms/created" : "date",
}

def query_results_to_template_articles(query_results):
    """
    Transform the RDFLIB SPARQL query result into the row that we want to use for the template
    """
    template_articles = []
    article = None
    current_uri = None
    for s, p, o in query_results:
        uri   = unicode(s).strip()
        key   = unicode(p).strip()
        value = unicode(o).strip()
        
        if uri != current_uri:
            if article:
                template_articles.append(article)
            article = {
                "href": uri
            }
            current_uri = uri
        
        if key in short_names:
            new_key = short_names[key]
            article[new_key] = value
    
    template_articles.append(article)
    
    return template_articles


class Command(BaseCommand):
    args = ''
    help = 'Create an index of all the articles’ metadata'

    def handle(self, *args, **options):
        
        g = rdflib.Graph()
        host = 'http://f-u-t-u-r-e.org/'
        # 'http://127.0.0.1:8000'
        
        for pad in Pad.objects.all():
            # We only want to index the articles—
            # For now we can distinguish them because they have url’s
            # ending in ‘.md’
            if not pad.display_slug.endswith('.md'):
                continue
            try:
                result = g.parse(host + pad.get_absolute_url())
            except HTTPError, e:
                if e.code == 403:
                    # Some of the pads will not be public yet—
                    # They gives a ‘403 FORBIDDEN’ response
                    # this is expected, and we don’t need to scrape them
                    continue
                else:
                    raise
        
        d = query_results_to_template_articles(g.query(sparql_query))
        
        with open(os.path.join(BACKUP_DIR, "index.json"), 'w') as f:
            f.write(json.dumps(d, indent=2, ensure_ascii=False).encode('utf-8'))
                
        # with open(os.path.join(BACKUP_DIR, "index.html"), 'w') as f:
        #    f.write(render_to_string("home.html", {"articles" : d}).encode('utf-8'))
