import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
import time
from unidecode import unidecode
import numpy as np


#make sure do not go over rate limit of 20 requests per minute. If over, sportsreference puts in "jail" for an hour
rate = 0
def checkRate(r):
    global rate
    time.sleep(5)


#since roster table is hidden in comments, needs this to fish it out
def makeCommentTable(soup1):
    global rate

    #finds all comments in soup and makes them not comments and just html. 
    comments = soup1.find_all(string=lambda text: isinstance(text, Comment) and "table_container" in text)
    roster_html = str(comments).replace('<!--', '').replace('-->', '')
    
    #parse through the HTML content using Beautiful Soup
    roster_soup = BeautifulSoup(roster_html, 'html.parser')

    #find the roster table by its HTML id
    table = roster_soup.find('table', {'id': 'roster'})

    #reads roster table html into a dataframe
    df = pd.read_html(str(table))[0]

    return df


#takes positional dataframe and returns array with only the player names.
def makePosArrays(df):
    global rate
    array = []
    for index, row in df.iterrows():
        player = row["Player"]
        array.append(player)
    
    return array


#takes in positional array of players and dictionary of all teams players, and birthdate/pos for verification, and finds each players AV and returns dict of that AV
def findAV(df, allPlayers, birthArray):
    global rate
    avValue = 0
    avDict = {}
    x = 0
    #iterates through small positional df
    for item in df:
        #iterates through large df of all players to see if it is in it, and if it is, adds the AV value to the player
        for thing in allPlayers:
            thing = thing[["Player", "AV", "Pos", "BirthDate"]]
            if len(thing[thing.Player == item]) >0:
                playerRow = thing[thing.Player == item]
                bday = playerRow["BirthDate"].iloc[0]
                #makes sure its not just same name, like how there are two josh allens. confirms with birthdays.
                if (bday == birthArray[x]):
                    avValue = playerRow["AV"]
                    avDict[item] = avValue.iloc[0]
        x+=1
    
    return avDict

#takes position and dict of positional grades and makes one grade per position and returns said grade.
def grader(dict2, pos):
    global rate
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
    
    #sort dictionary in order of AV Grade
    sortedDict = sorted(dict2.items(), key=lambda x:x[1], reverse=True)

    #for loop grades.
    for i in sortedDict:
        #breaks once it has done enough grades (does how ever large x is)
        if y > x:
            break

        #the next large if loop grades them. gives different percentages based on if starter, 2nd, or 3rd string, etc. also based on positions
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

#makes array that includes only bdays
def makeBday(df):
    array = []
    for index, row in df.iterrows():
        bday = row["BirthDate"]
        array.append(bday)

    return array
    

#team abbrevitions
teams = ["crd", "atl", "rav", "buf", "car", "chi", "cin", "cle", "dal", "den", "det", "gnb", "htx", "clt", "jax", "kan", "rai", "sdg", "ram", "mia", "min", "nwe", "nor", "nyg", "nyj", "phi", "pit", "sfo", "sea", "tam", "oti", "was"]

#years for machine learning. if x is true it uses them. 
#may have to split up the years into multiple smaller groups to prevent errors. then combine smaller csvs into the one main csv. 
#I split the 10 years (below) up into first 3, next 3, and last 4, and then combined them all to get csv shown in datasets_used_in_model
yearsBig = ["2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021"]
yearsSmall = ["2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019" "2020"]




#if x is true, it does the years in yearsBig and yearsSmall above(to get data for machine learning). 
#if false, it only does current year (for grading of players for rankings)
x = False

#array of each teams grade per positional groups
dictOfTeamsGrade = []

#array of dictionaries of all teams previous year roster with AV
statsPrevious = []

#to get multiple years of data
statsPreviousAll = []

#if the if statement is true it makes it of last ten years data to be used for machine learning. if false, just this year.
if x:
    pass
else: 
    yearsSmall = ["2022"] 
    yearsBig = ["2023"] 

#for loop gets data to use for grading of the next year
for arr in yearsSmall:
    print(arr + " small")
    for item in teams: 
        print(item + " small")
        #makes url for every team
        url = "https://www.pro-football-reference.com/teams/" + item + "/" + arr + "_roster.htm"

        #get page wanted and make a beautiful soup out of it.
        checkRate(rate)
        response = requests.get(url)
        print(response)
        rate += 1

        soup = BeautifulSoup(response.text, 'html.parser')

        table = makeCommentTable(soup)

        #append table for current team in loop to all teams
        statsPrevious.append(table)
                

    #appends current year to array with all years
    statsPreviousAll.append(statsPrevious)
    statsPrevious = []

#dictionary that has each teams grades
allTeams = {}

#has each teams grade for each year
bigYears = {}


q = 0


#grading the year with past data (achieved from yearsSmall in for loop above)
for arr in yearsBig:
    #if the if statement is true it makes it of last ten years data to be used for machine learning. if false, just this year.
    print(arr)
    #reset all teams dict
    allTeams = {}
    h = 0
    for item in teams:
        print(item)

        #arrays for positional grading
        
        ols = []
        rbs = []
        wrs = []
        tes = []
        qbs = []
        
        #get urls table for current team
        url = "https://www.pro-football-reference.com/teams/" + item + "/" + arr + "_roster.htm"

        checkRate(rate)
        response = requests.get(url)
        rate += 1
        print(response)

        soupCurrent = BeautifulSoup(response.text, 'html.parser')

        currTable = makeCommentTable(soupCurrent)

        #gets df to be only positions and columns wanted and non rookies, and resets index
        posWanted = ["QB", "WR", "RB", "TE", "OL", "C", "T", "G", "LG", "LT", "RG", "RT"]
        currTable = currTable.loc[currTable['Pos'].isin(posWanted)]
        currTable = currTable[currTable.Yrs != "Rook"]
        currTable = currTable.reset_index()
        currTable = currTable[["Player", "Pos", "BirthDate"]]

        #make individual position arrays
        rbDF = currTable.loc[currTable['Pos'] == "RB"]
        wrDF = currTable.loc[currTable['Pos'] == "WR"]
        teDF = currTable.loc[currTable['Pos'] == "TE"]
        olstuff = ["OL", "C", "T", "G", "LG", "LT", "RG", "RT"]
        olDF = currTable.loc[currTable['Pos'].isin(olstuff)]
        qbDF = currTable.loc[currTable['Pos'] == "QB"]

        #make array that has each positions bdays
        bdayRB = makeBday(rbDF)
        bdayWR = makeBday(wrDF)
        bdayTE = makeBday(teDF)
        bdayQB = makeBday(qbDF)
        bdayOL = makeBday(olDF)

        #make arrays of positons to include only the players
        ols = makePosArrays(olDF)
        rbs = makePosArrays(rbDF)
        wrs = makePosArrays(wrDF)
        tes = makePosArrays(teDF)
        qbs = makePosArrays(qbDF)

        #previous years stats
        stats = statsPreviousAll[q]

        #makes array of positions with AV values for players
        rbAV = findAV(rbs, stats, bdayRB)
        wrAV = findAV(wrs, stats, bdayWR)
        teAV = findAV(tes, stats, bdayTE)
        qbAV = findAV(qbs, stats, bdayQB)
        olAV = findAV(ols, stats, bdayOL)

        #grades each position on each time
        rbGrade = grader(rbAV, "rb")
        wrGrade = grader(wrAV, "wr")
        teGrade = grader(teAV, "te")
        qbGrade = grader(qbAV, "qb")
        olGrade = grader(olAV, "ol")

        #make dictionary and have teams grades of all position into main dictionary
        current = {}
        current["ol"] = olGrade
        current["rb"] = rbGrade
        current["wr"] = wrGrade
        current["qb"] = qbGrade
        current["te"] = teGrade
        allTeams[item] = current
        
    #to iterate through statsPreviousAll
    q = q + 1

    #add the year to whole year array
    bigYears[arr] = allTeams


#df that will have all years
largeDF = pd.DataFrame()

if x:
    for key in bigYears:
        #make dictionary into panda dataframe
        dfAll = pd.DataFrame.from_dict(bigYears[key], orient="index")

        #reset/add index
        dfAll = dfAll.reset_index()

        #rename index column as team column 
        dfAll.rename(columns = {'index':'team'}, inplace = True)

        #add column year
        dfAll['year'] = key

        #combine the dataframes into one large one
        largeDF = pd.concat([largeDF, dfAll], ignore_index=True, keys=None, levels=None, names=None, verify_integrity=False, copy=True)

    #make columns
    largeDF.columns = ["team", "ol", "rb", "wr", "qb", "te", "year"]

    #write dataframe into csv to be used later
    largeDF.to_csv("12Grades.csv", encoding='utf-8', index=False)

    print(largeDF)

    
else:
    #make dictionary into panda dataframe
    dfAll = pd.DataFrame.from_dict(allTeams, orient="index")

    #reset/add index
    dfAll = dfAll.reset_index()

    #rename index column as team column 
    dfAll.rename(columns = {'index':'team'}, inplace = True)

    #write dataframe into csv to be used later
    dfAll.to_csv("player_scoring_things/all_rosters_stats_and_av_csvs/teamsAVGrades.csv", encoding='utf-8', index=False)

    print(dfAll)









