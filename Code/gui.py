
import tkinter as tk
import os
import sys
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

def change_text():
    prediction()
    


window=tk.Tk()
window.resizable(False, False)
window.title('airbnb - Prediction nuitée')
window.iconbitmap("airbnb.ico")
window.iconphoto(True, tk.PhotoImage(file='airbnb.ico'))
img = tk.Image("photo", file="airbnb.ico")
# root.iconphoto(True, img) # you may also want to try this.
window.tk.call('wm','iconphoto', window._w, img)

tk.Label(text="Prédiction du prix d'une nuitée\nairbnb selon les critères définis", font='Helvetica 16 bold').grid(row=0, columnspan=5, column=0, pady=10)
tk.Label(text="").grid(row=1)

QuartierList = [
    'Autre',
    'Centre ville', 
    'Chartrons - Grand Parc - Jardin Public', 
    'Saint Augustin - Tauzin - Alphonse Dupeux', 
    'Bordeaux Sud', 
    'Nansouty - Saint Genès', 
    'La Bastide', 
    'Bordeaux Maritime', 
    'Caudéran'
] 
varQuartier = tk.StringVar(window)
varQuartier.set(QuartierList[0])

TypeLogementList = [
    'Autre',
    'Chambre privée', 
    'Logement entier', 
    'Chambre partagée'
]
varTypeLogement = tk.StringVar(window)
varTypeLogement.set(TypeLogementList[0])

ParkingList = [
    'Non', 
    'Oui'
]
varParking = tk.StringVar(window)
varParking.set(ParkingList[0])

TypeProprieteList = [
    'Autre',
    'Maison', 
    'Appartement', 
    'Bed & Breakfast', 
    'Maison de ville',
    'Loft', 
    'Cabane',
    'Appartement en résidence',
    'Bungalow',
    'Inconnue', 
    'Maison écologique', 
    'Villa', 
    'Dortoir'
]
varTypePropriete = tk.StringVar(window)
varTypePropriete.set(TypeProprieteList[0])

tk.Label(window, text="Quartier").grid(row=2)
tk.Label(window, text="Nb Salles de Bain").grid(row=3)
tk.Label(window, text="Nb Chambres").grid(row=4)
tk.Label(window, text="Nb Lits").grid(row=5)
tk.Label(window, text="Type Logement").grid(row=6)
tk.Label(window, text="Type Propriété").grid(row=7)
tk.Label(window, text="Capacité d'accueil").grid(row=8)
tk.Label(window, text="Parking sur place").grid(row=9)
tk.Label(window, text="Caution (€)").grid(row=10)

e1 = tk.OptionMenu(window, varQuartier, *QuartierList)
e1.config(width=30)

e2 = tk.Entry(window)
e2.config(width=34)

e3 = tk.Entry(window)
e3.config(width=34)

e4 = tk.Entry(window)
e4.config(width=34)

e5 = tk.OptionMenu(window, varTypeLogement, *TypeLogementList)
e5.config(width=30)

e6 = tk.OptionMenu(window, varTypePropriete, *TypeProprieteList)
e6.config(width=30)

e7 = tk.Entry(window)
e7.config(width=34)

e8 = tk.OptionMenu(window, varParking, *ParkingList)
e8.config(width=30)

e9 = tk.Entry(window)
e9.config(width=34)

e1.grid(row=2, column=1)
e2.grid(row=3, column=1)
e3.grid(row=4, column=1)
e4.grid(row=5, column=1)
e5.grid(row=6, column=1)
e6.grid(row=7, column=1)
e7.grid(row=8, column=1)
e8.grid(row=9, column=1)
e9.grid(row=10, column=1)

tk.Button(window, text='Générer un prix', command=change_text).grid(row=12, column=0, columnspan=5, pady=10)


my_prix = tk.StringVar()
my_prix.set("\n \n \n \n \n \n ")
Prix = tk.Label(window, textvariable=my_prix).grid(row=15, column=0, columnspan=5)



#adaptation du fichier prediction.py
def prediction():
    
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
    
    parkingSurPlace = 0
    if varParking.get() == 'Oui' :
        parkingSurPlace = 1
    else:
        parkingSurPlace = 0
    
    df2 = { 'Quartier'                  : str(varQuartier.get()),
            'NombreSdB'                 : int(e2.get()), 
            'NbChambres'                : int(e3.get()), 
            'NbLits'                    : int(e4.get()),
            'tokenized_Type_logement'   : str(varTypeLogement.get()),
            'tokenized_type_propriete'  : str(varTypePropriete.get()), 
            'Capacite_accueil'          : int(e7.get()), 
            'parking_sur-place'         : int(parkingSurPlace), 
            'Caution'                   : int(e9.get())
            }

    df_prediction = df_prediction.append(df2, ignore_index = True)

    lbl = preprocessing.LabelEncoder()
    df_prediction.loc[:,'tokenized_Type_logement'] = lbl.fit_transform(df_prediction.loc[:,'tokenized_Type_logement'].astype(str))
    df_prediction.loc[:,'tokenized_type_propriete'] = lbl.fit_transform(df_prediction.loc[:,'tokenized_type_propriete'].astype(str))
    df_prediction.loc[:,'Quartier'] = lbl.fit_transform(df_prediction.loc[:,'Quartier'].astype(str))

    prediction = xg_reg.predict(df_prediction)

    my_prix.set('\n\nNous vous proposons de louer\nvotre logement au prix de\n'+ str(round(prediction[0], 2)) + '€ par nuitée.\n\n')
    
    predicted_csv = df2
    predicted_csv['prediction'] = round(prediction[0], 2)

    #print(predicted_csv)

    predicted_df = pd.DataFrame([predicted_csv])
    predicted_df.to_csv("../Data/predicted.csv", mode='a', index=False, header=False) #header=True si fichier n'existe pas


# Enter into eventloop <- this will keep
# running your application, until you exit
tk.mainloop()

    
