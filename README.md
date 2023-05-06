# Fantasy Football Positional Rankings with Machine Learning

### Short description:
In this repository it ranks fantasy football players inside their position using neural networks (machine learning) based on previous year per-game stats, and grades for current teams positional groups (like Oline grade, QB grade, etc). Includes rankings for RBs, WRs, TEs, and QBs. I used neural networks so the machine learning could account for the complexities of fantasy football. Code is adaptable to be able to be used for future years as well. Unfortunately, I am currently unable to incorporate rookies or one combined ranking of all positions, however it is something that I aim to add in the future.


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

## File Breakdown:


## Other notes:
- If landscape of NFL dramatically changes in the distant future, may need to redo data for machine learning. To Re-do it you need to find a recent data set with at least 10 years of data that has all data needed in model, and also need to run teamPositionGrading.py to get the same 10 years as the data set. Overall, it may take a good bit of time and effort to do this.
- If a RB/TE is in a committee the rankings may slightly over-value them, as it is difficult for model to incorporate this into predictions. Same with WRs if there are so many good ones on one team, albeit this is rarer.
- QB grades may include a couple non-starters highly ranked. This is because it is grading each player almost as if they were a starter.
- Future potential updates: include rookies, and make one combined ranking that includes all positions
