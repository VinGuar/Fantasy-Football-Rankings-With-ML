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


#since roster table is hidden in comments, needs this to fish it out
def makeCommentTable(soup1):

    #finds all comments in soup. 
    comments = soup1.find_all(string=lambda text: isinstance(text, Comment))

    #this iterates through each of comments "things" and sees if it has table. If it is table, appends to table array.
    allTables = []
    for things in comments:
        if 'table' in things:
            try:
                return pd.read_html(things)[0]
            except:
                continue

    return allTables


#team abbrevitions
teams = ["crd", "atl", "rav", "buf", "car", "chi", "cin", "cle", "dal", "den", "det", "gnb", "htx", "clt", "jax", "kan", "rai", "sdg", "ram", "mia", "min", "nwe", "nor", "nyg", "nyj", "phi", "pit", "sfo", "sea", "tam", "oti", "was"]

#array of each teams grade per positional groups
dictOfTeamsGrade = []

#array of dictionaries of all teams previous year roster with AV
statsPrevious = []


#make statPrevious array
"""for item in teams: 

    #makes url for every team
    url = "https://www.pro-football-reference.com/teams/" + item + "/2022_roster.htm"

    #get page wanted and make a beautiful soup out of it.
    checkRate(rate)
    response = requests.get(url)
    rate += 1

    soup = BeautifulSoup(response.text, 'html.parser')

    table = makeCommentTable(soup)

    #append table for current team in loop to all teams
    statsPrevious.append(table)



print(statsPrevious)"""

for item in teams:
    #arrays for positional grading
    oline = []
    rbs = []
    wrs = []
    tes = []
    
    #get urls table for current team
    #url = "https://www.pro-football-reference.com/teams/" + item + "/2023_roster.htm"
    url = "https://www.pro-football-reference.com/teams/" + "was" + "/2023_roster.htm"

    checkRate(rate)
    response = requests.get(url)
    rate += 1

    soupCurrent = BeautifulSoup(response.text, 'html.parser')
    currTable = makeCommentTable(soupCurrent)

    #gets df to be only positions wanted and non rookies
    posWanted = ["QB", "WR", "RB", "TE", "OL", "C", "T", "G"]
    currTable = currTable.loc[currTable['Pos'].isin(posWanted)]
    currTable = currTable[currTable.Yrs != "Rook"]

    print(currTable)


    if rate == 1:
        break


print(dictOfTeamsGrade)









