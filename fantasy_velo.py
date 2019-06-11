import requests
import pickle
from collections import defaultdict
from itertools import combinations

from bs4 import BeautifulSoup as bs

TEAM_SIZE = 9

EXCEPTIONS = {'Chris Froome': 'Christopher Froome',
              'Felix Großschartner': 'Felix Grossschartner',
              'Magnus Cort': '.php?id=132428',
              'Alexey Lutsenko': '.php?id=138294',
              'Mickaël Cherel': '.php?id=140603',
              'Paweł Bernas': '.php?id=134451',
              'Carl Fredrik Hagen': '.php?id=179795',
              'Steve Cummings': '.php?id=140584',
              'Bart De Clerq': '.php?id=140336',
              'Nic Dlamini': '.php?id=183449',
              'Cristian Camilo Muñoz': '.php?id=235292'}


class Rider(object):
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.points = 0

    def __repr__(self):
        return str((self.name, self.points))


def scrape_info():
    ###Scrape the riders from velogames################################
    p = requests.get('https://www.velogames.com/dauphine/2019/riders.php')
    soup = bs(p.content, 'html.parser')
    table = soup.find('tbody')
    riders = [Rider(list(row.findAll('td'))[1].text,
                    int(list(row.findAll('td'))[-1].text))
              for row in table.findAll('tr')]
    ###################################################################

    ###Scrape the points from Procyclingstats##########################
    def get_points(url):
        p = requests.get(url)
        soup = bs(p.content, 'html.parser')
        results = soup.find(class_='results')
        if results is None:
            print(url)
            return 0 #  PCS does not have a 404 page
        score = int(results.text.split()[-1])
        return score

    pcs_base = 'https://www.procyclingstats.com/rider/'
    for rider in riders:
        if rider.name in EXCEPTIONS.keys():
            if 'php' in EXCEPTIONS[rider.name]:
                url = pcs_base[:-1] + EXCEPTIONS[rider.name]
            else:
                url = pcs_base + '-'.join(EXCEPTIONS[rider.name].split())
        else:
            url = pcs_base + '-'.join(rider.name.split())
        print(url)
        points = get_points(url) + get_points(url + '/2018')
        rider.points = points
    ###################################################################
    return riders

riders = scrape_info()

by_price = defaultdict(list)

for rider in riders: #  Group riders by price
    by_price[rider.price].append(rider)

for key in by_price.keys(): # Sort each price by how many points they have
    by_price[key].sort(key=lambda x:x.points, reverse=True)

possibles = []

for price in by_price.keys():
    if price > 10:
        possibles += by_price[price]
    else:
        possibles += by_price[price][:3] #  Only a few of the chaff

best_team = []
best_score = 0

print('\n\nThis may take a while, cancel when '
      'you get bored for best team so far...\n\n')

for count, team in enumerate(combinations(possibles, TEAM_SIZE)):
    total_price = sum([rider.price for rider in team])
    if total_price > 100:
        continue #  Too expensive
    score = sum([rider.points for rider in team])
    if score > best_score:
        best_score = score
        best_team = team[:]

for rider in best_team:
    print('{:20}|{:4d}|{:6d}'.format(rider.name, rider.price, rider.points))
print('{:20}|{:4d}|{:6d}'.format('',
                                 sum([r.price for r in best_team]),
                                 sum([r.points for r in best_team])))
    
