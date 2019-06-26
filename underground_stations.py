import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/List_of_London_Underground_stations'
dic_url = 'http://www.greenworm.net/sites/default/files/gw-assets/enable1-wwf-v4.0-wordlist.txt'


p = requests.get(url)
soup = BeautifulSoup(p.content, 'html.parser')
table = soup.find(class_ = 'wikitable')
stations = [row.find('th').text[:-1].upper() for row in table.findAll('tr')][1:]

##with open('clean_dictionary.txt', 'r') as f:
##    words = [w[:-1] for w in f.readlines()]

words = requests.get(dic_url).text.split()
words = [w.upper() for w in words]

word_stations = [station for station in stations
        if all([word if word in words else False for word in station.split()])]

with open('c:/Users/Ferd/Documents/Crossword-Filler/themes/tube_stations.txt', 'w') as f:
    for station in word_stations:
        f.write(''.join(station.split())+'\n')
