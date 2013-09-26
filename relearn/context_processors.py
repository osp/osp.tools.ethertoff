from datetime import datetime

from etherpadlite.models import Pad, PadAuthor, PadServer
from django.contrib.auth.models import AnonymousUser
from django.contrib.sites.models import get_current_site

def site_name(request):
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
            author = PadAuthor(
                user=request.user,
                server=PadServer.objects.get(id=1)
            )
            author.save()
        author.GroupSynch()
        hash['author'] = author
    hash['pads'] = Pad.objects.all()
    return hash

