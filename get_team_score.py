import requests
import pickle
from collections import defaultdict
from itertools import combinations
from unidecode import unidecode

from bs4 import BeautifulSoup as bs


class Rider(object):
    def __init__(self, name, price, style, points):
        self.name = name
        self.price = price
        self.style = style
        self.points = points

    def __repr__(self):
        return str((self.name, self.style, self.points))

p = requests.get('https://www.velogames.com/italy/2019/riders.php')
soup = bs(p.content, 'html.parser')
table = soup.find('tbody')
riders = [Rider(list(row.findAll('td'))[1].text,
                int(list(row.findAll('td'))[-1].text),
                list(row.findAll('td'))[3].text,
                int(list(row.findAll('td'))[-2].text))
          for row in table.findAll('tr')]

example_team = ('Primoz Roglic',
                'Miguel Angel Lopez',
                'Mikel Landa',
                'Arnaud Demare',
                'Davide Formolo',
                'Pavel Sivakov',
                'Ryan Gibbons',
                'Tobias Ludvigsson',
                'Matteo Moschetti')

team = [rider for rider in riders if unidecode(rider.name) in example_team]

for rider in team:
    print('{:20}{:4d}'.format(rider.name, rider.points))
print('total score: {:d}'.format(sum([r.points for r in team])))


