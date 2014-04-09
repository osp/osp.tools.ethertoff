# -*- coding: utf-8 -*-

# Python imports

import os
import codecs
import urllib

# PyPi imports

import markdown
from py_etherpad import EtherpadLiteClient

# Django imports

from django.core.management.base import BaseCommand, CommandError

# Django Apps import

from etherpadlite.models import Pad, PadAuthor
from relearn.settings import BACKUP_DIR

class Command(BaseCommand):
    args = ''
    help = 'Write all pads to plain text files'

    def handle(self, *args, **options):
        
        for pad in Pad.objects.all():
            padID = pad.group.groupID + '$' + urllib.quote_plus(pad.name.replace('::', '_'))
            epclient = EtherpadLiteClient(pad.server.apikey, pad.server.apiurl)
            
            # Etherpad gives us authorIDs in the form ['a.5hBzfuNdqX6gQhgz', 'a.tLCCEnNVJ5aXkyVI']
            # We link them to the Django users DjangoEtherpadLite created for us
            authorIDs = epclient.listAuthorsOfPad(padID)['authorIDs']
            authors = PadAuthor.objects.filter(authorID__in=authorIDs)
            
            text = epclient.getText(padID)['text']
            
            backup_file_path = os.path.join(BACKUP_DIR, pad.display_slug)
            
            with codecs.open(backup_file_path, 'w', 'utf-8') as f:
                f.write(text)
            