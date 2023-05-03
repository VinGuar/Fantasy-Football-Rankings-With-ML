import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
import time
from unidecode import unidecode
import numpy as np
from itertools import chain
import joblib
from sklearn.preprocessing import MinMaxScaler
import sklearn
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error
import warnings
warnings.filterwarnings("ignore", message="X has feature names, but MLPRegressor was fitted without feature names")

#gets ppg back into normal form
def getScaleBack(df):
  #index of column
  column_index = df.columns.get_loc("PPG")

  #min value of column:
  min_value = df["PPG"].min()

  #scaling valye of column
  #scaling_factor = scaler.scale_[column_index]
  max_value = df["PPG"].max()

  #array to be used later to scale each data
  arr = [min_value, max_value]

  return arr

def scorer():

    #scaler to scale data
    scaler = MinMaxScaler()

    #if 0 its non ppr, if 1 its half ppr, if 2 its full ppr. loops through.

    for ppr in range(3):
        #dict of scores
        dictScores = {}

        if ppr == 0:
            #read in player stats df and make positional dfs
            qbs = pd.read_csv("player_scoring_things/all_rosters_stats_and_av_csvs/playersDFsForModels/QBDFForModelNonPPR.csv")
            other = pd.read_csv("player_scoring_things/all_rosters_stats_and_av_csvs/playersDFsForModels/rushRecDFForModelNonPPR.csv")
            rbs = other.loc[other['Pos'] == "RB"].copy()
            wrs = other.loc[other['Pos'] == "WR"].copy()
            tes = other.loc[other['Pos'] == "TE"].copy()

            #loads models
            rbModel = joblib.load("ML_models_and_things/all_models/NonPPR_models/rbModelNonPPR.joblib")
            wrModel = joblib.load("ML_models_and_things/all_models/NonPPR_models/wrModelNonPPR.joblib")
            qbModel = joblib.load("ML_models_and_things/all_models/NonPPR_models/qbModelNonPPR.joblib")
            teModel = joblib.load("ML_models_and_things/all_models/NonPPR_models/teModelNonPPR.joblib")
        elif ppr == 1:
            #read in player stats df and make positional dfs
            qbs = pd.read_csv("player_scoring_things/all_rosters_stats_and_av_csvs/playersDFsForModels/QBDFForModelHalfPPR.csv")
            other = pd.read_csv("player_scoring_things/all_rosters_stats_and_av_csvs/playersDFsForModels/rushRecDFForModelHalfPPR.csv")
            rbs = other.loc[other['Pos'] == "RB"].copy()
            wrs = other.loc[other['Pos'] == "WR"].copy()
            tes = other.loc[other['Pos'] == "TE"].copy()

            #loads models
            rbModel = joblib.load("ML_models_and_things/all_models/HalfPPR_models/rbModelHalfPPR.joblib")
            wrModel = joblib.load("ML_models_and_things/all_models/HalfPPR_models/wrModelHalfPPR.joblib")
            qbModel = joblib.load("ML_models_and_things/all_models/HalfPPR_models/qbModelHalfPPR.joblib")
            teModel = joblib.load("ML_models_and_things/all_models/HalfPPR_models/teModelHalfPPR.joblib")
        elif ppr == 2:        
            #read in player stats df and make positional dfs
            qbs = pd.read_csv("player_scoring_things/all_rosters_stats_and_av_csvs/playersDFsForModels/QBDFForModelPPR.csv")
            other = pd.read_csv("player_scoring_things/all_rosters_stats_and_av_csvs/playersDFsForModels/rushRecDFForModelPPR.csv")
            rbs = other.loc[other['Pos'] == "RB"].copy()
            wrs = other.loc[other['Pos'] == "WR"].copy()
            tes = other.loc[other['Pos'] == "TE"].copy()

            #loads models
            rbModel = joblib.load("ML_models_and_things/all_models/PPR_models/rbModelPPR.joblib")
            wrModel = joblib.load("ML_models_and_things/all_models/PPR_models/wrModelPPR.joblib")
            qbModel = joblib.load("ML_models_and_things/all_models/PPR_models/qbModelPPR.joblib")
            teModel = joblib.load("ML_models_and_things/all_models/PPR_models/teModelPPR.joblib")

        #dictionary to easily call models
        modelsDict = {"QB": qbModel, "WR": wrModel, "RB": rbModel, "TE": teModel}

        #gets fantasypoints scale per each position
        scaleQB = getScaleBack(qbs)
        scaleRB = getScaleBack(rbs)
        scaleWR = getScaleBack(wrs)
        scaleTE = getScaleBack(tes)

        #create a scaled version of each positional df, and have it be same parameters as models
        rbsScaled = rbs.copy()
        rbsScaled = rbsScaled.drop(columns=["Games", "Pos", "Penalty", "Name", "Team"])        
        rbsScaled[rbsScaled.columns] = scaler.fit_transform(rbsScaled[rbsScaled.columns])

        wrsScaled = wrs.copy()
        wrsScaled = wrsScaled.drop(columns=["Games", "Pos", "Penalty", "Name", "Team"])        
        wrsScaled[wrsScaled.columns] = scaler.fit_transform(wrsScaled[wrsScaled.columns])

        tesScaled = tes.copy()
        tesScaled = tesScaled.drop(columns=["Games", "Pos", "Penalty", "Name", "Team"])        
        tesScaled[tesScaled.columns] = scaler.fit_transform(tesScaled[tesScaled.columns])
        
        qbsScaled = qbs.copy()
        qbsScaled = qbsScaled.drop(columns=["Games", "Pos", "Penalty", "Name", "Team"])        
        qbsScaled[qbsScaled.columns] = scaler.fit_transform(qbsScaled[qbsScaled.columns])

        #have these so it can iterate through easily
        allPosDFs = [rbs, wrs, tes, qbs]
        allPosDfsScaled = [rbsScaled, wrsScaled, tesScaled, qbsScaled]
        scaleBack = [scaleRB, scaleWR, scaleTE, scaleQB]

        currPosDict = {}
        indPosArr = []

        #iterates through each position
        for ind in range(len(allPosDFs)):
            #gets current position df, scaled current df, and array to help get ppg to normal.
            currDF = allPosDFs[ind]
            scaled = allPosDfsScaled[ind]
            arr = scaleBack[ind]

            #dictionary to store current position grades.
            currPosDict = {}
        
            #iterates through all players in current position.
            for i in range(len(currDF)):

                #gets current information for current player
                currRow = currDF.iloc[[i]]
                currRow = currRow.reset_index()
                scaled = scaled.reset_index()
                scaled = scaled.drop(columns=["index"])
                currRowForModel = scaled.iloc[[i]] 

                pos = currRow.loc[0, "Pos"]
                name = currRow.loc[0, "Name"]
                penalty = currRow.loc[0, "Penalty"]     

                #gets in correct positinal model and predicts each player
                model = modelsDict[pos]
                prediction = model.predict(currRowForModel)  

                #inverse transform the scaled predictions to get the original scale by reversing formula
                prediction = (prediction*(arr[1] - arr[0])) + arr[0]

                #this is where the penalty is added and prediction is entered into the dictionary
                currPosDict[name] = prediction[0]*penalty   

            #appends current position grades to all of them.
            indPosArr.append(currPosDict)

            
    
        #sorts dictionary
        finalrbs = indPosArr[0]
        finalwrs = indPosArr[1]
        finaltes = indPosArr[2]
        finalqbs = indPosArr[3]

        #sorts data
        finalrbs = dict(sorted(finalrbs.items(), key=lambda item: item[1], reverse=True))
        finalwrs = dict(sorted(finalwrs.items(), key=lambda item: item[1], reverse=True))
        finaltes = dict(sorted(finaltes.items(), key=lambda item: item[1], reverse=True))
        finalqbs = dict(sorted(finalqbs.items(), key=lambda item: item[1], reverse=True))

        #makes data into list and add Rank/Name column for each position
        n = len(finalrbs)
        rankNums = np.arange(1, n+1)
        finalrbs = list(finalrbs.keys())
        finalrbs = pd.DataFrame(finalrbs, columns=['Name'])
        finalrbs.insert(0, "Rank", rankNums, True)

        n = len(finalwrs)
        rankNums = np.arange(1, n+1)
        finalwrs = list(finalwrs.keys())
        finalwrs = pd.DataFrame(finalwrs, columns=['Name'])
        finalwrs.insert(0, "Rank", rankNums, True)

        n = len(finaltes)
        rankNums = np.arange(1, n+1)
        finaltes = list(finaltes.keys())
        finaltes = pd.DataFrame(finaltes, columns=['Name'])
        finaltes.insert(0, "Rank", rankNums, True)

        n = len(finalqbs)
        rankNums = np.arange(1, n+1)
        finalqbs = list(finalqbs.keys())
        finalqbs = pd.DataFrame(finalqbs, columns=['Name'])
        finalqbs.insert(0, "Rank", rankNums, True)


        #writes into csv files
        if ppr == 0:
            finalrbs.to_csv("final_rankings/NonPPR_rankings/RBs_NonPPR.csv", encoding='utf-8', index=False)
            finalwrs.to_csv("final_rankings/NonPPR_rankings/WRs_NonPPR.csv", encoding='utf-8', index=False)
            finaltes.to_csv("final_rankings/NonPPR_rankings/TEs_NonPPR.csv", encoding='utf-8', index=False)
            finalqbs.to_csv("final_rankings/NonPPR_rankings/QBs_NonPPR.csv", encoding='utf-8', index=False)
        elif ppr == 1:
            finalrbs.to_csv("final_rankings/HalfPPR_rankings/RBs_HalfPPR.csv", encoding='utf-8', index=False)
            finalwrs.to_csv("final_rankings/HalfPPR_rankings/WRs_HalfPPR.csv", encoding='utf-8', index=False)
            finaltes.to_csv("final_rankings/HalfPPR_rankings/TEs_HalfPPR.csv", encoding='utf-8', index=False)
            finalqbs.to_csv("final_rankings/HalfPPR_rankings/QBs_HalfPPR.csv", encoding='utf-8', index=False)
        elif ppr == 2:
            finalrbs.to_csv("final_rankings/PPR_rankings/RBs_PPR.csv", encoding='utf-8', index=False)
            finalwrs.to_csv("final_rankings/PPR_rankings/WRs_PPR.csv", encoding='utf-8', index=False)
            finaltes.to_csv("final_rankings/PPR_rankings/TEs_PPR.csv", encoding='utf-8', index=False)
            finalqbs.to_csv("final_rankings/PPR_rankings/QBs_PPR.csv", encoding='utf-8', index=False)


    #print(df)


scorer()