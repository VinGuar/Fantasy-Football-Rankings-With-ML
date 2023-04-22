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


    for index in range(len(currTeamsRoster)):

        individualDFQB = pd.DataFrame(columns= ["Age", "PassingYds", "PassingTD", "PassingAtt", "RushingYds", "RushingTD", "RushingAtt", "Int", "Fumbles", "PPG", "ol", "rb", "wr", "qb", "te"])
        individualDFOther = pd.DataFrame(columns= ["Age", "Tgt", "Rec", "RushingYds", "RushingTD", "RushingAtt", "ReceivingYds", "ReceivingTD", "Fumbles", "PPG", "ol", "rb", "wr", "qb", "te"])       
        individualDFOther.loc[0] = [0] * len(individualDFOther.columns)

        year = currTeamsRoster.loc[index, 'Yrs']
        bday = currTeamsRoster.loc[index, 'BirthDate']
        pos = currTeamsRoster.loc[index, 'Pos']
        age = currTeamsRoster.loc[index, 'Age']
        name = currTeamsRoster.loc[index, 'Player']
        team = currTeamsRoster.loc[index, 'Team']

        #see if rookie
        if int(year) > 0:
            pass
        else:
            #YOOO THIS WHERE YOU PUT ROOKIE STUFF. also have place for it later if not enough data
            continue
        
        totalStats = []
        while True:
            x = 1
            name = "Christian McCaffrey"
            bday = "6/7/1996"            
            #get all player rows from past year
            playerRowRoster = pastTeamsRoster.loc[(pastTeamsRoster['Player'] == name) & (pastTeamsRoster["YearsBack"] == x) & (pastTeamsRoster["BirthDate"] == bday)].copy()
            playerRowRoster = playerRowRoster.reset_index()

            for ind in range(len(playerRowRoster)):
                teamCurr = playerRowRoster.loc[ind, "Team"]
                numberCurr = playerRowRoster.loc[ind, "No."]
                
                if pos == "QB":
                    playerRowStats = oldQBStats.loc[(oldQBStats["Team"]== teamCurr) & (oldQBStats["Player"]==name) & (oldQBStats["No."]==numberCurr) & oldQBStats["YearsBack"]==x]
                    playerRowStats = playerRowStats.reset_index() 

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

                #add other columns needed
                individualDFOther["Age"] = age
                print(currAVs)
                individualDFOther["Age"] = age
                individualDFOther["Age"] = age
                individualDFOther["Age"] = age
                individualDFOther["Age"] = age
                individualDFOther["Age"] = age

            
            
            print(individualDFOther)


            #if not playerRow.empty:
            x+=1
            break


        break

dfMaker()





    

