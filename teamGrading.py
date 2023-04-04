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

#takes position and dict of positional grades and makes one grade per position and returns said grade.
def grader(dict2, pos):
    grade = 0

    #counting variables
    x = 0
    y = 1

    #how many players per position it wants to include in grade
    if pos == "qb":
        x = 1
    elif pos == "rb":
        x = 2
    elif pos == "wr":
        x = 3
    elif pos == "ol":
        x = 5
    elif pos == "te":
        x = 2
    
    sortedDict = sorted(dict2.items(), key=lambda x:x[1], reverse=True)

    for i in sortedDict:
        if y > x:
            break

        #the next large if loop grades them. gives different percentages based on if starter, 2nd, or 3rd string, etc.
        if (x == 1):
            grade = i[1]
        elif (x==2):
            if pos == "rb":
                if (y == 1):
                    grade = grade + i[1]*.7
                else:
                    grade = grade + i[1]*.3
            else:
                if (y == 1):
                    grade = grade + i[1]*.8
                else:
                    grade = grade + i[1]*.2
        elif (x==3):
            if (y == 1):
                grade = grade + i[1]*.38
            elif (y == 2):
                grade = grade + i[1]*.335
            else:
                grade = grade + i[1]*.285
        elif (x==5):
            if (y == 1):
                grade = grade + i[1]/5
            elif (y == 2):
                grade = grade + i[1]/5
            elif (y == 3):
                grade = grade + i[1]/5
            elif (y == 4):
                grade = grade + i[1]/5
            elif (y == 5):
                grade = grade + i[1]/5

        y+=1

    return grade


    

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
    ols = []
    rbs = []
    wrs = []
    tes = []
    qbs = []
    
    #get urls table for current team
    url = "https://www.pro-football-reference.com/teams/" + item + "/2023_roster.htm"

    checkRate(rate)
    response = requests.get(url)
    print(response)
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
    ols = makePosArrays(olDF)
    rbs = makePosArrays(rbDF)
    wrs = makePosArrays(wrDF)
    tes = makePosArrays(teDF)
    qbs = makePosArrays(qbDF)

    #makes array of positions with AV values for players
    rbAV = findAV(rbs, statsPrevious)
    wrAV = findAV(wrs, statsPrevious)
    teAV = findAV(tes, statsPrevious)
    qbAV = findAV(qbs, statsPrevious)
    olAV = findAV(ols, statsPrevious)

    #grades each position on each time
    rbGrade = grader(rbAV, "rb")
    wrGrade = grader(wrAV, "wr")
    teGrade = grader(teAV, "te")
    qbGrade = grader(qbAV, "qb")
    olGrade = grader(olAV, "ol")

    print(item, "rb", rbGrade)
    print(item, "wr", wrGrade)
    print(item, "te", teGrade)
    print(item, "qb", qbGrade)
    print(item, "ol", olGrade)
    print()



    









    



    















