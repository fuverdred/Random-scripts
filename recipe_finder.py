'''
A simple webscraper for ingredients and recipes, using the BBC good food site

Uses a slightly backwards method:
1. Use a list of ingredients to find recipes
2. Go through the recipes found and list all of the ingredient they require

Possible additions:
1. Check for duplicate recipes that have been scraped from common ingredients
2. Key words for differentiating similar ingredients. E.g. spicy peppers vs
   bell peppers. Excluding results with common words, E.g. Ignoring recipes
   requiring sweet potatoes when searching for potatoes.
3. Error handling. At the moment if you search for an ingredient with no
   recipes the program will throw an error, along with many other possible
   bugs.
'''


import requests
from collections import namedtuple, defaultdict

PAGE_LIMIT = 5 #  Scrape the first 5 pages of recipes
NO_RECIPES = 24 #  24 recipes per page

Recipe = namedtuple('Recipe', 'link name type ingredients')

from bs4 import BeautifulSoup

def get_recipes(ingredient):
    '''
    Takes in a string, e.g 'sweet potatoes' and searches the bbc food site for
    any recipes containing it, limiting the number of pages to PAGE_LIMIT.

    The names and links of the recipes are taken for further scraping
    '''
    base = 'https://www.bbc.com'
    url = base + '/food/search?q=' + '+'.join(ingredient.split())
    recipe_list = []

    p = requests.get(url)
    soup = BeautifulSoup(p.content, 'html.parser')

    num_results = int(soup.find(class_='gel-pica-bold').text)
    pages = num_results%NO_RECIPES + 1 #  Pages are not zero indexed
    
    for page in range(pages if pages < PAGE_LIMIT else PAGE_LIMIT):
        if page > 1: # Already have the first page
            p = requests.get(url + '&page=' + str(page))
            soup = BeautifulSoup(p.content, 'html.parser')

        recipes = soup.select('div.gel-layout.gel-layout--equal.promo-collection')
        for recipe in recipes[0].findAll(class_='promo'):
            link = base + recipe['href']
            name = recipe.find(class_='promo__title').text
            dish = recipe.find(class_='promo__type').text
            recipe_list.append(Recipe(link, name, dish, []))
    return recipe_list

def scrape_ingredients(recipe):
    '''
    Go to a specific recipe page and add all of the ingredients to the
    namedtuple storing the recipe
    '''
    p = requests.get(recipe.link)
    soup = BeautifulSoup(p.content, 'html.parser')

    ingredients = soup.findAll(class_='recipe-ingredients__list')
    for section in ingredients:
        for ingredient in section.children:
            recipe.ingredients.append(ingredient.text)
    

if __name__ == '__main__':
    example_ingredients = ['carrots', 'beetroot', 'sweet potatoes']
    recipes = []

    for ingredient in example_ingredients:
        print('Finding recipes including ', ingredient)
        recipes += get_recipes(ingredient)

    print('Scraping ingredients for recipes')
    for recipe in recipes:
        print(recipe.name)
        scrape_ingredients(recipe)

    
        
    
        
        
