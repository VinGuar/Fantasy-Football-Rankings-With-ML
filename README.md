# Fantasy Football Positional Rankings with Machine Learning

### Short description:
In this repository it ranks fantasy football players inside their position using neural networks (machine learning) based on previous year per-game stats, and grades for current teams positional groups (like Oline grade, QB grade, etc). Includes rankings for RBs, WRs, TEs, and QBs. I used neural networks so the machine learning could account for the complexities of fantasy football. Code is adaptable to be able to be used for future years as well. Unfortunately, I am currently unable to incorporate rookies or a combined ranking of all positions, something I aim to add in the future.

## How to use code
*BE PATIENT!* Running some of the code takes some time
<br/>

### Requirements:
- install python
- install needed modules and libraries listed at top of each file that you do not already have downloaded.
- install lxml
<br/>

### Things that need to be done once per year:
- run modelMaker.py to get each model used.
- run csvTeamRosterStatMaker.py's functions statMaker and rosterMaker with the last four years. ex: if it is July 2023, use array with 2022, 2021, 2020, 2019. This is data used to rank players

<br/>

### Things that need to be done to update rankings inside of each year:
- run csvTeamRosterStatMaker.py functions rosterMaker with only current year. ex: if July 2023, use 2023. This updates the teams roster.
- run teamPositionGrading.py and set x to false and scroll down a little bit and change yearsSmall in the if loop to last year and yearsBig to current year. ex: if it is July 2023, make yearsSmall 2022 and yearsBig 2023. This updates teams positional grade.
- run playerDFMaker.py. This makes player stats in manner necessary for models
- run playerScorer.py. This is where the actual rankings are predicted.

<br/>

