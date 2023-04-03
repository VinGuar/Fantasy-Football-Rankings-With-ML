import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
import time
from unidecode import unidecode

#make sure do not go over rate limit of 20 requests per minute. If over, sportsreference puts in "jail" for an hour
rate = 0
def checkRate(r):
    global rate
    if r > 16:
        rate = 0
        time.sleep(61)

#team abbrevitions
teams = ["crd", "atl", "rav", "buf", "car", "chi", "cin", "cle", "dal", "den", "det", "gnb", "htx", "clt", "jax", "kan", "rai", "sdg", "ram", "mia", "min", "nwe", "nor", "nyg", "nyj", "phi", "pit", "sfo", "sea", "tam", "oti", "was"]

#array of each teams grade per positional groups
dictOfTeamsGrade = []

#array of dictionaries of all teams previous year roster with AV
statsPrevious = []

#make statPrevious array
for item in teams: 

    #makes url for every team
    url = "https://www.pro-football-reference.com/teams/" + item + "/2022_roster.htm"

    #get page wanted and make a beautiful soup out of it.
    checkRate(rate)
    response = requests.get(url)
    rate += 1

    soup = BeautifulSoup(response.text, 'html.parser')


    #finds all comments in soup. Needed because the table we want is hidden in the comments.
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))

    #this iterates through each of comments "things" and sees if it has table. If it is table, appends to table array.
    allTables = []
    for things in comments:
        if 'table' in things:
            try:
                allTables.append(pd.read_html(things)[0])
            except:
                continue
    

    #append table for current team in loop to all teams
    statsPrevious.append(allTables)



print(statsPrevious)

