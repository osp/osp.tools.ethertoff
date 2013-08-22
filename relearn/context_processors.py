from etherpadlite.models import Pad, PadAuthor
from django.contrib.auth.models import AnonymousUser

def pads(request):
    hash = {}
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
