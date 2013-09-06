# -*- coding: utf-8 -*-

# Python imports
import datetime
import time
import urllib
from urlparse import urlparse

# Framework imports
from django.shortcuts import render_to_response, get_object_or_404

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

from py_etherpad import EtherpadLiteClient
from gitcommits.models import commits

from etherpadlite.models import *
from etherpadlite import forms
from etherpadlite import config

from django.shortcuts import render
from django.core.mail import send_mail
from relearn.forms import ContactForm

from relearn.templatetags.wikify import dewikify

@login_required(login_url='/accounts/login')
def padCreate(request, pk):
    """Create a named pad for the given group
    So this is kind of convoluted. With an input like
    
    Relearn::Can it scale to the universe
    
    we get a pad, with the unchangeable id:
    
    relearn::can-it-scale-to-the-universe
    
    This id becomes the initial value for the (changeable) url slug, as display_slug.
    Based on this id we also set the (changeable) display name, as display_name,
    through a slight transformation (- becomes space, :: →) as in:
    
    relearn → can it scale to the universe
    """
    group = get_object_or_404(PadGroup, pk=pk)

    if request.method == 'POST':  # Process the form
        form = forms.PadCreate(request.POST)
        if form.is_valid():
            n = form.cleaned_data['name']
            n = n.replace(u':',u'zxgiraffe77')
            n = slugify(n)
            n = n.replace(u'zxgiraffe77', u':')
            pad = Pad(
                name=n,
                display_slug=n,
                display_name=dewikify(n),
                server=group.server,
                group=group
            )
            pad.save()
            return HttpResponseRedirect(reverse('pad-write', args=(n,) ))
    else:  # No form to process so create a fresh one
        form = forms.PadCreate({'group': group.groupID})

    con = {
        'form': form,
        'pk': pk,
        'title': _('Create pad in %(grp)s') % {'grp': group.__unicode__()}
    }
    con.update(csrf(request))
    return render_to_response(
        'pad-create.html',
        con,
        context_instance=RequestContext(request)
    )


@login_required(login_url='/accounts/login')
def padDelete(request, pk):
    """Delete a given pad
    """
    pad = get_object_or_404(Pad, pk=pk)

    # Any form submissions will send us back to the profile
    if request.method == 'POST':
        if 'confirm' in request.POST:
            pad.delete()
        return HttpResponseRedirect(reverse('profile'))

    con = {
        'action': '/etherpad/delete/' + pk + '/',
        'question': _('Really delete this pad?'),
        'title': _('Deleting %(pad)s') % {'pad': pad.__unicode__()}
    }
    con.update(csrf(request))
    return render_to_response(
        'etherpad-lite/confirm.html',
        con,
        context_instance=RequestContext(request)
    )


@login_required(login_url='/accounts/login')
def groupCreate(request):
    """ Create a new Group
    """
    message = ""
    if request.method == 'POST':  # Process the form
        form = forms.GroupCreate(request.POST)
        if form.is_valid():
            group = form.save()
            # temporarily it is not nessessary to specify a server, so we take
            # the first one we get.
            server = PadServer.objects.all()[0]
            pad_group = PadGroup(group=group, server=server)
            pad_group.save()
            request.user.groups.add(group)
            return HttpResponseRedirect(reverse('profile'))
        else:
            message = _("This Groupname is allready in use or invalid.")
    else:  # No form to process so create a fresh one
        form = forms.GroupCreate()
    con = {
        'form': form,
        'title': _('Create a new Group'),
        'message': message,
    }
    con.update(csrf(request))
    return render_to_response(
        'etherpad-lite/groupCreate.html',
        con,
        context_instance=RequestContext(request)
    )


@login_required(login_url='/accounts/login')
def groupDelete(request, pk):
    """
    """
    pass


@login_required(login_url='/accounts/login')
def profile(request):
    """Display a user profile containing etherpad groups and associated pads
    """
    name = request.user.__unicode__()

    try:  # Retrieve the corresponding padauthor object
        author = PadAuthor.objects.get(user=request.user)
    except PadAuthor.DoesNotExist:  # None exists, so create one
        author = PadAuthor(
            user=request.user,
            server=PadServer.objects.get(id=1)
        )
        author.save()
    author.GroupSynch()

    groups = {}
    for g in author.group.all():
        groups[g.__unicode__()] = {
            'group': g,
            'pads': Pad.objects.filter(group=g)
        }

    return render_to_response(
        'etherpad-lite/profile.html',
        {
            'name': name,
            'author': author,
            'groups': groups
        },
        context_instance=RequestContext(request)
    )


@login_required(login_url='/accounts/login')
def pad(request, pk=None, slug=None):
    """Create and session and display an embedded pad
    """

    # Initialize some needed values
    if slug:
        pad = get_object_or_404(Pad, display_slug=slug)
    else:
        pad = get_object_or_404(Pad, pk=pk)
    padLink = pad.server.url + 'p/' + pad.group.groupID + '$' + \
        urllib.quote_plus(pad.name)
    server = urlparse(pad.server.url)
    author = PadAuthor.objects.get(user=request.user)

    if author not in pad.group.authors.all():
        response = render_to_response(
            'pad.html',
            {
                'pad': pad,
                'link': padLink,
                'server': server,
                'uname': author.user.__unicode__(),
                'error': _('You are not allowed to view or edit this pad')
            },
            context_instance=RequestContext(request)
        )
        return response

    # Create the session on the etherpad-lite side
    expires = datetime.datetime.utcnow() + datetime.timedelta(
        seconds=config.SESSION_LENGTH
    )
    epclient = EtherpadLiteClient(pad.server.apikey, pad.server.apiurl)

    try:
        result = epclient.createSession(
            pad.group.groupID,
            author.authorID,
            time.mktime(expires.timetuple()).__str__()
        )
    except Exception, e:
        response = render_to_response(
            'pad.html',
            {
                'pad': pad,
                'link': padLink,
                'server': server,
                'uname': author.user.__unicode__(),
                'error': _('etherpad-lite session request returned:') +
                ' "' + e.reason + '"'
            },
            context_instance=RequestContext(request)
        )
        return response

    # Set up the response
    response = render_to_response(
        'pad.html',
        {
            'pad': pad,
            'link': padLink,
            'server': server,
            'uname': author.user.__unicode__(),
            'error': False,
            'mode' : 'write'
        },
        context_instance=RequestContext(request)
    )

    # Delete the existing session first
    if ('padSessionID' in request.COOKIES):
        if 'sessionID' in request.COOKIES.keys():
            try:
                epclient.deleteSession(request.COOKIES['sessionID'])
            except ValueError:
                response.delete_cookie('sessionID', server.hostname)
        response.delete_cookie('padSessionID')

    # Set the new session cookie for both the server and the local site
    response.set_cookie(
        'sessionID',
        value=result['sessionID'],
        expires=expires,
        domain=server.hostname,
        httponly=False
    )
    response.set_cookie(
        'padSessionID',
        value=result['sessionID'],
        expires=expires,
        httponly=False
    )
    return response

def pad_read(request, pk=None, slug=None):
    """Read only pad
    """

    # Initialize some needed values
    if slug:
        pad = get_object_or_404(Pad, display_slug=slug)
    else:
        pad = get_object_or_404(Pad, pk=pk)
    
    padID = pad.group.groupID + '$' + urllib.quote_plus(pad.name.replace('::', '_'))
    epclient = EtherpadLiteClient(pad.server.apikey, pad.server.apiurl)
    
    text = epclient.getHtml(padID)['html']
    text = text.replace('&lt;&#x2F;', '</').replace('&#x2F;&gt;', '/>').replace('&gt;', '>').replace('&lt;', '<')
    
    # Create namespaces from the url of the pad
    # 'pedagogy::methodology' -> ['pedagogy']
    # 'pedagogy::methodology::contact' -> ['pedagogy', 'methodology']
    namespaces = [p.rstrip('-') for p in pad.display_slug.split('::')[:-1]]
    
    tpl_params = { 'pad' : pad, 'text' : text, 'mode' : 'read', 'namespaces' : namespaces }
    # or tpl_params['plaintext'] = epclient.getText(padID)['text']
    # and do processing ourselves—
    # we need to figure out if Etherpad’s html output suffices for our purposes
    # The problem with the plain text output is that plugins don’t seem to affect it—
    # And so the Headings are not translated.
    
    return render_to_response("pad-read.html", tpl_params, context_instance = RequestContext(request))

def filter_commits(commits):
    filtered_commits = []
    for commit in commits:
        if "Merge branch '" in commit['message']:
            continue
        commit['commit_time'] = datetime.datetime.fromtimestamp(commit['commit_time'])
        commit['repo_name'] = commit['repo_name'].replace('osp.', '')
        filtered_commits.append(commit)
    return filtered_commits

def all_commits (request):
    commit_stream = commits("osp.relearn.off-grid") + commits("osp.relearn.gesturing-paths") + commits("osp.relearn.be") + commits("osp.relearn.can-it-scale-to-the-universe")
    commit_stream.sort(reverse=True, key=lambda c: c['commit_time'])
    tpl_params = { 'all_commits' : filter_commits(commit_stream) }
    
    return render_to_response("commits.html", tpl_params, context_instance = RequestContext(request))


def home(request):
    # The homepage is the pad called ‘start’ (props to DokuWiki!)
    try:
        Pad.objects.get(name='relearn::start')
        return pad_read(request, slug='relearn::start')
    except Pad.DoesNotExist:
        return HttpResponseRedirect(reverse('login'))


def post_issue(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            subject = "[issue spotted] %s" % form.cleaned_data['subject']
            message = "%s\n\n-- %s" % (form.cleaned_data['message'], name)
            #message = "%s" % (form.cleaned_data['message'])
            email  = form.cleaned_data['email']
            recipients = ['relearn@lists.constantvzw.org']
            send_mail(subject, message, email, recipients)

            return HttpResponseRedirect(reverse('relearn-issue-success')) # Redirect after POST
    else:
        form = ContactForm() # An unbound form
    
    return render(request, 'form.html', {'form': form})
