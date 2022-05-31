from re import A
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
from sklearn import preprocessing
import sys

# print('quartier : ', type(sys.argv[1]))
# print('nb SdB : ', type(sys.argv[2]))
# print('nb Chambres : ', type(sys.argv[3]))
# print('nb lits : ', sys.argv[4])
# print('type logement : ', sys.argv[5])
# print('type propriete : ', sys.argv[6])
# print('capacité accueil : ', sys.argv[7])
# print('parking sur place : ', sys.argv[8])
# print('caution : ', sys.argv[9])


df = pd.read_csv("../Data/final_dataset.csv")

del df['Identifiant']
del df['Latitude']
del df['Longitude']
del df['Titre']
del df['Resume']
del df['Type_logement']
del df['type_propriete']
del df['conditions_annulation']
del df['Description']
del df['reglement_interieur'] 

df.fillna('', inplace=True)

#modele machine learning
X = df[['Quartier','NombreSdB', 'NbChambres', 'NbLits','tokenized_Type_logement','tokenized_type_propriete', 'Capacite_accueil', 'parking_sur-place', 'Caution']]
y = df['PrixNuitee']

lbl = preprocessing.LabelEncoder()
X.loc[:,'tokenized_Type_logement'] = lbl.fit_transform(X.loc[:,'tokenized_Type_logement'].astype(str))
X.loc[:,'tokenized_type_propriete'] = lbl.fit_transform(X.loc[:,'tokenized_type_propriete'].astype(str))
X.loc[:,'Quartier'] = lbl.fit_transform(X.loc[:,'Quartier'].astype(str))

data_dmatrix = xgb.DMatrix(data=X,label=y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=105)

xg_reg = xgb.XGBRegressor(objective ='reg:squarederror', colsample_bytree = 0.33, learning_rate = 0.3, max_depth = 7, alpha = 5, n_estimators = 10)

xg_reg.fit(X_train,y_train)
preds = xg_reg.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, preds))

cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
# evaluate model
scores = cross_val_score(xg_reg, X, y, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1)
# force scores to be positive
scores = abs(scores)

#prediction
df_prediction = df[['Quartier','NombreSdB', 'NbChambres', 'NbLits','tokenized_Type_logement','tokenized_type_propriete', 'Capacite_accueil', 'parking_sur-place', 'Caution']][0:0]

df2 = { 'Quartier'                  : str(sys.argv[1]),
        'NombreSdB'                 : int(sys.argv[2]), 
        'NbChambres'                : int(sys.argv[3]), 
        'NbLits'                    : int(sys.argv[4]),
        'tokenized_Type_logement'   : str(sys.argv[5]),
        'tokenized_type_propriete'  : str(sys.argv[6]), 
        'Capacite_accueil'          : int(sys.argv[7]), 
        'parking_sur-place'         : int(sys.argv[8]), 
        'Caution'                   : int(sys.argv[9])
        }

df_prediction = df_prediction.append(df2, ignore_index = True)

lbl = preprocessing.LabelEncoder()
df_prediction.loc[:,'tokenized_Type_logement'] = lbl.fit_transform(df_prediction.loc[:,'tokenized_Type_logement'].astype(str))
df_prediction.loc[:,'tokenized_type_propriete'] = lbl.fit_transform(df_prediction.loc[:,'tokenized_type_propriete'].astype(str))
df_prediction.loc[:,'Quartier'] = lbl.fit_transform(df_prediction.loc[:,'Quartier'].astype(str))

prediction = xg_reg.predict(df_prediction)

print('\n\nprédiction de', prediction[0], '€\n\n')

predicted_csv = df2
predicted_csv['prediction'] = prediction[0]

#print(predicted_csv)

predicted_df = pd.DataFrame([predicted_csv])
predicted_df.to_csv("../Data/predicted.csv", mode='a', index=False, header=False) #header=True si fichier n'existe pas
