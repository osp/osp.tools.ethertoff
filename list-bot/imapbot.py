"""
This script connects to an IMAP mailbox, reads unread emails and mark them as
read.
"""


import os
import email
import imaplib
import settings as bot_settings

from django.template import Template, Context
from django.template import loader
from django.conf import settings


conn = imaplib.IMAP4_SSL(bot_settings.SERVER)

try:
    (retcode, capabilities) = conn.login(bot_settings.USER, bot_settings.PASSWORD)
except:
    print sys.exc_info()[1]
    sys.exit(1)

ret = conn.select() # Select inbox or default namespace

(retcode, messages) = conn.search(None, '(UNSEEN)')

if retcode == 'OK':
    PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
    settings.configure(
        TEMPLATE_DIRS=(os.path.join(PROJECT_DIR, 'templates'),),
    )
    t = loader.get_template('issue.html')

    for num in messages[0].split(' '):
        if num:
            typ, data = conn.fetch(num,'(RFC822)')
            msg = email.message_from_string(data[0][1])

            ret, data = conn.store(num,'+FLAGS', '\\Seen')

            if ret == 'OK':
                c = Context({
                    'from': msg.get('From'),
                    'date': msg.get('Date'),
                    'subject': msg.get('Subject'),
                    'body':msg.get_payload()
                })

                #print(t.render(c))

                # If needed we can save this html to file
                import codecs
                f = codecs.open('email.html', "w", encoding="utf-8")
                f.write(t.render(c))
                f.close()

conn.close()
