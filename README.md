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
- You need to run modelMaker.py to get each model used.
- You need to run csvTeamRosterStatMaker.py's functions statMaker and rosterMaker with the last four years. ex: if it is July 2023, use array with 2022, 2021, 2020, 2019.
- 

### Things that need to be done to update rankings inside of each year:

### Things that need to be done to update model on more recent years (If far enough in future that the NFL fundamentally changes.)