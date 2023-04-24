import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
import time
from unidecode import unidecode
import numpy as np
from itertools import chain

def dfMaker():

    #if ppr is 0 it is non ppr, if it is 1 it is half ppr, if its 2 it is full ppr
    ppr = 2
    
    #read csv files into pandas
    oldQBStats = pd.read_csv("player_scoring_things/all_rosters_stats_and_av_csvs/teamsOldQBStats.csv")
    oldRushRecStats = pd.read_csv("player_scoring_things/all_rosters_stats_and_av_csvs/teamsOldRushRecStats.csv")
    currTeamsRoster = pd.read_csv("player_scoring_things/all_rosters_stats_and_av_csvs/currYearRoster.csv")
    pastTeamsRoster = pd.read_csv("player_scoring_things/all_rosters_stats_and_av_csvs/teamsPastRoster.csv")
    currAVs = pd.read_csv("player_scoring_things/all_rosters_stats_and_av_csvs/teamsAVGrades.csv")

    completeDFQB = pd.DataFrame(columns= ["Team", "Pos", "Penalty", "Games", "Name", "Age", "PassingYds", "PassingTD", "PassingAtt", "RushingYds", "RushingTD", "RushingAtt", "Int", "Fumbles", "PPG", "ol", "rb", "wr", "qb", "te"])
    completeDFOther = pd.DataFrame(columns= ["Team", "Pos", "Penalty", "Games", "Name", "Age", "Tgt", "Rec", "RushingYds", "RushingTD", "RushingAtt", "ReceivingYds", "ReceivingTD", "Fumbles", "PPG", "ol", "rb", "wr", "qb", "te"])
    rookieList = []

    f = 0
    for index in range(len(currTeamsRoster)):

        f+=1
        #boolean to break if rookie
        breakBool = False

        #years back variable
        x = 1

        #penalty variable for injuries
        penalty = 0

        individualDFQB = pd.DataFrame(columns= ["Team", "Pos", "Penalty", "Games", "Name", "Age", "PassingYds", "PassingTD", "PassingAtt", "RushingYds", "RushingTD", "RushingAtt", "Int", "Fumbles", "PPG", "ol", "rb", "wr", "qb", "te"])
        individualDFOther = pd.DataFrame(columns= ["Team", "Pos", "Penalty", "Games", "Name", "Age", "Tgt", "Rec", "RushingYds", "RushingTD", "RushingAtt", "ReceivingYds", "ReceivingTD", "Fumbles", "PPG", "ol", "rb", "wr", "qb", "te"])       
        individualDFOther.loc[0] = [0] * len(individualDFOther.columns)
        individualDFQB.loc[0] = [0] * len(individualDFQB.columns)

        year = currTeamsRoster.loc[index, 'Yrs']
        bday = currTeamsRoster.loc[index, 'BirthDate']
        pos = currTeamsRoster.loc[index, 'Pos']
        age = currTeamsRoster.loc[index, 'Age']
        name = currTeamsRoster.loc[index, 'Player']
        team = currTeamsRoster.loc[index, 'Team']
        print(name, team)

        games = 0

        #see if rookie
        if year == "Rook":
            #add player to rookie column
            dict = {}
            dict = {"Name": name, "Year": year, "Bday": bday, "Age": age, "Team": team}
            rookieList.append(dict)
            breakBool = True

            continue
        
        totalStats = []
        while True:
         
            #get all player rows from past year
            playerRowRoster = pastTeamsRoster.loc[(pastTeamsRoster['Player'] == name) & (pastTeamsRoster["YearsBack"] == x) & (pastTeamsRoster["BirthDate"] == bday)].copy()
            playerRowRoster = playerRowRoster.reset_index()
            
            if playerRowRoster.empty:
                if x>3:
                    if games>6:
                        break
                    elif (int(year)<4):
                        #add player to rookie column
                        dict = {}
                        dict = {"Name": name, "Year": year, "Bday": bday, "Age": age, "Team": team}
                        rookieList.append(dict)
                        breakBool = True
                        break
                    else:
                        breakBool = True
                        break

                x=x+1
                continue

            for ind in range(len(playerRowRoster)):
                teamCurr = playerRowRoster.loc[ind, "Team"]
                numberCurr = playerRowRoster.loc[ind, "No."]

                
                if pos == "QB":
                    playerRowStats = oldQBStats.loc[(oldQBStats["Team"]== teamCurr) & (oldQBStats["Player"]==name) & (oldQBStats["No."]==numberCurr) & (oldQBStats["YearsBack"]==x)]
                    playerRowStats = playerRowStats.reset_index() 
                    playerRowStats = playerRowStats.fillna(0)

                    if playerRowStats.empty:
                        continue
                                                
                    #add columns to each other to get df of stats per player
                    individualDFQB["PassingYds"] = playerRowStats.loc[0, "Yds"] + individualDFQB["PassingYds"]
                    individualDFQB["PassingTD"] = playerRowStats.loc[0, "TD"] + individualDFQB["PassingTD"]
                    individualDFQB["PassingAtt"] = playerRowStats.loc[0, "Att"] + individualDFQB["PassingAtt"]
                    individualDFQB["RushingYds"] = playerRowStats.loc[0, "RushYds"] + individualDFQB["RushingYds"]            
                    individualDFQB["RushingTD"] = playerRowStats.loc[0, "RushTD"] + individualDFQB["RushingTD"]            
                    individualDFQB["RushingAtt"] = playerRowStats.loc[0, "RushAtt"] + individualDFQB["RushingAtt"]            
                    individualDFQB["Int"] = playerRowStats.loc[0, "Int"] + individualDFQB["Int"]            
                    individualDFQB["Fumbles"] = playerRowStats.loc[0, "Fmb"] + individualDFQB["Fumbles"]    
                    games = games + playerRowStats.loc[0, "G"]

                else:
                    playerRowStats = oldRushRecStats.loc[(oldRushRecStats["Team"]== teamCurr) & (oldRushRecStats["Player"]==name) & (oldRushRecStats["No."]==numberCurr) & (oldRushRecStats["YearsBack"]==x)]
                    playerRowStats = playerRowStats.reset_index() 
                    playerRowStats = playerRowStats.fillna(0)
                    
                    if playerRowStats.empty:
                        continue

                    #add columns to each other to get df of stats per player
                    individualDFOther["Tgt"] = playerRowStats.loc[0, "Tgt"] + individualDFOther["Tgt"]
                    individualDFOther["Rec"] = playerRowStats.loc[0, "Rec"] + individualDFOther["Rec"]
                    individualDFOther["RushingYds"] = playerRowStats.loc[0, "RushYds"] + individualDFOther["RushingYds"]
                    individualDFOther["RushingTD"] = playerRowStats.loc[0, "RushTD"] + individualDFOther["RushingTD"]            
                    individualDFOther["RushingAtt"] = playerRowStats.loc[0, "Att"] + individualDFOther["RushingAtt"]            
                    individualDFOther["ReceivingYds"] = playerRowStats.loc[0, "RecYds"] + individualDFOther["ReceivingYds"]            
                    individualDFOther["ReceivingTD"] = playerRowStats.loc[0, "RecTD"] + individualDFOther["ReceivingTD"]            
                    individualDFOther["Fumbles"] = playerRowStats.loc[0, "Fmb"] + individualDFOther["Fumbles"]    

                    games = games + playerRowStats.loc[0, "G"]

                #add penalty variable
                if (x==1):
                    penalty = penalty + playerRowStats.loc[0, "G"]   
                elif (x==2):
                    penalty = penalty + (playerRowStats.loc[0, "G"]*0.8)   
                elif (x==3):
                    penalty = penalty + (playerRowStats.loc[0, "G"]*0.6)   
                elif (x==4):
                    penalty = penalty + (playerRowStats.loc[0, "G"]*0.4)   

            if (games<6) and (x>3) and (int(year)<4):
                #add player to rookie column
                dict = {}
                dict = {"Name": name, "Year": year, "Bday": bday, "Age": age, "Team": team}
                rookieList.append(dict)
                breakBool = True
                break
            elif (games<6) and (x>3):
                breakBool = True
                break
            if (games>6) or (x>3):
                break

            x+=1


        #break if rookie
        if (breakBool == True):
            continue

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
            individualDFQB["Name"] = name
            individualDFQB["Pos"] = pos
            individualDFQB["Team"] = team
            individualDFQB["Games"] = games
            individualDFQB["Penalty"] = penalty/games

            #ppg column
            individualDFQB.loc[:, "PPG"] = (individualDFQB["RushingYds"]*0.1) + (individualDFQB["PassingYds"]*.04) + (individualDFQB["RushingTD"]*6) + (individualDFQB["PassingTD"]*4) + (individualDFQB["Fumbles"]*-2) + (individualDFQB["Int"]*-2)
            individualDFQB.loc[:, "PPG"] = individualDFQB["PPG"]
            
            #add other columns needed
            individualDFQB["Age"] = age

            #locate row with correct team and pos and add it
            rowOL = currAVs.loc[currAVs['team'] == team].iloc[0]
            individualDFQB['ol'] = rowOL['ol']
            
            rowRB = currAVs.loc[currAVs['team'] == team].iloc[0]
            individualDFQB['rb'] = rowRB['rb']

                      
            rowWR = currAVs.loc[currAVs['team'] == team].iloc[0]
            individualDFQB['wr'] = rowWR['wr']

            rowQB = currAVs.loc[currAVs['team'] == team].iloc[0]
            individualDFQB['qb'] = rowQB['qb']

            rowTE = currAVs.loc[currAVs['team'] == team].iloc[0]
            individualDFQB['te'] = rowTE['te']

            completeDFQB = pd.concat([completeDFQB, individualDFQB], ignore_index=True, join="inner")                
                

        else:
            #make it all per game not total
            print(games)
            individualDFOther["Tgt"] = individualDFOther["Tgt"]/games
            individualDFOther["Rec"] = individualDFOther["Rec"]/games
            individualDFOther["RushingYds"] = individualDFOther["RushingYds"]/games
            individualDFOther["RushingTD"] = individualDFOther["RushingTD"]/games            
            individualDFOther["RushingAtt"] = individualDFOther["RushingAtt"]/games            
            individualDFOther["ReceivingYds"] = individualDFOther["ReceivingYds"]/games            
            individualDFOther["ReceivingTD"] = individualDFOther["ReceivingTD"]/games            
            individualDFOther["Fumbles"] = individualDFOther["Fumbles"]/games   
            individualDFOther["Name"] = name
            individualDFOther["Pos"] = pos
            individualDFOther["Team"] = team
            individualDFOther["Games"] = games
            individualDFOther["Penalty"] = penalty/games

            #ppg column
            individualDFOther.loc[:, "PPG"] = (individualDFOther["RushingYds"]*0.1) + (individualDFOther["ReceivingYds"]*0.1) + (individualDFOther["RushingTD"]*6) + (individualDFOther["ReceivingTD"]*6) + (individualDFOther["Fumbles"]*-2)
            if ppr == 2:
                individualDFOther.loc[:, "PPG"] = individualDFOther["PPG"] + (individualDFOther["Rec"])
            elif ppr == 1:
                individualDFOther.loc[:, "PPG"] = individualDFOther["PPG"] + ((individualDFOther["Rec"])/2)

            individualDFOther.loc[:, "PPG"] = individualDFOther["PPG"]
                   
            #add other columns needed
            individualDFOther["Age"] = age

            #locate row with correct team and pos and add it
            rowOL = currAVs.loc[currAVs['team'] == team].iloc[0]
            individualDFOther['ol'] = rowOL['ol']
            
            rowRB = currAVs.loc[currAVs['team'] == team].iloc[0]
            individualDFOther['rb'] = rowRB['rb']

            rowQB = currAVs.loc[currAVs['team'] == team].iloc[0]
            individualDFOther['qb'] = rowQB['qb']

            rowWR = currAVs.loc[currAVs['team'] == team].iloc[0]
            individualDFOther['wr'] = rowWR['wr']

            rowTE = currAVs.loc[currAVs['team'] == team].iloc[0]
            individualDFOther['te'] = rowTE['te']
            
            completeDFOther = pd.concat([completeDFOther, individualDFOther], ignore_index=True, join="inner")                
                

    print(completeDFOther)
    print(completeDFQB)
    print(rookieList)
    
    #write into csv based on ppr
    if ppr == 0:
        completeDFOther.to_csv("player_scoring_things/all_rosters_stats_and_av_csvs/playersDFsForModels/rushRecDFForModelNonPPR.csv", encoding='utf-8', index=False)
        completeDFQB.to_csv("player_scoring_things/all_rosters_stats_and_av_csvs/playersDFsForModels/QBDFForModelNonPPR.csv", encoding='utf-8', index=False)
    elif ppr == 1:
        completeDFOther.to_csv("player_scoring_things/all_rosters_stats_and_av_csvs/playersDFsForModels/rushRecDFForModelHalfPPR.csv", encoding='utf-8', index=False)
        completeDFQB.to_csv("player_scoring_things/all_rosters_stats_and_av_csvs/playersDFsForModels/QBDFForModelHalfPPR.csv", encoding='utf-8', index=False)
    elif ppr == 2:
        completeDFOther.to_csv("player_scoring_things/all_rosters_stats_and_av_csvs/playersDFsForModels/rushRecDFForModelPPR.csv", encoding='utf-8', index=False)
        completeDFQB.to_csv("player_scoring_things/all_rosters_stats_and_av_csvs/playersDFsForModels/QBDFForModelPPR.csv", encoding='utf-8', index=False)
dfMaker()





    

