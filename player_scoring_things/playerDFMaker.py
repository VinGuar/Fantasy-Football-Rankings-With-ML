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

    for index in range(len(currTeamsRoster)):
       
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

        while True:
            x = 1
            playerRow = pastTeamsRoster.loc[(pastTeamsRoster['Player'] == name) & (pastTeamsRoster["YearsBack"] == x) & (pastTeamsRoster["BirthDate"] == bday)].copy()
            print(playerRow)
            x+=1
            break


        break

dfMaker()





    

