import os


with open('/home/mohsinali/Projects/Alphavu/fetch_email/emails/34/final.txt', 'r') as ftp:
    fts = ftp.read()

if '​' in fts:
    print('Found: ', fts)
    fts2 = fts.replace('​', '')
    print(fts2)

with open('/home/mohsinali/Projects/Alphavu/fetch_email/test/test.txt', 'w+') as tp:
    tp.write(fts)