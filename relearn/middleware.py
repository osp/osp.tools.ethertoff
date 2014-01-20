from django.http import HttpResponseServerError
from django.template import Context, Template, loader

from urllib2 import URLError
from relearn.context_processors import EthertoffError
from etherpadlite.models import Pad, PadAuthor, PadServer

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
