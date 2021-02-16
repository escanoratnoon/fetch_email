import os
import pandas
from collections import namedtuple

PATH = '/home/mohsinali/Projects/Alphavu/fetch_email/emails'

if os.path.isdir(PATH):
    os.chdir(PATH)
else:
    raise Exception('Custom Exception: Emails directory not found.')

dirs_to_iter = [os.path.join(PATH, a) for a in os.listdir(PATH) if a]

Email = namedtuple('Email',
                   ['id', 'timestamp', 'sender_name', 'sender_email', 'receiver_name', 'receiver_email',
                    'subject', 'is_threaded', 'is_forwarded', 'content', 'reply'])

for dirr in dirs_to_iter:
    list_of_csvs = []
    if os.path.exists(dirr + '/header.csv'):
        data = pandas.read_csv(dirr + '/header.csv')
        list_of_csvs.append(data)
    else:
        print('Header not found..')
        continue

    if not data['is_threaded'].values[0]:
        print('No replies exist for this email.')
        continue

    print('Attaching reply files..')
    if os.path.exists(dirr + '/replies/'):
        for root, dirs, files in os.walk(dirr + '/replies/'):
            for file in files:
                if file.endswith('.csv'):
                    data = pandas.read_csv(dirr + '/replies/' + file)
                    list_of_csvs.append(data)
    else:
        print('No replies folder.')

    print('Item...', len(list_of_csvs))
    for item in list_of_csvs:
        print(item)

