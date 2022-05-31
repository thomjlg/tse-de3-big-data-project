#Importation des librairies
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import re
from nltk import sent_tokenize
import nltk
from deep_translator import GoogleTranslator
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import shapefile
from shapely.geometry import Point # Point class
from shapely.geometry import shape # shape() is a function to convert geo objects through the interface
from wordcloud import WordCloud
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
from sklearn import preprocessing

# Import des données 
df = pd.read_csv("../Data/33000-BORDEAUX_nettoye.csv")

#affiche de quelques lignes au hasard
pd.set_option('display.max_columns', None)

#suppression colonne URL car inutile pour notre analyse
del df["Url"]

#suppression des colonnes en double
#colonne PrixNuitee = prix_nuitee (en double), on la supprime
del df["prix_nuitee"]                 

for column in df:
    if(df[column].to_numpy() [0] == df[column].to_numpy() ).all(0)  == True:
        del df[column] #va supprimer la colonne shampooing car inutile, que des valeurs à 0

df[df.duplicated() == 1]
#aucune ligne dupliquée !

#renommage de la colonne rection_semaine en reduction_semaine
df.rename(columns = {'rection_semaine':'reduction_semaine'}, inplace = True)

#NombreSdB max aberrant : 75

nb_SdB = 20

#display(df[df.NombreSdB > nb_SdB].sort_values(by=['NombreSdB']))

#Correction NombreSdB en ayant analysé les annonces airbnb
#Si 15 --> 1,5
#Si 25 --> 2,5
#Si 35 --> 3,5
#Si 75 --> 1

df.NombreSdB[df.NombreSdB == 15] = 1.5
df.NombreSdB[df.NombreSdB == 25] = 2.5
df.NombreSdB[df.NombreSdB == 35] = 3.5
df.NombreSdB[df.NombreSdB == 75] = 1

#Si studio chambre T1 studette dans Titre --> NombreSdB = 1 pour cohérence data
df.loc[df['Titre'].str.contains('studio', case=False), 'NombreSdB'] = 1
df.loc[df['Titre'].str.contains('chambre', case=False), 'NombreSdB'] = 1
df.loc[df['Titre'].str.contains('T1', case=False), 'NombreSdB'] = 1
df.loc[df['Titre'].str.contains('studette', case=False), 'NombreSdB'] = 1

#suppressions des lignes ayant un prix nul
df = df[df['PrixNuitee'] != 0]
#suppression des lignes ayant des prix de plus de 200€
#df = df[df['PrixNuitee'] <= 200]

for column in df:
    if df[column].isnull().sum() / df.shape[0] *100 > 50:
        print(column)
        print(df[column].isnull().sum(), 'valeurs nulles')
        print(round(df[column].isnull().sum() / df.shape[0] *100, 2), "% de valeurs nulles\n")
        del df[column] 
        
#suppression colonne Animal_sur_place

#Ajout du quartier
for i, row in df.iterrows():
    longitude = df.at[i, 'Longitude']
    latitude = df.at[i, 'Latitude']

    point_to_check = (longitude, latitude) # an x,y tuple
    shp = shapefile.Reader('../Data/se_quart_s/se_quart_s.shp') #open the shapefile
    all_shapes = shp.shapes() # get all the polygons
    all_records = shp.records()     
    for j in range(len(all_shapes)):
        boundary = all_shapes[j] # get a boundary polygon
        if Point(point_to_check).within(shape(boundary)): # make a point and see if it's in the polygon
            name = all_records[j][2] # get the second field of the corresponding record
            df.at[i, "Quartier"] = name

#ajout d'un index
df['index_col'] = df.index
nb_lignes = df.index_col.max()

#on traduit tout en français pour un meilleur fonctionnement du modele
#ATTENTION PREND ENVIRON 35 MINUTES
for col in df:
    if df[col].dtypes == 'object':
        for i, row in df.iterrows():
            col_text = df.at[i, col]
            translated = GoogleTranslator(target='fr').translate(col_text)
            df.at[i, col] = translated

for column in df:
    if df[column].dtypes == 'object':
        #tout en minuscule
        df[column] = df[column].str.lower()
        # suppression  des '
        df[column] = df[column].replace(to_replace=r"'", regex=True, value=' ')
        # suppression  des \n \r
        df[column] = df[column].replace(to_replace=r"\n", regex=True, value=' ')
        df[column] = df[column].replace(to_replace=r"\r", regex=True, value='')
        #suppresion nombres et caractères spéciaux mais on garde les accents (latin)
        df[column] = df[column].replace(to_replace=r"[^A-Za-z\u00c0-\u00d6\u00d8-\u00f6\u00f8-\u02af\u1d00-\u1d25\u1d62-\u1d65\u1d6b-\u1d77\u1d79-\u1d9a\u1e00-\u1eff\u2090-\u2094\u2184-\u2184\u2488-\u2490\u271d-\u271d\u2c60-\u2c7c\u2c7e-\u2c7f\ua722-\ua76f\ua771-\ua787\ua78b-\ua78c\ua7fb-\ua7ff\ufb00-\ufb06]+", regex=True, value=' ')
        # suppression des espaces
        df[column] = df[column].replace('{html}','') 
        df[column] = df[column].replace(to_replace='<.*?>', regex=True, value='')
        # suppresions des eventuels liens web
        df[column] = df[column].replace(to_replace='http\S+', regex=True, value='')
        # on garde que les mots de + de 3 lettres
        df[column] = df[column].replace(to_replace=r'\b(\w{1,2})\b', regex=True, value='')
        #on enlève les espaces au début et à la fin
        df[column] = df[column].str.strip()


#tokenisation
tokenizer = RegexpTokenizer(r'\w+')
stop_words = set(stopwords.words('french'))

for column in df:
    if df[column].dtypes == 'object':
        df[column] = df[column].fillna('cellule_vide')
        
#on tokenise
df['tokenized_Titre'] = df['Titre'].apply(tokenizer.tokenize)
df['tokenized_Resume'] = df['Resume'].apply(tokenizer.tokenize)
df['tokenized_Type_logement'] = df['Type_logement'].apply(tokenizer.tokenize)
df['tokenized_type_propriete'] = df['type_propriete'].apply(tokenizer.tokenize)
df['tokenized_conditions_annulation'] = df['conditions_annulation'].apply(tokenizer.tokenize)
df['tokenized_Description'] = df['Description'].apply(tokenizer.tokenize)
df['tokenized_reglement_interieur'] = df['reglement_interieur'].apply(tokenizer.tokenize)

#passage de liste à string
df['tokenized_Titre'] = [','.join(i) for i in df['tokenized_Titre']]
df['tokenized_Resume'] = [','.join(i) for i in df['tokenized_Resume']]
df['tokenized_Type_logement'] = [','.join(i) for i in df['tokenized_Type_logement']]
df['tokenized_type_propriete'] = [','.join(i) for i in df['tokenized_type_propriete']]
df['tokenized_conditions_annulation'] = [','.join(i) for i in df['tokenized_conditions_annulation']]
df['tokenized_Description'] = [','.join(i) for i in df['tokenized_Description']]
df['tokenized_reglement_interieur'] = [','.join(i) for i in df['tokenized_reglement_interieur']]

#on enleve les stop words francais
df['tokenized_Titre'] = df['tokenized_Titre'].apply(lambda x: ' '.join([word for word in x.split(',') if word not in stop_words]))
df['tokenized_Resume'] = df['tokenized_Resume'].apply(lambda x: ' '.join([word for word in x.split(',') if word not in stop_words]))
df['tokenized_Type_logement'] = df['tokenized_Type_logement'].apply(lambda x: ' '.join([word for word in x.split(',') if word not in stop_words]))
df['tokenized_type_propriete'] = df['tokenized_type_propriete'].apply(lambda x: ' '.join([word for word in x.split(',') if word not in stop_words]))
df['tokenized_conditions_annulation'] = df['tokenized_conditions_annulation'].apply(lambda x: ' '.join([word for word in x.split(',') if word not in stop_words]))
df['tokenized_Description'] = df['tokenized_Description'].apply(lambda x: ' '.join([word for word in x.split(',') if word not in stop_words]))
df['tokenized_reglement_interieur'] = df['tokenized_reglement_interieur'].apply(lambda x: ' '.join([word for word in x.split(',') if word not in stop_words]))

for column in df:
    if df[column].dtypes == 'object':
        df[column]= df[column].replace("cellule_vide", "")
        df[column].str.replace('dtype', '')
        df[column].str.replace('Name', '')
        df[column].str.replace('Length', '')
        df[column].str.replace('NaN', '')
        df[column].str.replace('nan', '')
        df[column].str.replace('object', '')
        
df.fillna('', inplace=True)

#export dataset final
df.to_csv("../Data/final_dataset.csv", index=False)
