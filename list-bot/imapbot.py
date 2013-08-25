"""
This script connects to an IMAP mailbox, reads unread emails and mark them as
read.
"""


import email
import imaplib
import settings


conn = imaplib.IMAP4_SSL(settings.SERVER)

try:
    (retcode, capabilities) = conn.login(settings.USER, settings.PASSWORD)
except:
    print sys.exc_info()[1]
    sys.exit(1)

ret = conn.select() # Select inbox or default namespace

(retcode, messages) = conn.search(None, '(UNSEEN)')

if retcode == 'OK':
    for num in messages[0].split(' '):
        if num:
            typ, data = conn.fetch(num,'(RFC822)')
            msg = email.message_from_string(data[0][1])

            from_ = msg.get('From')
            date = msg.get('Date')
            subject = msg.get('Subject')
            body = msg.get_payload()

            ret, data = conn.store(num,'+FLAGS', '\\Seen')

            if ret == 'OK':
                print(from_)
                print(date)
                print(subject)
                print(body)

conn.close()
