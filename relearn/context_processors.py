from datetime import datetime

from etherpadlite.models import Pad, PadAuthor, PadServer
from django.contrib.auth.models import AnonymousUser
from django.contrib.sites.models import get_current_site

from gitcommits.models import commits

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

def filter_commits(commits):
    filtered_commits = []
    i = 0
    for commit in commits:
        if "Merge branch '" in commit['message']:
            continue
        commit['commit_time'] = datetime.fromtimestamp(commit['commit_time'])
        commit['repo_name'] = commit['repo_name'].replace('osp.', '')
        filtered_commits.append(commit)
        i += 1
        if i == 10:
            break
    return filtered_commits

def compose_commits(request):
    if 'admin' in request.path:
        return {}
    commit_stream = commits("osp.relearn.off-grid") + commits("osp.relearn.gesturing-paths") + commits("osp.relearn.be") + commits("osp.relearn.can-it-scale-to-the-universe")
    commit_stream.sort(reverse=True, key=lambda c: c['commit_time'])
    return { 'commits' : filter_commits(commit_stream) }
