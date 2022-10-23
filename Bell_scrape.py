import numpy as np
import pandas as pd
from bs4 import BeautifulSoup 
import requests
import time 

from Bell_scrape_class import BellRezepte


# Define the url in python 
url = 'https://www.bell.ch/de/rezepte/alle-rezepte/'
# Fetching html from the website
page = requests.get(url)
# Initializing DataFrame to store the scraped URLs
recipe_url_df = pd.DataFrame()
# BeautifulSoup enables to find the elements/tags in a webpage 
soup = BeautifulSoup(page.text, 'html.parser')

# Filtering the urls to only ones containing german language recipes 
recipe_urls = pd.Series([a.get("href") for a in soup.find_all("a")])
recipe_urls = recipe_urls[(recipe_urls.str.count('-')>0) & 
(recipe_urls.str.contains('/rezepte/')==True) & 
(recipe_urls.str.contains('-rezepte/')==True) & 
(recipe_urls.str.endswith('rezepte/')==False)].unique()

# DataFrame to store the scraped URLs
df = pd.DataFrame({'recipe_urls':recipe_urls})
df['recipe_urls'] = "https://www.bell.ch" + df['recipe_urls'].astype('str')
# Appending 'df' to a main DataFrame 'recipe_urls_df'
recipe_df = recipe_url_df.append(df).copy()


# The list of recipe attributes we want to scrape
attribs = ['recipe_name', 'serves', 'cooking_time', 'difficulty', 'ingredients', 'directions', 'preferences', 'image']

# For each url (i) we add the attribute data to the i-th row
BellRezepte_df = pd.DataFrame(columns=attribs)
for i in range(0,len(recipe_df['recipe_urls'])):
    url = recipe_df['recipe_urls'][i]
    recipe_scraper = BellRezepte(url)
    BellRezepte_df.loc[i] = [getattr(recipe_scraper, attrib)() for attrib in attribs]

# Put all the data into the same dataframe
BellRezepte_df['recipe_urls'] = recipe_df['recipe_urls']
columns = ['recipe_urls'] + attribs
temp = BellRezepte_df[columns]

BellRezepte_df.to_json(r"./BellRezepte_full.json", orient='records')