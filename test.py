import re
import uuid
import datefinder
# print(type(uuid.uuid4()))

strrr = 'On 10-12-2021 10:30 AM, Guy Burton <guyburton@live.com> wrote:'
matches = list(datefinder.find_dates(strrr))

if len(matches) > 0:
    # date returned will be a datetime.datetime object. here we are only using the first match.
    date = matches[0]
    print(date)
else:
    print('No dates found')
print()
#
# if re.search(r'wrote[:]$', strrr):
#     print('YES')
# email = re.search(r'[<](.*?)[>]', strrr).group(1)
#
# list = strrr.split(' ')
#
# list = list[1:-1]
#
# print(list)
#
#
# list.remove('<' + email + '>')
#
# print('email:', email)
#
# name = ' '.join(list[-2:]).strip()
#
# print('name:', name)
#
# list = list[:-2]
#
# date = ' '.join(list).strip()
#
# print('date:', date)