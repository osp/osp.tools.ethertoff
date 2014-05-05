import re
import os
from random import randint

from datetime import datetime

from relearn.settings import MEDIA_ROOT
from etherpadlite.models import Pad, PadAuthor, PadServer
from django.contrib.auth.models import AnonymousUser
from django.contrib.sites.models import get_current_site

is_eye = re.compile(r'[GD]\d+\.svg')
number_of_eyes = len([eye for eye in os.listdir(os.path.join(MEDIA_ROOT, 'images', 'eyes')) if is_eye.match(eye)])

class EthertoffError(Exception):
    pass

def site_name(request):
    if 'admin' in request.path:
        return {}
    current_site = get_current_site(request)
    # maybe something that sounds more to the point than stite_name?
    # project_name? wiki_name?
    return { 'site_name' : current_site.name }

def pads(request):
    hash = {}
    if 'admin' in request.path:
        return hash
    # If the user is logged in:
    if hasattr(request, 'user') and not isinstance(request.user, AnonymousUser):
        # This magic exists to synch between the django author and the etherpad author
        try:  # Retrieve the corresponding padauthor object
            author = PadAuthor.objects.get(user=request.user)
        except PadAuthor.DoesNotExist:
            if len(PadServer.objects.all()) == 0:
                raise EthertoffError("In trying to associate the author to Etherpad, Ethertoff did not find a suitable pad server. In the admin, you need to create a PadServer object that contains the address of your etherpad install.")
            author = PadAuthor(
                user=request.user,
                server=PadServer.objects.all().reverse()[0]
            )
            author.save()
        author.GroupSynch()
        if author.group.count() == 0:
            raise EthertoffError("This user needs to be associated to a group (that in turn needs to be associated to an Etherpad group).")
        hash['author'] = author
    hash['pads'] = Pad.objects.all()
    return hash

def eye(request):
    hash = {}
    if 'admin' in request.path:
        return hash
    n = randint(1, 1 + number_of_eyes / 2)
    hash['left_eye']  = 'G' + str(n) + '.svg'
    hash['right_eye'] = 'D' + str(n) + '.svg'
    return hash
