# -*- coding: utf-8 -*-

# Python imports
import datetime
import time
import urllib
from urlparse import urlparse
import HTMLParser
import json
import re
import os

# PyPi imports

import markdown
from py_etherpad import EtherpadLiteClient
import dateutil.parser

# Framework imports
from django.shortcuts import render_to_response, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

# Django Apps import

from etherpadlite.models import *
from etherpadlite import forms
from etherpadlite import config

from django.shortcuts import render
from django.core.mail import send_mail
from relearn.forms import ContactForm

from relearn.templatetags.wikify import dewikify

# By default, the homepage is the pad called ‘start’ (props to DokuWiki!)
try:
    from relearn.settings import HOME_PAD
except ImportError:
    HOME_PAD = 'start'

"""
Set up an HTMLParser for the sole purpose of unescaping
Etherpad’s HTML entities.
cf http://fredericiana.com/2010/10/08/decoding-html-entities-to-text-in-python/
"""

h = HTMLParser.HTMLParser()
unescape = h.unescape

"""
Create a regex for our include template tag
"""
include_regex = re.compile("{%\s?include\s?\"([\w._-]+)\"\s?%}")


@login_required(login_url='/accounts/login')
def padCreate(request, pk):
    """Create a named pad for the given group
    So this is kind of convoluted. With an input like

    Relearn::Can it scale to the universe

    we get a pad, with the unchangeable id:
    relearn::can-it-scale-to-the-universe
    and the name / display_slug:
    Relearn::Can_it_scale_to_the_universe

    The title of pages is displayed through a slight transformation,
    known as dewikify.
    _ becomes space, :: → as in:
    Relearn → can it scale to the universe
    """
    group = get_object_or_404(PadGroup, pk=pk)

    if request.method == 'POST':  # Process the form
        form = forms.PadCreate(request.POST)
        if form.is_valid():
            n = form.cleaned_data['name']
            basename = slugify(n)[:42]
            n = re.sub(r'\s+', u'_', n)
            pad = Pad(
                name=basename,
                display_slug=n,
                display_name=n,     # this is just for backwards compatibility
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
def pad(request, pk=None, slug=None): # pad_write
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

    # Etherpad gives us authorIDs in the form ['a.5hBzfuNdqX6gQhgz', 'a.tLCCEnNVJ5aXkyVI']
    # We link them to the Django users DjangoEtherpadLite created for us
    authorIDs = epclient.listAuthorsOfPad(padID)['authorIDs']
    authors = PadAuthor.objects.filter(authorID__in=authorIDs)

    authorship_authors = []
    for author in authors:
        authorship_authors.append({ 'name'  : author.user.first_name if author.user.first_name else author.user.username,
                                    'class' : 'author' + author.authorID.replace('.','_') })
    authorship_authors_json = json.dumps(authorship_authors, indent=2)

    name, extension = os.path.splitext(slug)

    meta = {}

    if not extension:
        # Etherpad has a quasi-WYSIWYG functionality.
        # Though is not alwasy dependable
        text = epclient.getHtml(padID)['html']
        # Quick and dirty hack to allow HTML in pads
        text = unescape(text)
    else:
        # If a pad is named something.css, something.html, something.md etcetera,
        # we don’t want Etherpads automatically generated HTML, we want plain text.
        text = epclient.getText(padID)['text']
        if extension in ['.md', '.markdown']:
            md = markdown.Markdown(extensions=['extra', 'meta', 'headerid(level=2)', 'attr_list', 'figcaption'])
            text = md.convert(text)
            try:
                meta = md.Meta
            except AttributeError:   # Edge-case: this happens when the pad is completely empty
                meta = None
    
    # Convert the {% include %} tags into a form easily digestible by jquery
    # {% include "example.html" %} -> <a id="include-example.html" class="include" href="/r/include-example.html">include-example.html</a>
    def ret(matchobj):
        return '<a id="include-%s" class="include pad-%s" href="%s">%s</a>' % (slugify(matchobj.group(1)), slugify(matchobj.group(1)), reverse('pad-read', args=(matchobj.group(1),) ), matchobj.group(1))
    
    text = include_regex.sub(ret, text)
    
    
    # Create namespaces from the url of the pad
    # 'pedagogy::methodology' -> ['pedagogy', 'methodology']
    namespaces = [p.rstrip('-') for p in pad.display_slug.split('::')]

    meta_list = []
    if meta and len(meta.keys()) > 0:
        print meta.keys()

        # One needs to set a ‘Public’ metadata for the page to be accessible to outside visitors
        if not 'public' in meta or not meta['public'][0] or meta['public'][0].lower() in ['false', 'no', 'off', '0']:
            if not request.user.is_authenticated():
                raise PermissionDenied
        
        # The human-readable date is parsed so we can sort all the articles
        if 'date' in meta:
            meta['date_parsed'] = []
            for date in meta['date']:
                meta['date_parsed'].append( dateutil.parser.parse(meta['date'][0]).isoformat() )
        
        meta_list = list(meta.iteritems())

    tpl_params = { 'pad'                : pad,
                   'meta'               : meta,      # to access by hash, like meta.author
                   'meta_list'          : meta_list, # to access all meta info in a (key, value) list
                   'text'               : text,
                   'mode'               : 'read',
                   'namespaces'         : namespaces,
                   'authorship_authors_json' : authorship_authors_json,
                   'authors'            : authors }

    if not request.user.is_authenticated():
        request.session.set_test_cookie()
        tpl_params['next'] = reverse('pad-write', args=(slug,) )

    return render_to_response("pad-read.html", tpl_params, context_instance = RequestContext(request))

def home(request):
    try:
        Pad.objects.get(display_slug=HOME_PAD)
        return pad_read(request, slug=HOME_PAD)
    except Pad.DoesNotExist:
        return HttpResponseRedirect(reverse('login'))

def css(request):
    try:
        pad = Pad.objects.get(display_slug='style.css')
        padID = pad.group.groupID + '$' + urllib.quote_plus(pad.name.replace('::', '_'))
        epclient = EtherpadLiteClient(pad.server.apikey, pad.server.apiurl)
        return HttpResponse(epclient.getText(padID)['text'], mimetype="text/css")
    except:
        # If there is no pad called "css", loads a default css file
        f = open('relearn/static/css/style.css', 'r')
        css = f.read()
        f.close()
        return HttpResponse(css, mimetype="text/css")

def cssprint(request):
    try:
        pad = Pad.objects.get(display_slug='print.css')
        padID = pad.group.groupID + '$' + urllib.quote_plus(pad.name.replace('::', '_'))
        epclient = EtherpadLiteClient(pad.server.apikey, pad.server.apiurl)
        return HttpResponse(epclient.getText(padID)['text'], mimetype="text/css")
    except:
        # If there is no pad called "css", loads a default css file
        f = open('relearn/static/css/print.css', 'r')
        css = f.read()
        f.close()
        return HttpResponse(css, mimetype="text/css")
