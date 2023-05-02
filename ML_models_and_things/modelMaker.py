#imports necesary things
import pandas as pd
import numpy as np
import warnings
from sklearn.preprocessing import MinMaxScaler

pd.options.mode.chained_assignment = None


import sklearn
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error


from sklearn.model_selection import train_test_split
import joblib


#scaler to scale data
scaler = MinMaxScaler()

#read csv files into pandas
dfFantasy = pd.read_csv("ML_models_and_things/datasets_used_in_model/12-21FantasyData.csv")
dfGrades = pd.read_csv("ML_models_and_things/datasets_used_in_model/12-21Grades.csv")

def correctData(df, pos, pprTF):
  #cols to make per game
  cols = ['Tgt', 'Rec', 'PassingYds', 'PassingTD', 'PassingAtt', 'RushingYds', 'RushingTD', 'RushingAtt', 'ReceivingYds', 'ReceivingTD', 'Int', 'Fumbles', 'FumblesLost']

  #for some reason data for 20/21 was not ppr, so making it that.
  df.loc[df["Year"] == 2021, "FantasyPoints"] = df['FantasyPoints'] + df['Rec']  
  df.loc[df["Year"] == 2020, "FantasyPoints"] = df['FantasyPoints'] + df['Rec'] 



  #basing data if ppr or not
  if pprTF == 2:
    pass
  elif pprTF == 0:
    df.loc[:, "FantasyPoints"] = df["FantasyPoints"] - df['Rec']
  elif pprTF == 1:
    df.loc[:, "FantasyPoints"] = df["FantasyPoints"] - (df['Rec']/2)

    
  #adding ppg column
  df.loc[:, 'PPG'] = df['FantasyPoints'] / df['G']


  #make all columns in a per game basis
  for col in cols:
    df.loc[:, col] = df[col] / df['G'] 


  #only players with more than 7 games.
  df = df[df.G > 7]
  df = df[df.FantasyPoints >= 0]

  
  #get right amount amount of ppg per position to make df have right amount of players, with not only having amazing players but also not including the terrible
  if (pos=="RB"):
    df = df[df.PPG > 2]
  elif (pos=="WR"):
    if pprTF == 2:
      df = df[df.PPG > 2]
    elif pprTF == 0:
      df = df[df.PPG > 1]
    elif pprTF == 1:
      df = df[df.PPG > 1.5]
  elif (pos=="TE"):
    if pprTF == 2:
      df = df[df.PPG > 2]
    elif pprTF == 0:
      df = df[df.PPG > 1]
    elif pprTF == 1:
      df = df[df.PPG > 1.5]
  elif (pos=="QB"):
      df = df[df.PPG > 5]
  

  return df

#matches team abbreviation of both datasets so they can be called easily.
def getTeamAbbrMatching(df):
  #teams in one dataset and teams in other. need to match.
  newTeams = ["crd", "atl", "rav", "buf", "car", "chi", "cin", "cle", "dal", "den", "det", "gnb", "htx", "clt", "jax", "kan", "rai", "sdg", "ram", "mia", "min", "nwe", "nor", "nyg", "nyj", "phi", "pit", "sfo", "sea", "tam", "oti", "was"]
  oldTeams = ["ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE", "DAL", "DEN", "DET", "GNB", "HOU", "IND", "JAX", "KAN", "LVR", "LAC", "LAR", "MIA", "MIN", "NWE", "NOR", "NYG", "NYJ", "PHI", "PIT", "SFO", "SEA", "TAM", "TEN", "WAS"]
  
  #since some team names changed irl, the dataset has them changed as well. So need to account for those too.
  normal = ["ram", "rai", "sdg"]
  repeats = ["STL", "OAK", "SDG"]

  #loops over both arrays since are same length
  for new, old in zip(newTeams, oldTeams):  
      df.loc[df['Tm'] == old, 'Tm'] = new

  #loops over repeated team arrays next
  for new2, old2 in zip(normal, repeats):  
     df.loc[df['Tm'] == old2, 'Tm'] = new2

  return df

def putAV(df, dfAV):
  #years to iterate through
  yearsBig = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
  teams = ["crd", "atl", "rav", "buf", "car", "chi", "cin", "cle", "dal", "den", "det", "gnb", "htx", "clt", "jax", "kan", "rai", "sdg", "ram", "mia", "min", "nwe", "nor", "nyg", "nyj", "phi", "pit", "sfo", "sea", "tam", "oti", "was"]

  #columns wanted to add
  columns = ["ol", "rb", "wr", "qb", "te"]
  df[columns] = np.nan

  #gets rid of nan for these columns, as when we drop nan we want to save these.
  for colNow in columns:
    df.loc[df["Year"] == 2011, colNow] = "no"



  #iterates through years
  for year in yearsBig:

    #assigns df of AVS to only include current year
    dfCurr = dfAV[dfAV.year == year].copy()
    
    #iterates through team list
    for teamNow in teams:
      #makes the df
      dfCurrNew = dfCurr[dfCurr.team == teamNow]
      
      #iterates through columns and adds AV
      for colNow in columns:
        #locate correct year and team rows
        condition = (df["Year"] == year) & (df["Tm"] == teamNow)

        #set these rows to correct values
        df.loc[condition, colNow] = dfCurrNew.iloc[0][colNow]

  df = df.dropna()

  return df

#removes unneccesary stats
def removeUnwanted(dfPos, pos):
  dfPos = dfPos.drop(columns=["G", "GS", "FantasyPoints", "Player", "Year", "FumblesLost", "Tm", "Pos"])
  if pos == "QB":
    dfPos = dfPos.drop(columns=["ReceivingYds", "ReceivingTD", "Tgt", "Rec"])
  else:
    dfPos = dfPos.drop(columns=["PassingYds", "PassingTD", "PassingAtt", "Int"])

  return dfPos

#shifts data forward one year
def makeCorrectShift(df):
  shifters = ['Age', 'G', 'GS', 'Tgt', 'Rec', 'PassingYds', 'PPG', 'PassingTD', 'PassingAtt', 'RushingYds', 'RushingTD', 'RushingAtt', 'ReceivingYds', 'ReceivingTD', 'FantasyPoints', 'Int', 'Fumbles', 'FumblesLost']
  
  #adds target variable
  df["targetPPG"] = df["PPG"]
  
  #shifts it forward a year (for example 2011 goes to 2012)
  df[shifters] = df.groupby('Player')[shifters].shift(1)
  df = df.dropna()

  return df

#where machine learning is done. returns the model and score.
def machineLearning(df, arr, dictParam):

  #make columns everything but target
  predictors = [col for col in df.columns if col != "targetPPG"]


  #make train and test sets
  x = df[predictors].values
  y = df["targetPPG"].values
  x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=40)

  #make the model based on parameters from function below
  mlp = MLPRegressor(hidden_layer_sizes=dictParam["hidden_layer_sizes"], activation=dictParam["activation"], solver=dictParam["solver"], max_iter=dictParam["max_iter"])

  #print(dictParam)

  #fit it with the data
  mlp.fit(x_train,y_train)

  #make the predictions
  predict_test = mlp.predict(x_test)

  #inverse transform the scaled predictions to get the original scale by reversing formula
  for i in range(len(predict_test)):
    predict_test[i] = (predict_test[i]*(arr[1] - arr[0])) + arr[0]
  for i in range(len(y_test)):
    y_test[i] = (y_test[i]*(arr[1] - arr[0])) + arr[0]
  

  #average error 
  mae = mean_absolute_error(y_test, predict_test)
  #print("test ", mae)

  arr2 = [mae, mlp]
  return arr2

def getBestParams(df, arr):

  #make the predictors and data and test sets correctly
  predictors = [col for col in df.columns if col != "targetPPG"]
  x = df[predictors].values
  y = df["targetPPG"].values
  x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=40)

  
  #make the parameters to search over. for hidden_layer_sizes, I experimented with alot and the ones listed now is just final set of experiment.
  
  grid = {
      'hidden_layer_sizes': [(32,32), (64,32), (64), (64,64)],
      'activation': ['tanh', 'identity', 'logistic', 'relu'],
      'solver': ['adam', 'sgd', 'lbfgs'],
      'max_iter': [100, 200, 500]
  }

  #create an MLPRegressor object
  mlp = MLPRegressor()

  #create a GridSearchCV object and fit it to the training data
  grid_search = GridSearchCV(mlp, param_grid=grid, cv=5, n_jobs=-1)
  grid_search.fit(x_train, y_train)

  print("Best things:", grid_search.best_params_)

  #the best model to make predictions on the test data and evaluate performance
  y_pred = grid_search.predict(x_test)

  #inverse transform the scaled predictions to get the original scale, uses a reverse of original formula
  for i in range(len(y_pred)):
    y_pred[i] = (y_pred[i]*(arr[1] - arr[0])) + arr[0]
  for i in range(len(y_test)):
    y_test[i] = (y_test[i]*(arr[1] - arr[0])) + arr[0]


  print(mean_absolute_error(y_test, y_pred))

  return grid_search.best_params_

#gets original value for fantasy points for predictions.
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

def test(df, model, arr):
  #make columns everything but target
  predictors = [col for col in df.columns if col != "targetPPG"]


  #make train and test sets
  x = df[predictors].values
  y = df["targetPPG"].values
  x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=40)

  #make the predictions
  predict_test = model.predict(x_test)

  #inverse transform the scaled predictions to get the original scale by reversing formula
  for i in range(len(predict_test)):
    predict_test[i] = (predict_test[i]*(arr[1] - arr[0])) + arr[0]
  for i in range(len(y_test)):
    y_test[i] = (y_test[i]*(arr[1] - arr[0])) + arr[0]

  #average error 
  mae = mean_absolute_error(y_test, predict_test)
  print("test ", mae)

#if ppr is 0, than it is non ppr. if 1, then it is half ppr. if 2, full ppr. loops through each.
for ppr in range(3):
  dfFantasy = dfFantasy.dropna()

  #removes 2 team players as it will not work well with datasets
  dfFantasy = dfFantasy[dfFantasy.Tm != "2TM"] 
  dfFantasy = dfFantasy[dfFantasy.Tm != "3TM"]
  dfFantasy = dfFantasy[dfFantasy.Tm != "4TM"]

  #make team abbreviations correct
  dfFantasy = getTeamAbbrMatching(dfFantasy)

  #makes dataframes only their position
  dfFantasyRB = dfFantasy[dfFantasy.Pos == "RB"]
  dfFantasyWR = dfFantasy[dfFantasy.Pos == "WR"]
  dfFantasyQB = dfFantasy[dfFantasy.Pos == "QB"]
  dfFantasyTE = dfFantasy[dfFantasy.Pos == "TE"]

  #makes the data correct as shown by method CorrectData (enough games played, ppr or not, etc)
  dfFantasyRB = correctData(dfFantasyRB, "RB", ppr)
  dfFantasyWR = correctData(dfFantasyWR, "WR", ppr)
  dfFantasyQB = correctData(dfFantasyQB, "QB", ppr)
  dfFantasyTE = correctData(dfFantasyTE, "TE", ppr)

  #add on avs
  dfFantasyWR = putAV(dfFantasyWR, dfGrades)
  dfFantasyRB = putAV(dfFantasyRB, dfGrades)
  dfFantasyTE = putAV(dfFantasyTE, dfGrades)
  dfFantasyQB = putAV(dfFantasyQB, dfGrades)

  #shift the years so its predicting correctly
  dfFantasyWR = makeCorrectShift(dfFantasyWR)
  dfFantasyRB = makeCorrectShift(dfFantasyRB)
  dfFantasyTE = makeCorrectShift(dfFantasyTE)
  dfFantasyQB = makeCorrectShift(dfFantasyQB)

  #removes any rows with the year 2011
  dfFantasyWR = dfFantasyWR.loc[dfFantasyWR["Year"] != 2011]
  dfFantasyTE = dfFantasyTE.loc[dfFantasyTE["Year"] != 2011]
  dfFantasyRB = dfFantasyRB.loc[dfFantasyRB["Year"] != 2011]
  dfFantasyQB = dfFantasyQB.loc[dfFantasyQB["Year"] != 2011]

  #get right columns
  dfFantasyWR = removeUnwanted(dfFantasyWR, "WR")
  dfFantasyRB = removeUnwanted(dfFantasyRB, "RB")
  dfFantasyTE = removeUnwanted(dfFantasyTE, "TE")
  dfFantasyQB = removeUnwanted(dfFantasyQB, "QB")

  #resets index of dataframes
  dfFantasyWR = dfFantasyWR.reset_index(drop=True)
  dfFantasyRB = dfFantasyRB.reset_index(drop=True)
  dfFantasyTE = dfFantasyTE.reset_index(drop=True)
  dfFantasyQB = dfFantasyQB.reset_index(drop=True)

  #gets fantasypoints scale per each position
  scaleQB = getScaleBack(dfFantasyQB)
  scaleRB = getScaleBack(dfFantasyRB)
  scaleWR = getScaleBack(dfFantasyWR)
  scaleTE = getScaleBack(dfFantasyTE)

  #scale data to 1
  dfFantasyWR[dfFantasyWR.columns] = scaler.fit_transform(dfFantasyWR[dfFantasyWR.columns])
  dfFantasyTE[dfFantasyTE.columns] = scaler.fit_transform(dfFantasyTE[dfFantasyTE.columns])
  dfFantasyQB[dfFantasyQB.columns] = scaler.fit_transform(dfFantasyQB[dfFantasyQB.columns])
  dfFantasyRB[dfFantasyRB.columns] = scaler.fit_transform(dfFantasyRB[dfFantasyRB.columns])

  #obtained by running the getBestParams function per each respective position
  paramRB = {'activation': 'logistic', 'hidden_layer_sizes': (64, 32), 'max_iter': 200, 'solver': 'lbfgs'}
  #paramRB = getBestParams(dfFantasyRB, scaleRB)

  #obtained by running the getBestParams function per each respective position
  paramWR = {'activation': 'logistic', 'hidden_layer_sizes': (64, 32), 'max_iter': 500, 'solver': 'lbfgs'}
  #paramWR = getBestParams(dfFantasyWR, scaleWR)

  #obtained by running the getBestParams function per each respective position
  paramTE = {'activation': 'tanh', 'hidden_layer_sizes': (64, 64), 'max_iter': 200, 'solver': 'adam'}
  #paramTE = getBestParams(dfFantasyTE, scaleTE)

  #obtained by running the getBestParams function per each respective position
  paramQB = {'activation': 'tanh', 'hidden_layer_sizes': (64, 64), 'max_iter': 200, 'solver': 'adam'}
  #paramQB = getBestParams(dfFantasyQB, scaleQB)

  #makes array of model and score, then prints it
  rbArray = machineLearning(dfFantasyRB, scaleRB, paramRB)
  num = rbArray[0]
  rbModel = rbArray[1]
  
  print(ppr)
  print("rb score(ppg off on average per player): ", num)

  #makes array of model and score, then prints it
  wrArray = machineLearning(dfFantasyWR, scaleWR, paramWR)
  num = wrArray[0]
  wrModel = wrArray[1]

  print("wr score(ppg off on average per player): ", num)

  #makes array of model and score, then prints it
  teArray = machineLearning(dfFantasyTE, scaleTE, paramTE)
  num = teArray[0]
  teModel = teArray[1]

  print("te score(ppg off on average per player): ", num)

  #makes array of model and score, then prints it
  qbArray = machineLearning(dfFantasyQB, scaleQB, paramQB)
  num = qbArray[0]
  qbModel = qbArray[1]
    
  print("qb score(ppg off on average per player): ", num)
  print("")
  if ppr == 0:
    joblib.dump(rbModel, "ML_models_and_things/all_models/NonPPR_models/rbModelNonPPR.joblib")
    joblib.dump(wrModel, "ML_models_and_things/all_models/NonPPR_models/wrModelNonPPR.joblib")
    joblib.dump(qbModel, "ML_models_and_things/all_models/NonPPR_models/qbModelNonPPR.joblib")
    joblib.dump(teModel, "ML_models_and_things/all_models/NonPPR_models/teModelNonPPR.joblib")
  #dumps each model into a file to be used later.
  elif ppr == 1:
    joblib.dump(rbModel, "ML_models_and_things/all_models/HalfPPR_models/rbModelHalfPPR.joblib")
    joblib.dump(wrModel, "ML_models_and_things/all_models/HalfPPR_models/wrModelHalfPPR.joblib")
    joblib.dump(qbModel, "ML_models_and_things/all_models/HalfPPR_models/qbModelHalfPPR.joblib")
    joblib.dump(teModel, "ML_models_and_things/all_models/HalfPPR_models/teModelHalfPPR.joblib")
  elif ppr == 2:
    joblib.dump(rbModel, "ML_models_and_things/all_models/PPR_models/rbModelPPR.joblib")
    joblib.dump(wrModel, "ML_models_and_things/all_models/PPR_models/wrModelPPR.joblib")
    joblib.dump(qbModel, "ML_models_and_things/all_models/PPR_models/qbModelPPR.joblib")
    joblib.dump(teModel, "ML_models_and_things/all_models/PPR_models/teModelPPR.joblib")

#print(dfFantasyQB.columns)
#print(dfFantasyRB.columns)

