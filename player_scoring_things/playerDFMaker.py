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
    qbStats = pd.read_csv("teamsOldQBStats.csv")
    rushRecStats = pd.read_csv("teamsOldRushRecStats.csv")
    currTeams = pd.read_csv("currYearRoster")
    pastTeams = pd.read_csv("teamsPastRoster")
    currAVs = pd.read_csv("teamsAVGrades")

    

