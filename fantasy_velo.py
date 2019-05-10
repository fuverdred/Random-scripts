import requests
import pickle
from collections import defaultdict

from bs4 import BeautifulSoup as bs


class Rider(object):
    def __init__(self, name, price, style):
        self.name = name
        self.price = price
        self.style = style
        self.points = 0

    def __repr__(self):
        return self.name


def scrape_info():
    ###Scrape the riders from velogames################################
    p = requests.get('https://www.velogames.com/italy/2019/riders.php')
    soup = bs(p.content, 'html.parser')
    table = soup.find('tbody')
    riders = [Rider(list(row.findAll('td'))[1].text,
                    int(list(row.findAll('td'))[-1].text),
                    list(row.findAll('td'))[3].text)
              for row in table.findAll('tr')]
    ###################################################################

    ###Scrape the points from Procyclingstats##########################
    def get_points(name, year=''):
        pcs_base = 'https://www.procyclingstats.com/rider/'
        p = requests.get(pcs_base + '-'.join(name.split()) + '/' + str(year))
        soup = bs(p.content, 'html.parser')
        results = soup.find(class_='results')
        if results is None:
            return #  PCS does not have a 404 page
        score = int(results.text.split()[-1])
        return score

    for rider in riders:
        print(rider.name)
        score = get_points(rider.name)
        if score is not None:
            rider.points = score
    ###################################################################
    return riders

#riders = scrape_info()
with open('giro_riders.pickle', 'rb') as f:
    riders = pickle.load(f)

styles = defaultdict(list)
for rider in riders:
    styles[rider.style].append(rider)
    

def recursive(riders, team=[], price=0, score=0, depth=0):
    depth += 1
    #print(' '*depth, depth)

    global best_score
    global best_team

    if score > best_score and len(team)==9:
        best_score = score
        best_team = team

    if depth > 9 or 100-price > (100-depth)*4:
        return

    for index, rider in enumerate(riders, 1):
        if price + rider[1] > 100:
            continue

        team.append(rider)
        recursive(riders[index:], team, price+rider[1], score+rider[2], depth)
        team.remove(rider)

best_score = 0
best_team = None

#recursive(reduced)


