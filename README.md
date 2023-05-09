# Fantasy Football Positional Rankings with Machine Learning

### Description:
In this repository it ranks fantasy football players inside their position using neural networks (machine learning) based on previous year per-game stats, and grades for current teams positional groups (OLs, QBs, WRs, RBs, and TEs grades). Includes rankings for RBs, WRs, TEs, and QBs in Non PPR, Half PPR, and Full PPR. I used neural networks so the machine learning could account for the complexities of fantasy football. Code is adaptable to be able to be used for future years as well. Unfortunately, I am currently unable to incorporate rookies or one combined ranking of all positions, however it is something that I aim to add in the future. The languaged used throughout the project is Python.

<br/>

## How to use program
***BE PATIENT!* Running some of the code takes some time**
<br/>

### Requirements:
- install python
- install needed modules and libraries listed at top of each file that you do not already have downloaded.
- install lxml

### Things that need to be done once per year:
- run modelMaker.py to get each model used.
- run csvTeamRosterStatMaker.py's functions statMaker and rosterMaker with the last four years. ex: if it is July 2023, set years array to 2022, 2021, 2020, 2019. This is data used to rank players

### Things that need to be done to update rankings inside of each year:
- run csvTeamRosterStatMaker.py functions rosterMaker with only current year. ex: if July 2023, set years array to just 2023. This updates the teams roster.
- run teamPositionGrading.py and set x to false and scroll down a little bit and change yearsSmall in the if loop to last year and yearsBig to current year. ex: if it is July 2023, make yearsSmall 2022 and yearsBig 2023. This updates teams positional grade.
- run playerDFMaker.py. This makes player stats in manner necessary for models
- run playerScorer.py. This is where the actual rankings are predicted.

<br/>

## File Breakdown:

### Python files:
- **modelMaker.py:** This is where the nueral network machine learning models are made. It takes players per game stats from previous year and grades for current year team positional group and uses this to predict PPG, which is how the rankings are done. Does it for Non PPR, Half PPR, and Full PPR, and stores them in all_models folder using joblib.
- **csvTeamRosterStatMaker.py:** This is where the data is obtained from past four years for DF. It makes current year roster (currYearRoster.csv) for each team and then past four years rosters (teamsPastRoster.csv) to help indentify and confirm a players stats for each year. It also makes teamsOldQBStats.csv and teamsOldRushRec.csv, which is players stats for last four years.
- **playerDFMaker.py:** This file makes each individual players, who is currently on a team, dataframe row that has everything needed for the model. It takes the grades for their current team, and stats for last year. If they were hurt or suspended so they did not play at least 7 games, it goes to previous years until it can get enough, adding penalty for each year back so it is not fully counted. If they are a rookie, only needs a few games instead. Writes it into playersDFsForModels folder.
- **playerScorer.py:** This is where the rankings are made. It puts each player into the model and ranks them. It then sorts all players in each position in order from highest to lowest and writes rankings into final_rankings folder.
- **teamPositionGrading.py:** This is where the AV grades (simple grading system from sportsreference) are obtained. When X is false in program, it makes teamsAVGrades.csv (need to change yearsBig and yearsSmall in if statements later on, as listed in how to), when it is true it uses the main yearsBig and yearsSmall (last ten years, similar breakup as listed in how to for the current year) to make 12-21Grades.csv for machine learning model.

### CSV files:
- **csvs in final_rankings folder:** This is where all the rankings are compiled, sorted by if non ppr, half ppr, or ppr, and then by position.
- **12-21FantasyData.csv:** This is data obtained from kaggle that is used for the machine learning. If trying to make model more recent in the future, have to find dataset that has same things as model does.
- **12-21Grades.csv** This is teams position grades data obtained from teamPositionGrading.py of the same ten years as the data above. If trying to make model more recent in the future, need to rerun teamPositionGrading.py with years wanted.
- **csvs in playerDFsForModels folder:** These are csvs with the data of each person seperated by if QB or not, and PPR status. Used to predict ppg.
- **currYearRoster.csv:** Current year rosters for each team, iterates through this to make rankings. Uses player bday to confirm it finds same player in previous year.
- **teamsAVGrades.csv:** Current teams grades per positonal group to be used for each player in model.
- **teamsOldQBStats.csv:** QBs, that are on rosters, stats and grades that will be used in the model.
- **teamsOldRushRecStats.csv:** WRs, RBs, WRs, and TEs, that are on rosters, stats and grades that will be used in the model.
- **teamsPastRoster.csv:** Old rosters for teams. Used to match birthday and number of player to ensure the right stats are used, and not someone who happens to have the same name.


### Machine Learning Models:
- **dumped models as joblibs in all_models folder:** These are the nueral network machining learning models that are called on later for the predicting of players PPG. They have each position in non ppr, half ppr, and full ppr.

<br/>

## Other notes:
- Re-running modelMaker.py to get new models can create different rankings, although players will be in same general area, just with slight altercations. Sometimes, although it is very rare, there will be a bad batch of rankings with model, and if there is just re-run modelMaker.py again to get new models to be used for rankings (mostly just happens with QBs).
- If landscape of NFL dramatically changes in the distant future, may need to redo data for machine learning. To Re-do it you need to find a recent data set with at least 10 years of data that has all data needed in model, and also need to run teamPositionGrading.py to get the same 10 years as the data set. Overall, it may take a good bit of time and effort to do this, and is not likely to be necessary for quite some time
- If a RB/TE is in a committee the rankings may slightly over-value them, as it is difficult for model to incorporate this into predictions. Same with WRs if there are so many good ones on one team, albeit this is rarer.
- QB grades may include a couple non-starters highly ranked. This is because it is grading each player almost as if they were a starter.
- Future potential updates: include rookies, and make one combined ranking that includes all positions

<br/>

## Let me know if you have any questions ever, I am happy to answer any!