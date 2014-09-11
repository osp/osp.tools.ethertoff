from django.http import HttpResponseServerError
from django.template import Context, Template, loader

from urllib2 import URLError
from relearn.context_processors import EthertoffError
from etherpadlite.models import Pad, PadAuthor, PadServer

from html5lib import HTMLParser, serializer, treebuilders, treewalkers

def tidy(html):
    parser = HTMLParser(tree=treebuilders.getTreeBuilder("lxml"), namespaceHTMLElements=False)
    p = parser.parse(html, encoding=None, parseMeta=True, useChardet=True)
    s = serializer.htmlserializer.HTMLSerializer(quote_attr_values = True,
                                                 omit_optional_tags = False,
                                                 minimize_boolean_attributes = False,
                                                 use_trailing_solidus = True,
                                                 space_before_trailing_solidus = True,
                                                 escape_lt_in_attrs = False,
                                                 escape_rcdata = False,
                                                 resolve_entities = True,
                                                 alphabetical_attributes = False,
                                                 inject_meta_charset = True,
                                                 strip_whitespace = False,
                                                 sanitize = False)

    walker = treewalkers.getTreeWalker("lxml")
    stream = walker(p)
    output_generator = s.serialize(stream)

    return ''.join(o for o in output_generator)

class ErrorHandlingMiddleware(object):
    """
    Catch errors if we can make some reasonable prediction about what went wrong
    """
    def process_exception(self, request, exception):
        path   = request.get_host() + request.path
        reason = None
        if isinstance(exception, URLError):
            reason = "This means Ethertoff has trouble connecting to your Etherpad Lite instance. Either Etherpad Lite it is not running, or the address that you set in the admin is incorrect. Note: for security reasons, Etherpad Lite and Ethertoff need to be served from the same domain. You could run Ethertoff from the root folder and Etherpad from the folder /ether/ for example."
        elif isinstance(exception, EthertoffError):
            reason = str(exception)
        if reason:
            t = loader.get_template('500.html')
            tpl_variables = { 'path'      : path,
                              'exception' : exception,
                              'reason'    : reason }
            return HttpResponseServerError(t.render(Context(tpl_variables)))
        return None

class TidyMiddleware(object):
    # cf http://pyevolve.sourceforge.net/wordpress/?p=814
    def process_response(self, request, response):
        if 'admin' in request.path:
            return response
        if response.status_code == 200:
            if response["content-type"].startswith("text/html"):
                response.content = tidy(response.content)
        return response
