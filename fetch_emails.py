import os
import imaplib
import email
from email.header import decode_header
import csv
import re

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

            date, date_encoding = decode_header(msg['Date'])[0]
            if isinstance(date, bytes):
                date = date.decode(date_encoding)

            subject, subject_encoding = decode_header(msg['Subject'])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(subject_encoding)

            if 're:' in subject.lower():
                is_threaded = True
            else:
                is_threaded = False
            if 'fwd' in subject.lower():
                is_forwarded = True
            else:
                is_forwarded = False

            sender, sender_encoding = decode_header(msg.get('From'))[0]
            if isinstance(sender, bytes):
                sender = sender.decode(sender_encoding)

            # with open('header.txt', 'w+') as header:
            #     header.write(f'is_threaded: {is_threaded}\nSender: {sender}\nSubject: {subject}\nis_forwarded: {is_forwarded}\n'
            #                  f'ID: {ID}')

            with open('header.csv', mode='w') as csv_file:
                fieldnames = ['id', 'timestamp', 'sender_name', 'sender_email', 'receiver_name', 'receiver_email',
                              'subject', 'is_threaded', 'is_forwarded', 'content']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                try:
                    sender_name = (' '.join(sender.split(' ')[:-1]))
                    sender_name = re.sub(r'[",]', '', sender_name)
                    sender_email = sender.split(' ')[-1].replace(r'[<>]', '')
                    sender_email = re.sub(r'[<>]', '', sender_email)
                except:
                    print('Exception found:', sender)
                    sender_name = None
                    sender_email = re.sub(r'[<>]', '', sender)
                    print('Name:', sender_name, 'Email:', sender_email)
                writer.writerow({'id': ID, 'timestamp': date, 'sender_name': sender_name, 'sender_email': sender_email,
                                 'receiver_name': 'Capmetro Customer Support', 'receiver_email': 'capmetro.customersupport@alphavu.com',
                                 'subject': subject, 'is_threaded': is_threaded, 'is_forwarded': is_forwarded, 'content': 'None'})

            if msg.is_multipart():
                multipart_ = True
                for part in msg.walk():
                    os.chdir(PATH + index)
                    content_type = part.get_content_type()
                    content_disposition = str(part.get('Content-Disposition'))
                    try:
                        body = part.get_payload(decode=True).decode()
                    except:
                        print('Body not found for', sender_email, 'subject:', subject)
                        continue
                    if content_type == 'text/plain' and 'attachment' not in content_disposition:
                        with open('body.txt', 'w+') as file:
                            file.write(str(body))

                    elif content_type == 'text/html':
                        os.chdir(PATH + index)
                        with open('body.html', 'w+') as file:
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
                        misc_path = PATH + index + '/misc'
                        if not os.path.exists(misc_path):
                            os.mkdir(misc_path)
                        os.chdir(misc_path)
                        filename = part.get_filename()
                        if filename:
                            with open(filename, 'wb') as misc_file:
                                misc_file.write(part.get_payload(decode=True))

            else:
                multipart_ = False
                content_type = msg.get_content_type()
                try:
                    body = msg.get_payload(decode=True).decode()
                except:
                    pass
                if content_type == 'text/plain':
                    with open('body.txt', 'w+') as file:
                        file.write(str(body))
                if content_type == 'text/html':
                    os.chdir(PATH + index)
                    with open('body.html', 'w+') as file:
                        file.write(str(body))
    print(f'Fetched mail {index}.')
    print('*' * 100)

imap.close()
imap.logout()
