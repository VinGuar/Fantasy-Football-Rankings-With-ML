# FantasyFootball

say how main 10 year csv of team grades was obtained by 3 smaller ones. also say how that is done to prevent rate limiting or other errors on large scraping, however doing it as one main scrape at once could have also worked. explain how this process works for future years testing, and how for me I did 3 seperate scrapes with splitting the 10 years up into first 3, next 3, and last 4, and then combined them all to get csv shown in repo

things need to do if for new year:
change year for how teams grade was made.
change years for how the last four years in csvGradingMaker was made
potentially change machine learning years if wanted. (optional)

must change if ppr, half ppr, or non ppr in modelMaker, playerDFMaker, playerScorer


**BE PATIENT
***explain how to run, and whether run each year or just before making. 
ex: yearly: need to run models in each ppr, get models Old/past/final in in all_rosters_stats thing from csvteamrosterstatmaker

**BE PATIENT
before making list: make curryearroster from csvteamrosterstatmaker, make teamsavgrades from teampositiongrading, make playerstatsmatchedcsv from playerdfmaker, run playerscorer to grade players and make csv of final rankings. then run main.

tell them how co starters like knight and hall or allegier and rookie rb may overvalue botj

tell them how complete rankings maker with varying multiplicators for each pos score may need to be varied every couple years as the league evolves.

tell them may need to run models again if its looking bad, sometimes a rly bad batch happens. unlikely, however happens more with qbs. still unlikely tho, so just re-run models and such.

tell them how it may vary a tiny bit with new models. players will stay in same area, just a few small alterations up or down for players each time.

tell them how i couldnt do rookies


# Hey! To run everything to get data, there are some steps you need to do. Refer to README for specifics.

# Some things you need to run yearly to get new data, and others you run each time before you run rankings.

# Yearly:
# 1. 



