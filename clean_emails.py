import os
from bs4 import BeautifulSoup
import re

PATH = os.getenv('DIR_PATH')

if os.path.isdir(PATH):
    os.chdir(PATH)
else:
    raise Exception('Custom Exception: Emails directory not found.')

dirs_to_iter = [os.path.join(PATH, a) for a in os.listdir(PATH) if a]

for dir in dirs_to_iter:

    has_text_body_ = False
    has_html_body_ = False

    textified = None
    if os.path.exists(dir + '/body.html'):
        focused_file = dir + '/body.html'
        with open(focused_file, 'r') as html_file:
            soup = BeautifulSoup(html_file, 'html.parser')
            textified = soup.get_text()

    elif os.path.exists(dir + '/body.txt'):
        focused_file = dir + '/body.txt'
        with open(focused_file, 'r') as text_file:
            textified = text_file.read()
    else:
        continue
    # with open(focused_file, 'r') as text_file:
    #     soup = BeautifulSoup(text_file, 'html.parser')
    #     textified_file = soup.get_text()
    #     resultant_string = ''

    if not textified:
        continue

    resultant_string = ''
    for line in textified.split('\n'):
        if line.strip():
            if '<' or '>' in line:
                line = line.replace('<', '')
                line = line.replace('>', '')
            resultant_string += (line.strip() + '\n')
        else:
            pass

    if u'\u00A0' in resultant_string:
        resultant_string = resultant_string.replace(u'\u00A0', '\n')

    with open(dir + '/processed.txt', 'w+',  encoding='utf-8') as processed_file:
        processed_file.write(resultant_string)
