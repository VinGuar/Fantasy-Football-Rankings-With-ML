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
    if r > 16:
        rate = 0
        time.sleep(61)

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

def rosterMaker():

    #empty df to add things to
    df = pd.DataFrame(columns= ["No.", "Player", "Age", "Pos", "G", "GS", "Wt", "Ht", "College/Univ", "BirthDate", "Yrs", "AV", "Drafted (tm/rnd/yr)", "Year"])


    global rate

    #years used for grading. changes each season. if making currYearRoster, make this just current year
    years = ["2019", "2020", "2021", "2022"]

    #team abbr list
    teams = ["crd", "atl", "rav", "buf", "car", "chi", "cin", "cle", "dal", "den", "det", "gnb", "htx", "clt", "jax", "kan", "rai", "sdg", "ram", "mia", "min", "nwe", "nor", "nyg", "nyj", "phi", "pit", "sfo", "sea", "tam", "oti", "was"]


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
            table = makeCommentTable(soup)
            table['Year'] = num
            #append table for current team in loop to all teams

            #make all into one df
            df = pd.concat([df, table], ignore_index=True, join="inner")


    #write dfs into csv files for later use
    if len(years)==1:
        df.to_csv("player_scoring_things/all_rosters_stats_and_av_csvs/currYearRoster.csv", encoding='utf-8', index=False)
    else:
        df.to_csv("player_scoring_things/all_rosters_stats_and_av_csvs/teamsPastRoster.csv", encoding='utf-8', index=False)

def statMaker():

    #make it so have one csv file for passing and one for rushing/recieving
    #also remeber may have to deal with commented out tables
