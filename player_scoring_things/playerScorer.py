#REMEMBER ROOKIES
#rmbr to scale data and have exact columns

#to do:
#take bday/name from all eligible players from current year. 
#find that bday in rosterav thing to find players teams/pos/number for that year, and confirm with name, or vice versa
#find that player in their team in stats for position and teamsAVGrade
#confirm with the pos obtained in that year and team and player number for that year and team (use first two letters of pos in case of WR/RB)
#make df with the stats and avgrade, and use CURRENT YEAR for age.

#other necessary notes:
#if players on two teams like odell or cmc, find both teams they were one and get data from both and make it to be one combined df. 
#^if switch teams may switch number or position, so confirm with the number or position specific to that team   
#make the df based on certain number of games over multiple years if not enough in last year.
#make sure all columns used in model are their in correct order for each position.
#remember rookies and to scale data or other necessary cleaning for model

'''
#make ppg column
rushRec.loc[:, "FantasyPPG"] = (rushRec["RushYds"]*0.1) + (rushRec["RecYds"]*0.1) + (rushRec["RushTD"]*6) + (rushRec["RecTD"]*6) + (rushRec["Fmb"]*-2)
if ppr == 2:
    rushRec.loc[:, "FantasyPPG"] = rushRec["FantasyPPG"] + (rushRec["Rec"])
elif ppr == 1:
    rushRec.loc[:, "FantasyPPG"] = rushRec["FantasyPPG"] + ((rushRec["Rec"])/2)

rushRec.loc[:, "FantasyPPG"] = rushRec["FantasyPPG"]/rushRec["G"]

#make ppg column
passing.loc[:, "FantasyPPG"] = (passing["RushYds"]*0.1) + (passing["Yds"]*.04) + (passing["RushTD"]*6) + (passing["TD"]*4) + (passing["Fmb"]*-2) + (passing["Int"]*-2)
passing.loc[:, "FantasyPPG"] = passing["FantasyPPG"]/passing["G"]
'''