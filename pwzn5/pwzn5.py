import os
import requests
from bs4 import BeautifulSoup
import numpy as np
from scipy.signal import convolve2d
import re
import pandas as pd

def remove_non_single_spaces(text):
    out = re.sub(r'\s+', ' ', text)
    if len(out) > 0 and out[0] == ' ':
        return out[1:]
    else: 
        return out

def is_full_of_spaces(word):
    return all(char.isspace() for char in word)

url = "http://www.ufcstats.com/fighter-details/0d8011111be000b2"
#url = "http://www.ufcstats.com/fighter-details/1338e2c7480bdf9e"

try:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
except Exception as e:
    print(f"An unexpected error occurred: {e}")

tags = [tag.text for tag in soup.find_all('a')] 
tokens = []
for tag in tags:
    #print(tag)
    tmp_list = tag.split('\n')
    #print(tmp_list)
    tokens = tokens + tmp_list
    
tokens = [remove_non_single_spaces(element) for element in tokens]
tokens = [element for element in tokens if element != "" or element == "\n"]

#print(tokens[3:])

# for token in tokens[3:-5]:
#     print(token)

columns = ['FIGHTER', 'OPONENT', 'RESULT']
results = []
fighters = []
opp = []
for i in range(3, len(tokens[3:-5]), 4):
    chunk = tokens[i:i+4]
    #print(chunk)
    results.append(chunk[0])
    fighters.append(chunk[1])
    opp.append(chunk[2])

df = pd.DataFrame({'FIGHTER' : fighters, 'OPONENT' : opp, 'RESULT' : results})

print(df)