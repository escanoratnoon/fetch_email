import os
import imaplib
import email
from email.header import decode_header

PATH = '/home/mohsinali/Projects/Alphavu/fetch_email/emails/'
USERNAME = os.getenv('IMAP_ADDRESS')
PASSWORD = os.getenv('IMAP_PASSWORD')

if not os.path.exists(PATH):
    os.mkdir(PATH)

os.chdir(PATH)

imap = imaplib.IMAP4_SSL('outlook.office365.com')
imap.login(USERNAME, PASSWORD)

status, messages_count = imap.select('INBOX')
messages_count = int(messages_count[0])

if status == 'OK':
    print('Connection established.')
    print(f'{messages_count} mails found.')

for i in reversed(range(messages_count)):
    index = str(i + 1)

    if not os.path.exists(PATH + index):
        os.mkdir(PATH + index)
    os.chdir(PATH + index)

    res, msg = imap.fetch(index, '(RFC822)')
    for response in msg:
        os.chdir(PATH + index)
        if isinstance(response, tuple):
            ID = response[0].decode('utf-8')
            msg = email.message_from_bytes(response[1])

            subject, encoding = decode_header(msg['Subject'])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding)

            sender, encoding = decode_header(msg.get('From'))[0]
            if isinstance(sender, bytes):
                sender = sender.decode(encoding)

            print('Subject:', subject)
            print('From:', sender)
            with open('header.txt', 'w+') as header:
                header.write(f'ID: {ID}\nSender: {sender}\nSubject: {subject}')

            if msg.is_multipart():
                for part in msg.walk():
                    os.chdir(PATH + index)
                    content_type = part.get_content_type()
                    content_disposition = str(part.get('Content-Disposition'))
                    try:
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass
                    if content_type == 'text/plain' and 'attachment' not in content_disposition:
                        with open('body.txt', 'w+') as file:
                            file.write(str(body))

                    elif 'attachment' in content_disposition:
                        attachments_path = PATH + index + '/attachemnts'
                        if not os.path.exists(attachments_path):
                            os.mkdir(attachments_path)
                        os.chdir(attachments_path)
                        filename = part.get_filename()
                        if filename:
                            with open(filename, 'wb') as attachment:
                                attachment.write(part.get_payload(decode=True))
            else:
                content_type = msg.get_content_type()
                if content_type == 'text/plain':
                    with open('body.txt', 'w+') as file:
                        file.write(str(body))

            if content_type == 'text/html':
                os.chdir(PATH + index)
                with open('body.html', 'w+') as file:
                    file.write(str(body))
            print('*' * 100)

imap.close()
imap.logout()
