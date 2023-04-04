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

#takes positional dataframe and returns dataframe with only the player names.
def makePosArrays(df):
    array = []
    for index, row in df.iterrows():
        player = row["Player"]
        array.append(player)
    
    return array

#takes in positional array of players and dictionary of all teams players and finds each players AV and returns dict of that AV
def findAV(df, allPlayers):
    avValue = 0
    avDict = {}
    #iterates through small positional df
    for item in df:
        #iterates through large df of all players to see if it is in it, and if it is, adds the Av value to the player
        for thing in allPlayers:
            thing = thing[["Player", "AV"]]
            if len(thing[thing.Player == item]) >0:
                playerRow = thing[thing.Player == item]
                avValue = playerRow["AV"]
                avDict[item] = avValue.iloc[0]
    
    return avDict





    

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

    table = makeCommentTable(soup)

    #append table for current team in loop to all teams
    statsPrevious.append(table)

    




for item in teams:
    #arrays for positional grading
    oline = []
    rbs = []
    wrs = []
    tes = []
    qbs = []
    
    #get urls table for current team
    url = "https://www.pro-football-reference.com/teams/" + item + "/2023_roster.htm"

    checkRate(rate)
    response = requests.get(url)
    rate += 1

    soupCurrent = BeautifulSoup(response.text, 'html.parser')
    currTable = makeCommentTable(soupCurrent)

    #gets df to be only positions and columns wanted and non rookies, and resets index
    posWanted = ["QB", "WR", "RB", "TE", "OL", "C", "T", "G"]
    currTable = currTable.loc[currTable['Pos'].isin(posWanted)]
    currTable = currTable[currTable.Yrs != "Rook"]
    currTable = currTable.reset_index()
    currTable = currTable[["Player", "Pos"]]

    #make individual position arrays
    rbDF = currTable.loc[currTable['Pos'] == "RB"]
    wrDF = currTable.loc[currTable['Pos'] == "WR"]
    teDF = currTable.loc[currTable['Pos'] == "TE"]
    olstuff = ["OL", "C", "T", "G"]
    olDF = currTable.loc[currTable['Pos'].isin(olstuff)]
    qbDF = currTable.loc[currTable['Pos'] == "QB"]


    #make arrays of positons include the players
    oline = makePosArrays(olDF)
    rbs = makePosArrays(rbDF)
    wrs = makePosArrays(wrDF)
    tes = makePosArrays(teDF)
    qbs = makePosArrays(qbDF)
    rbAV = findAV(rbs, statsPrevious)

    #makes array of positions with AV values for players
    wrAV = findAV(wrs, statsPrevious)
    teAV = findAV(tes, statsPrevious)
    qbAV = findAV(qbs, statsPrevious)
    olAV = findAV(oline, statsPrevious)




    



    















