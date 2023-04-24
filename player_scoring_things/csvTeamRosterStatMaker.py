import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
import time
from unidecode import unidecode
import numpy as np
from itertools import chain


#make sure do not go over rate limit of 20 requests per minute. If over, sportsreference puts in "jail" for an hour
rate = 0
def checkRate(r):
    global rate
    #if r > 16:
        #rate = 0
    time.sleep(5)

#since roster table is hidden in comments, needs this to fish it out
def makeCommentTable(soup1, type):
    global rate

    #finds all comments in soup and makes them not comments and just html. 
    comments = soup1.find_all(string=lambda text: isinstance(text, Comment) and "table_container" in text)
    html = str(comments).replace('<!--', '').replace('-->', '')
    
    #parse through the HTML content using Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    #reads roster table html into a dataframe
    if type == False:
        #find the roster table by its HTML id
        rosterTable = soup.find('table', {'id': 'roster'})
        df = pd.read_html(str(rosterTable))[0]
    else:
        passingTable = soup.find('table', {'id': 'passing'})
        otherTable = soup.find('table', {'id': 'rushing_and_receiving'})

        #make array of two df instead of one, then flatten it to 1d array to be used later
        df = [pd.read_html(str(passingTable)), pd.read_html(str(otherTable))]
        df = list(chain.from_iterable(df))

    return df

def rosterMaker():

    #empty df to add things to
    df = pd.DataFrame(columns= ["No.", "Player", "Age", "Pos", "G", "GS", "Wt", "Ht", "College/Univ", "BirthDate", "Yrs", "AV", "Drafted (tm/rnd/yr)", "Year", "YearsBack", "Team"])

    global rate

    #years used for grading. changes each season. if making currYearRoster, use array below with current year
    #years = ["2022", "2021", "2020", "2019"]
    years = ["2023"]

    #team abbr list
    teams = ["crd", "atl", "rav", "buf", "car", "chi", "cin", "cle", "dal", "den", "det", "gnb", "htx", "clt", "jax", "kan", "rai", "sdg", "ram", "mia", "min", "nwe", "nor", "nyg", "nyj", "phi", "pit", "sfo", "sea", "tam", "oti", "was"]

    #used to find yearsback from present
    x = 1

    #loop to go through each team in each year and make df of roster for each team per year
    for num in years:
        for item in teams: 
            #makes url for every team
            url = "https://www.pro-football-reference.com/teams/" + item + "/" + num + "_roster.htm"

            #get page wanted and make a beautiful soup out of it.
            checkRate(rate)
            response = requests.get(url)
            print(response)
            rate += 1

            soup = BeautifulSoup(response.text, 'html.parser')

            #dataframe of table
            table = makeCommentTable(soup, False)

            #add in year and years back columns
            table['Year'] = num
            table["YearsBack"] = x
            table["Team"] = item


            #make all into one df
            df = pd.concat([df, table], ignore_index=True, join="inner")
                
        x+=1
        
        
    
    #write dfs into csv files for later use
    if len(years)==1:
        #change all rb type positions to rb
        rbValues = ['RB', 'HB', 'TB', 'FB', "LH", "RH", "BB", "B", "WB"]
        df.loc[df['Pos'].isin(rbValues), 'Pos'] = "RB"

        #make only first two strings kept, and only keep rb, wr, qb, te columns
        df.loc[df['Pos'].str.len() > 2, 'Pos'] = df.loc[df['Pos'].str.len() > 2, 'Pos'].apply(lambda x: x[:2])
        keepers = ["RB", "QB", "TE", "WR"]

        df = df.loc[df['Pos'].isin(keepers)]

        df.to_csv("player_scoring_things/all_rosters_stats_and_av_csvs/currYearRoster.csv", encoding='utf-8', index=False)
    else:
        df.to_csv("player_scoring_things/all_rosters_stats_and_av_csvs/teamsPastRoster.csv", encoding='utf-8', index=False)

def statMaker():
    global rate

    years = ["2022", "2021", "2020", "2019"]

    #team abbr list
    teams = ["crd", "atl", "rav", "buf", "car", "chi", "cin", "cle", "dal", "den", "det", "gnb", "htx", "clt", "jax", "kan", "rai", "sdg", "ram", "mia", "min", "nwe", "nor", "nyg", "nyj", "phi", "pit", "sfo", "sea", "tam", "oti", "was"]

    #empty df to add things to
    passingCol = ["No.", "Player", 'Age', 'Pos', 'G', 'GS', 'QBrec', 'Cmp', 'Att', 'Cmp%', 'Yds', 'TD', 'TD%', 'Int', 'Int%', 'Lng', 'Y/A', 'AY/A', 'Y/C', 'Y/G', 'Rate', 'QBR', 'Sk', 'Sk%', 'NY/A', 'ANY/A', '4QC', 'GWD', "RushAtt", "RushYds", "RushTD", "Fmb", "Year", "YearsBack", "Team"]
    passing = pd.DataFrame(columns= passingCol)

    #empty df to add things to
    rushRecCol = ["No.", "Player", 'Age', 'Pos', 'G', 'GS', 'Att', 'RushYds', 'RushTD', 'RushLng', 'Y/A', 'RushY/G', 'A/G', 'Tgt', 'Rec', 'RecYds', 'Y/R', 'RecTD', 'RecLng', 'R/G', 'RecY/G', 'Ctch%', 'Y/Tgt', 'Touch', 'Y/Tch', 'YScm', 'RRTD', 'Fmb', "Year", "YearsBack", "Team"]
    rushRec = pd.DataFrame(columns= rushRecCol)

    #to find years back
    x = 1

    #loop to go through each team in each year and make df of stats of passing/rushRec for each team per year
    for num in years:
        for item in teams: 
            #makes url for every team
            url = "https://www.pro-football-reference.com/teams/" + item + "/" + num + ".htm"

            #get page wanted and make a beautiful soup out of it.
            checkRate(rate)
            response = requests.get(url)
            print(response)
            rate += 1

            soup = BeautifulSoup(response.text, 'html.parser')

            #dataframe of table
            table = makeCommentTable(soup, True)

            passingDF = table[0]
            rushRecDF = table[1]


            #make it single index
            rushRecDF.columns = rushRecDF.columns.droplevel()

            #add in rushing columns for qbs
            passingDF["RushAtt"] = 0
            passingDF["RushTD"] = 0
            passingDF["RushYds"] = 0
            passingDF["Fmb"] = 0

            #add in year, team and years back columns
            passingDF["Year"] = num
            passingDF["YearsBack"] = x
            passingDF["Team"] = item
            rushRecDF["Year"] = num
            rushRecDF["YearsBack"] = x
            rushRecDF["Team"] = item
           

            #since there was duplicate column headers, have to change that so there isnt.
            rushRecDF.columns = ["No.", "Player", 'Age', 'Pos', 'G', 'GS', 'Att', 'RushYds', 'RushTD', 'RushLng', 'Y/A', 'RushY/G', 'A/G', 'Tgt', 'Rec', 'RecYds', 'Y/R', 'RecTD', 'RecLng', 'R/G', 'RecY/G', 'Ctch%', 'Y/Tgt', 'Touch', 'Y/Tch', 'YScm', 'RRTD', 'Fmb', "Year", "YearsBack", "Team"]
            
            #make passing/qb df into full stats needed for grading from this section
            for i in range(len(passingDF)):
                currRow = passingDF.iloc[[i]]

                playerStatsRush = rushRecDF.loc[(rushRecDF['Player'] == currRow["Player"].item()) & (rushRecDF["Year"] == currRow["Year"].item())]

                #make sure there actually is a rushrec row for player
                if len(playerStatsRush) > 0:
                    passingDF.iloc[i, passingDF.columns.get_loc("RushAtt")] = playerStatsRush["Att"]
                    passingDF.iloc[i, passingDF.columns.get_loc("RushTD")] = playerStatsRush["RushTD"]
                    passingDF.iloc[i, passingDF.columns.get_loc("RushYds")] = playerStatsRush["RushYds"]
                    passingDF.iloc[i, passingDF.columns.get_loc("Fmb")] = playerStatsRush["Fmb"]
                
            #make all into one df
            passing = pd.concat([passing, passingDF], ignore_index=True, join="inner")
            rushRec = pd.concat([rushRec, rushRecDF], ignore_index=True, join="inner")
            
        

        x+=1  


    #cleaning/combing data into one final dataframe
    passing = passing.loc[passing['Pos'] == "QB"]

    #replace NaN with 0
    passing.fillna(0, inplace=True)
    rushRec.fillna(0, inplace=True)

    #drop totals rows
    passing.drop(passing[passing['Player'] == 'Team Total'].index, inplace = True)
    passing.drop(passing[passing['Player'] == 'Opp Total'].index, inplace = True)

    rushRec.drop(rushRec[rushRec['Player'] == 'Team Total'].index, inplace = True)
    rushRec.drop(rushRec[rushRec['Player'] == 'Opp Total'].index, inplace = True)
    



    #remove *+ that say if pro bowler or not for simplicity.
    passing["Player"] = passing["Player"].str.replace("*", "")
    passing["Player"] = passing["Player"].str.replace("+", "")
    rushRec["Player"] = rushRec["Player"].str.replace("*", "")
    rushRec["Player"] = rushRec["Player"].str.replace("+", "")

    print(passing)
    print(rushRec)

    #write into csv
    passing.to_csv("player_scoring_things/all_rosters_stats_and_av_csvs/teamsOldQBStats.csv", encoding='utf-8', index=False)
    rushRec.to_csv("player_scoring_things/all_rosters_stats_and_av_csvs/teamsOldRushRecStats.csv", encoding='utf-8', index=False)
             

#comment out whichever one you are not running.
#rosterMaker()
statMaker()
