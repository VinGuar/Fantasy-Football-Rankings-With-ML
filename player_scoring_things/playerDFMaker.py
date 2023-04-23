import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
import time
from unidecode import unidecode
import numpy as np
from itertools import chain

def dfMaker():

    #if ppr is 0 it is non ppr, if it is 1 it is half ppr, if its 2 it is full ppr
    ppr = 0

    #read csv files into pandas
    oldQBStats = pd.read_csv("player_scoring_things/all_rosters_stats_and_av_csvs/teamsOldQBStats.csv")
    oldRushRecStats = pd.read_csv("player_scoring_things/all_rosters_stats_and_av_csvs/teamsOldRushRecStats.csv")
    currTeamsRoster = pd.read_csv("player_scoring_things/all_rosters_stats_and_av_csvs/currYearRoster.csv")
    pastTeamsRoster = pd.read_csv("player_scoring_things/all_rosters_stats_and_av_csvs/teamsPastRoster.csv")
    currAVs = pd.read_csv("player_scoring_things/all_rosters_stats_and_av_csvs/teamsAVGrades.csv")

    completeDFQB = pd.DataFrame(columns= ["Age", "PassingYds", "PassingTD", "PassingAtt", "RushingYds", "RushingTD", "RushingAtt", "Int", "Fumbles", "PPG", "ol", "rb", "wr", "qb", "te"])
    completeDFOther = pd.DataFrame(columns= ["Age", "Tgt", "Rec", "RushingYds", "RushingTD", "RushingAtt", "ReceivingYds", "ReceivingTD", "Fumbles", "PPG", "ol", "rb", "wr", "qb", "te"])
    rookieList = []


    for index in range(len(currTeamsRoster)):
        #boolean to break if rookie
        breakBool = False

        individualDFQB = pd.DataFrame(columns= ["Age", "PassingYds", "PassingTD", "PassingAtt", "RushingYds", "RushingTD", "RushingAtt", "Int", "Fumbles", "PPG", "ol", "rb", "wr", "qb", "te"])
        individualDFOther = pd.DataFrame(columns= ["Age", "Tgt", "Rec", "RushingYds", "RushingTD", "RushingAtt", "ReceivingYds", "ReceivingTD", "Fumbles", "PPG", "ol", "rb", "wr", "qb", "te"])       
        individualDFOther.loc[0] = [0] * len(individualDFOther.columns)
        individualDFQB.loc[0] = [0] * len(individualDFQB.columns)

        year = currTeamsRoster.loc[index, 'Yrs']
        bday = currTeamsRoster.loc[index, 'BirthDate']
        pos = currTeamsRoster.loc[index, 'Pos']
        age = currTeamsRoster.loc[index, 'Age']
        name = currTeamsRoster.loc[index, 'Player']
        team = currTeamsRoster.loc[index, 'Team']

        games = 0

        #see if rookie
        if int(year) > 0:
            pass
        else:
            #add player to rookie column
            dict = {}
            dict = {"Name": name, "Year": year, "Bday": bday, "Age": age, "Team": team}
            rookieList.append(dict)
            continue
        
        totalStats = []
        while True:
            x = 1
            name = "Patrick Mahomes"
            pos = "QB"
            bday = "9/17/1995"            
            #get all player rows from past year
            playerRowRoster = pastTeamsRoster.loc[(pastTeamsRoster['Player'] == name) & (pastTeamsRoster["YearsBack"] == x) & (pastTeamsRoster["BirthDate"] == bday)].copy()
            playerRowRoster = playerRowRoster.reset_index()
            
            if playerRowRoster.empty:
                continue

            for ind in range(len(playerRowRoster)):
                teamCurr = playerRowRoster.loc[ind, "Team"]
                numberCurr = playerRowRoster.loc[ind, "No."]

                
                if pos == "QB":
                    playerRowStats = oldQBStats.loc[(oldQBStats["Team"]== teamCurr) & (oldQBStats["Player"]==name) & (oldQBStats["No."]==numberCurr) & (oldQBStats["YearsBack"]==x)]
                    playerRowStats = playerRowStats.reset_index() 
                                        
                    #add columns to each other to get df of stats per player
                    individualDFQB["PassingYds"] = playerRowStats.loc[0, "Yds"] + individualDFQB["PassingYds"]
                    individualDFQB["PassingTD"] = playerRowStats.loc[0, "TD"] + individualDFQB["PassingTD"]
                    individualDFQB["PassingAtt"] = playerRowStats.loc[0, "Att"] + individualDFQB["PassingAtt"]
                    individualDFQB["RushingYds"] = playerRowStats.loc[0, "RushYds"] + individualDFQB["RushingYds"]            
                    individualDFQB["RushingTD"] = playerRowStats.loc[0, "RushTD"] + individualDFQB["RushingTD"]            
                    individualDFQB["RushingAtt"] = playerRowStats.loc[0, "RushAtt"] + individualDFQB["RushingAtt"]            
                    individualDFQB["Int"] = playerRowStats.loc[0, "Int"] + individualDFQB["Int"]            
                    individualDFQB["Fumbles"] = playerRowStats.loc[0, "Fmb"] + individualDFQB["Fumbles"]    
                    games = games + playerRowStats.loc[ind, "G"]

                else:
                    playerRowStats = oldRushRecStats.loc[(oldRushRecStats["Team"]== teamCurr) & (oldRushRecStats["Player"]==name) & (oldRushRecStats["No."]==numberCurr) & (oldRushRecStats["YearsBack"]==x)]
                    playerRowStats = playerRowStats.reset_index() 

                    #add columns to each other to get df of stats per player
                    individualDFOther["Tgt"] = playerRowStats.loc[0, "Tgt"] + individualDFOther["Tgt"]
                    individualDFOther["Rec"] = playerRowStats.loc[0, "Rec"] + individualDFOther["Rec"]
                    individualDFOther["RushingYds"] = playerRowStats.loc[0, "RushYds"] + individualDFOther["RushingYds"]
                    individualDFOther["RushingTD"] = playerRowStats.loc[0, "RushTD"] + individualDFOther["RushingTD"]            
                    individualDFOther["RushingAtt"] = playerRowStats.loc[0, "Att"] + individualDFOther["RushingAtt"]            
                    individualDFOther["ReceivingYds"] = playerRowStats.loc[0, "RecYds"] + individualDFOther["ReceivingYds"]            
                    individualDFOther["ReceivingTD"] = playerRowStats.loc[0, "RecTD"] + individualDFOther["ReceivingTD"]            
                    individualDFOther["Fumbles"] = playerRowStats.loc[0, "Fmb"] + individualDFOther["Fumbles"]    

                    games = games + playerRowStats.loc[ind, "G"]

                print(games)
                
                if (games>6) or (x>3):
                    break
                elif (games<6) and (x>3):
                    #add player to rookie column
                    dict = {}
                    dict = {"Name": name, "Year": year, "Bday": bday, "Age": age, "Team": team}
                    rookieList.append(dict)
                    breakBool = True
            x+=1
            break
        #break if rookie
        if (breakBool == True):
            break

        if pos == "QB":
            #make it all per game not total
            individualDFQB["PassingYds"] = individualDFQB["PassingYds"]/games
            individualDFQB["PassingTD"] = individualDFQB["PassingTD"]/games
            individualDFQB["PassingAtt"] = individualDFQB["PassingAtt"]/games
            individualDFQB["RushingYds"] = individualDFQB["RushingYds"]/games         
            individualDFQB["RushingTD"] = individualDFQB["RushingTD"]/games            
            individualDFQB["RushingAtt"] = individualDFQB["RushingAtt"]/games            
            individualDFQB["Int"] = individualDFQB["Int"]/games            
            individualDFQB["Fumbles"] = individualDFQB["Fumbles"]/games  

            #add other columns needed
            individualDFQB["Age"] = age
            individualDFQB["ol"] = currAVs.loc[currAVs.index[currAVs['team'] == team], "ol"]
            individualDFQB["rb"] = currAVs.loc[currAVs.index[currAVs['team'] == team], "rb"]
            individualDFQB["wr"] = currAVs.loc[currAVs.index[currAVs['team'] == team], "wr"]
            individualDFQB["qb"] = currAVs.loc[currAVs.index[currAVs['team'] == team], "qb"]
            individualDFQB["te"] = currAVs.loc[currAVs.index[currAVs['team'] == team], "te"]

            completeDFQB = pd.concat([completeDFQB, individualDFQB], ignore_index=True, join="inner")                
                
            print(completeDFQB)

        else:
            #make it all per game not total
            individualDFOther["Tgt"] = individualDFOther["Tgt"]/games
            individualDFOther["Rec"] = individualDFOther["Rec"]/games
            individualDFOther["RushingYds"] = individualDFOther["RushingYds"]/games
            individualDFOther["RushingTD"] = individualDFOther["RushingTD"]/games            
            individualDFOther["RushingAtt"] = individualDFOther["RushingAtt"]/games            
            individualDFOther["ReceivingYds"] = individualDFOther["ReceivingYds"]/games            
            individualDFOther["ReceivingTD"] = individualDFOther["ReceivingTD"]/games            
            individualDFOther["Fumbles"] = individualDFOther["Fumbles"]/games   
                    
            #add other columns needed
            individualDFOther["Age"] = age
            individualDFOther["ol"] = currAVs.loc[currAVs.index[currAVs['team'] == team], "ol"]
            individualDFOther["rb"] = currAVs.loc[currAVs.index[currAVs['team'] == team], "rb"]
            individualDFOther["wr"] = currAVs.loc[currAVs.index[currAVs['team'] == team], "wr"]
            individualDFOther["qb"] = currAVs.loc[currAVs.index[currAVs['team'] == team], "qb"]
            individualDFOther["te"] = currAVs.loc[currAVs.index[currAVs['team'] == team], "te"]
            
            completeDFOther = pd.concat([completeDFOther, individualDFOther], ignore_index=True, join="inner")                
                
            print(completeDFOther)



        break

dfMaker()





    

