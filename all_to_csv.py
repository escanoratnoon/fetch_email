import os
import pandas
import csv

PATH = '/home/mohsinali/Projects/Alphavu/fetch_email/emails'

with open(PATH + '/emails.csv', mode='w+') as email_csv:
    fieldnames = ['email_id', 'thread_id', 'thread_name', 'timestamp', 'sender_name', 'sender_email',
                  'receiver_name', 'receiver_email', 'subject', 'is_threaded', 'is_forwarded', 'content']
    emails_writer = csv.DictWriter(email_csv, fieldnames=fieldnames)
    emails_writer.writeheader()

dirs_to_iter = [os.path.join(PATH, a) for a in os.listdir(PATH) if a]

for dir in dirs_to_iter:
    print('DIR: ', dir)
    is_threaded = ''
    if os.path.exists(dir + '/header.csv'):
        data = pandas.read_csv(dir + '/header.csv')
        is_threaded = str(data['is_threaded'].values[0])
        with open(PATH + '/emails.csv', 'a') as f:
            data.to_csv(f, header=False, index= False)
    else:
        print('Header file not found.', dir)
        continue
    if is_threaded != 'False':
        print('THREADED', is_threaded)
        for root, dirs, files in os.walk(dir + '/replies'):
            for file in files:
                if file.endswith(".csv"):
                    print('file: ', dir + '/replies/' + file)
                    data = pandas.read_csv(str(dir + '/replies/' + file))
                    with open(PATH + '/emails.csv', 'a') as f:
                        print('OPENED')
                        data.to_csv(f, header=False, index= False)
