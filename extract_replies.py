import os
import pandas
import re
import csv

PATH = os.getenv('DIR_PATH')

if os.path.isdir(PATH):
    os.chdir(PATH)
else:
    raise Exception('Custom Exception: Emails directory not found.')

dirs_to_iter = [os.path.join(PATH, a) for a in os.listdir(PATH) if a]

for dir in dirs_to_iter:
    is_threaded = ''
    if os.path.exists(dir + '/header.csv'):
        data = pandas.read_csv(dir + '/header.csv')
        is_threaded = str(data['is_threaded'].values[0])
    else:
        raise Exception('Header file not found.')

    if is_threaded == 'False':
        if os.path.exists(dir + '/processed.txt'):
            with open(dir + '/processed.txt', 'r') as content:
                data.loc[0, 'content'] = content.read()
            data.to_csv(dir + '/header.csv', index=False)
            continue
        else:
            continue

    if not os.path.exists(dir + '/replies'):
        os.mkdir(dir + '/replies')
    os.chdir(dir + '/replies')
    list_of_replies = []

    if not os.path.exists(dir + '/processed.txt'):
        continue

    with open(dir + '/processed.txt', 'r') as file:
        text_file = file.read()
        focus_string = ''
        for line in text_file.split('\n'):

            if line.lower().startswith('from:'):
                list_of_replies.append(focus_string)
                focus_string = ''
                focus_string += (line + '\n')

            else:
                focus_string += (line + '\n')

        list_of_replies.append(focus_string)

    data.loc[0, 'content'] = list_of_replies[0]
    data.to_csv(dir + '/header.csv', index=False)

    list_of_replies.pop(0)

    count = 1
    for list_item in list_of_replies:
        focus_string = ''
        sender = ''
        receiver = ''
        subject = ''
        date = ''
        cc = ''
        bcc = ''
        for line in list_item.split('\n'):

            if line.lower().startswith('from:'):
                sender = (' '.join(line.split(':')[1:])).strip()

            elif line.lower().startswith('to:'):
                receiver = (' '.join(line.split(':')[1:])).strip()

            elif line.lower().startswith('subject:'):
                subject = (' '.join(line.split(':')[1:])).strip()

            elif line.lower().startswith('sent:') or line.lower().startswith('date:'):
                date = (' '.join(line.split(':')[1:])).strip()

            elif line.lower().startswith('cc:'):
                cc = (' '.join(line.split(':')[1:]))

            elif line.lower().startswith('bcc:'):
                bcc = (' '.join(line.split(':')[1:]))

            else:
                focus_string += line

        try:
            sender_name = (' '.join(sender.split(' ')[:-1]))
            sender_name = re.sub(r'[",]', '', sender_name).strip()
            sender_email = sender.split(' ')[-1].replace(r'[<>]', '')
            sender_email = re.sub(r'[<>]', '', sender_email).strip()
        except:
            sender_name = None
            sender_email = re.sub(r'[<>]', '', sender)

        try:
            receiver_name = (' '.join(receiver.split(' ')[:-1]))
            receiver_name = re.sub(r'[",]', '', receiver_name).strip()
            receiver_email = receiver.split(' ')[-1].replace(r'[<>]', '')
            receiver_email = re.sub(r'[<>]', '', receiver_email).strip()
        except:
            receiver_name = None
            receiver_email = re.sub(r'[<>]', '', receiver)

        # print('For', dir)
        # print('Sender:', reply_sender.strip())
        # print('Sender Name:', sender_name.strip())
        # print('Sender Email:', sender_email.strip())
        # print('Date:', reply_date.strip())
        # print('Receiver:', reply_receiver.strip())
        # print('Receiver Name:', receiver_name.strip())
        # print('Receiver Email:', receiver_email.strip())
        # print('Subject:', reply_subject.strip())
        # print('Text:'+focus_string+'\n')

        with open(f'reply_{count}.txt', 'w+') as reply_file:
            reply_file.write(list_item)

        with open(f'reply_{count}.csv', mode='w+') as csv_file:
            fieldnames = ['id', 'date', 'sender_name', 'sender_email', 'receiver_name', 'receiver_email',
                          'subject', 'is_threaded', 'is_forwarded', 'content']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'id': None, 'date': date, 'sender_name': sender_name, 'sender_email': sender_email,
                             'receiver_name': receiver_name, 'receiver_email': receiver_email,
                             'subject': subject, 'is_threaded': 'True', 'is_forwarded': None,
                             'content': focus_string})

        count += 1



