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

#REMEMBER ROOKIES
#rmbr to scale data and have exact columns in correct order among other cleaning for model

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

    #ppr variable. if 0 its non ppr, if 1 its half ppr, if 2 its full ppr
    ppr = 0

    #dict of scores
    dictScores = {}

    if ppr == 0:
        #read in player stats df
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
        #read in player stats df
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
        #read in player stats df
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


    modelsDict = {"QB": qbModel, "WR": wrModel, "RB": rbModel, "TE": teModel}

    #gets fantasypoints scale per each position
    scaleQB = getScaleBack(qbs)
    scaleRB = getScaleBack(rbs)
    scaleWR = getScaleBack(wrs)
    scaleTE = getScaleBack(tes)

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



    rb = {}

    allPosDFs = [rbs, wrs, tes, qbs]
    allPosDfsScaled = [rbsScaled, wrsScaled, tesScaled, qbsScaled]
    scaleBack = [scaleRB, scaleWR, scaleTE, scaleQB]

    #for ind in range(len(allPosDFs)):
    for ind in range(3):
        ind = 0
        currDF = allPosDFs[ind]
        scaled = allPosDfsScaled[ind]
        arr = scaleBack[ind]

        for i in range(len(currDF)):
            currRow = currDF.iloc[[i]]
            currRow = currRow.reset_index()
            scaled = scaled.reset_index()
            scaled = scaled.drop(columns=["index"])
            currRowForModel = scaled.iloc[[i]] 

            pos = currRow.loc[0, "Pos"]
            name = currRow.loc[0, "Name"]
            penalty = currRow.loc[0, "Penalty"]     

            model = modelsDict[pos]
            prediction = model.predict(currRowForModel)  

            #inverse transform the scaled predictions to get the original scale by reversing formula
            prediction = (prediction*(arr[1] - arr[0])) + arr[0]
            
            dictScores[name] = prediction[0]*penalty
    
        break

    '''
    for ind in range(len(other)):
        
        currRow = other.iloc[[ind]]
        currRow = currRow.reset_index()
        otherScaled = otherScaled.reset_index()
        otherScaled = otherScaled.drop(columns=["index"])        
        currRowForModel = otherScaled.iloc[[ind]] 

        pos = currRow.loc[0, "Pos"]
        name = currRow.loc[0, "Name"]
        penalty = currRow.loc[0, "Penalty"]

        model = modelsDict[pos]
        prediction = model.predict(currRowForModel)        

        if pos == "TE":
            rb[name] = prediction*penalty

        dictScores[name] = prediction[0]*penalty
        
    sorted_dict = dict(sorted(dictScores.items(), key=lambda item: item[1], reverse=True))
    sorted_dict = dict(sorted(rb.items(), key=lambda item: item[1], reverse=True))
    df = pd.DataFrame(list(sorted_dict.items()), columns=['Name', 'Score'])
    #df.to_csv("rankings.csv", encoding='utf-8', index=False)
    

    #print(df)
    
    teamDict = {}
    for ind in range(len(qbs)):
        currRow = qbs.iloc[[ind]]
        currRow = currRow.reset_index()
        qbsScaled = qbsScaled.reset_index()
        qbsScaled = qbsScaled.drop(columns=["index"])        
        currRowForModel = qbsScaled.iloc[[ind]] 

        pos = currRow.loc[0, "Pos"]
        name = currRow.loc[0, "Name"]
        penalty = currRow.loc[0, "Penalty"]
        team = currRow.loc[0, "Team"]

        model = modelsDict[pos]
        prediction = model.predict(currRowForModel)        

        if pos == "QB":
            rb[name] = prediction[0]*penalty      

        #teamDict[team]

        dictScores[name] = prediction[0]*penalty
    '''
    
        
    sorted_dict = dict(sorted(dictScores.items(), key=lambda item: item[1], reverse=True))
    #sorted_dict = dict(sorted(rb.items(), key=lambda item: item[1], reverse=True))
    df = pd.DataFrame(list(sorted_dict.items()), columns=['Name', 'Score'])
    df.to_csv("rankings.csv", encoding='utf-8', index=False)

    print(df)


scorer()