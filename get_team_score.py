import requests
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

p = requests.get('https://www.velogames.com/spain/2019/riders.phps')
soup = bs(p.content, 'html.parser')
table = soup.find('tbody')
riders = [Rider(list(row.findAll('td'))[1].text,
                int(list(row.findAll('td'))[-1].text),
                list(row.findAll('td'))[3].text,
                int(list(row.findAll('td'))[-2].text))
          for row in table.findAll('tr')]

example_team = ('Alejandro Valverde',
                'Nairo Quintana',
                'Jakob Fuglsang',
                'Tadej Pogačar',
                'Wout Poels',
                'Ion Izagirre',
                'Zdeněk Štybar',
                'Luis Leon Sánchez',
                'Philippe Gilbert')

team = [rider for rider in riders if unidecode(rider.name) in example_team]

for rider in team:
    print('{:20}{:5d}'.format(rider.name, rider.points))
print('{}\n{:25d}'.format('='*25,sum([r.points for r in team])))


