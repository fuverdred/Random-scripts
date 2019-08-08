'''
BNTO SCRAPER

Most recent BNTO comment 27327
'''

import requests
from bs4 import BeautifulSoup
import sys
from collections import namedtuple

BNTO_comment = namedtuple('BNTO_comment', 'url comments')

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

base = 'http://www.fifteensquared.net/guardian-'

def strip_bnto_comments(url, name='BNTO'):    
    p = requests.get(url)
    soup = BeautifulSoup(p.content, 'html.parser')

    comments = soup.findAll(class_='comment')
    BNTO_comments = []
    for comment in comments:
        if comment.find('cite').text == name:
            for p in comment.find_all('p'):
                print(p.text.translate(non_bmp_map))
                BNTO_comments.append(p.text.translate(non_bmp_map))
    return BNTO_comments
                
gathered = []
for puzzle_number in range(27894, 27327, -1):
    url = base + str(puzzle_number)
    print(url)
    comments = strip_bnto_comments(url, 'Alex')
    if comments:
        gathered.append(BNTO_comment(url, comments))
    

