import requests
from bs4 import BeautifulSoup
import pandas as pd 
import numpy as np
import re

class BellRezepte():
    """ This class will output the recipe details. Recipes have the
    following properties:
    Attributes:
        url: The url of the recipe on the Bell recipes site.
    Methods:
        Serves: How many people the recipe serves.
        Cooking time: What it says on the tin.
        Difficulty: Recipe difficulty.
        Ingredients: Recipe ingredients.
        Directions: Recipe directions.
        Preferences: Food preferences.
        Image: Image of the recipe.
    """
    def __init__(self, url):
        self.url = url 
        self.soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        
        first_div = self.soup.find('div', {'class': 'recipe-meta-item'})
        self.all_divs = [first_div] + first_div.find_next_siblings('div', {'class': 'recipe-meta-item'})
    
    def recipe_name(self):
        """ Locates the recipe title """
        try:
            return self.soup.find('h1').text.strip()
        except: 
            return np.nan
        
    def serves(self):
        """ Locates the number of people the meal serves """
        try:
            return self.soup.find('span', attrs={'class': 'recipe-servings-size'}).text.split()[0]
        except:
            return np.nan 

    def cooking_time(self):
        """ Locates the cooking time (in mins or hours and mins) """
        try:
            return ' '.join(self.all_divs[0].text.split())
        except:
            return np.nan

    def difficulty(self):
        """ Locates the cooking difficulty """
        try:
            return ''.join(self.all_divs[1].text.split())
        except:
            return np.nan

    def ingredients(self):
        """ Locates the ingredients of the recipe """
        try:
            quantity, name = [], []
            for i in range(0, len(self.soup.find_all('td')), 2):
                ingred = ' '.join(self.soup.find_all('td')[i].text.split())
                quantity.append(ingred)
            for i in range(1, len(self.soup.find_all('td')), 2):
                ingred = ' '.join(self.soup.find_all('td')[i].text.split())
                name.append(ingred)
            ingredients = [{"quantity": q, "name": n} for q, n in zip(quantity, name)]
            return ingredients
        except:
            return np.nan

    def directions(self):
        """ Locates the directions for cooking the recipe """
        try:
            directions = [] 
            for i in self.soup.find_all('div', {'class': 'col-md-8'}):
                d = ' '.join(i.text.split())
                d = d.replace('Zubereitung', '')
                directions.append(d)
            return directions[0]
        except:
            return np.nan

    def preferences(self):
        """" Locates the recipe preferences for the user """
        try:
            if len(self.all_divs) > 2:
                preferences = []
                for i in self.all_divs[2:]:
                    p = ' '.join(i.text.split())
                    preferences.append(p)
            return preferences
        except:
            return np.nan

    def image(self):
        """" Locates the image of the recipe meal """
        try:
            return self.soup.picture.img['src']
        except:
            return np.nan