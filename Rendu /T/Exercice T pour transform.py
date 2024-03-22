#Import de pandas pour la manipulation des données tabulaires.
#Import de MinMaxScaler  pour normaliser les données.
#Import de LinearRegression  et train_test_splitpour la validation croisé.

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

# Chargement du jeu de données depuis le fichier CSV
dataframe = pd.read_csv('jeux_de_donnees.csv')

# 1. Analyse des données
print("Nombre total d'enregistrements :", len(dataframe))
print("-------------------------------------------------------------:")
print("Colonnes du jeu de données :", dataframe.columns)
print("-------------------------------------------------------------:")
print("Types de données des colonnes :\n", dataframe.dtypes)
print("-------------------------------------------------------------:")
print("Résumé statistique des données :\n", dataframe.describe())
print("-------------------------------------------------------------:")


# 2. Traitement des données (changement de type, normalisation, valeurs manquantes)

# Convertir la colonne "Date_vente" en type de date au lieu de la laisser en type objet 
#dataframe['Date_vente'] = pd.to_datetime(dataframe['Date_vente'])

#Normalisation des données.
scaler = MinMaxScaler()
col_num = ['Quantite_vendue', 'Prix_unitaire',]
dataframe[col_num] = scaler.fit_transform(dataframe[col_num ])


#Traitement valeurs manquantes 
#Données avant traitement
vide_par_colonne = dataframe.isnull().sum()
print("\nNombre de valeurs manquantes par colonne :\n", vide_par_colonne)
print("-------------------------------------------------------------:")

#Traitement 
QV_moyenne = dataframe['Quantite_vendue'].mean()
dataframe['Quantite_vendue'].fillna(QV_moyenne, inplace=True)
dataframe.dropna(subset=['Prix_unitaire'], inplace=True)
nv_valeurs = [f"eid{i}" for i in range(1, 11)]
cellules_nulles = dataframe['Nom_produit'].isnull()
dataframe.loc[cellules_nulles, 'Nom_produit'] = nv_valeurs[:sum(cellules_nulles)]


#Données aprés traitement
vide_par_colonne = dataframe.isnull().sum()
print("\nNombre de valeurs manquantes par colonne aprés traitement :\n", vide_par_colonne)
print("-------------------------------------------------------------:")

# 3. Gestion des valeurs aberrantes
val_aberrantes_avant = dataframe[dataframe['Quantite_vendue'] > 70].shape[0]
print("Nombre de valeurs aberrantes avant le remplacement :", val_aberrantes_avant)
#quantite_vendue_median = dataframe['Quantite_vendue'].median()
dataframe.loc[dataframe['Quantite_vendue'] > 50, 'Quantite_vendue'] = QV_moyenne

# 4. Détection et suppression des doublons
data_avant_supp = len(dataframe)
dataframe.drop_duplicates(inplace=True)
data_apres_supp = len(dataframe)
print("Data avant la suppression :", data_avant_supp)
print("Data après la suppression :", data_apres_supp)
print("-------------------------------------------------------------:")

# Transformation supplémentaire 1 : Ajout d'une colonne 'Montant_total'
dataframe['Montant_total'] = dataframe['Quantite_vendue'] * dataframe['Prix_unitaire']

# Transformation supplémentaire 2 : Normalisation de la colonne 'Quantite_vendue'
quantite_vendue_max = dataframe['Quantite_vendue'].max()
dataframe['Quantite_vendue_normalisee'] = dataframe['Quantite_vendue'] / quantite_vendue_max

# Affichage du DataFrame après les transformations
print("\nDataFrame après les transformations :\n", dataframe)



print("-------------------------------------------------------------:")

# Gestion des valeurs manquantes
dataframe.fillna(dataframe.mean(), inplace=True)

# Encodage one-hot des variables catégorielles (Nom_produit)
dataframe = pd.get_dummies(dataframe, columns=['Nom_produit'])

# Extraction des caractéristiques temporelles (Date_vente)
dataframe['Date_vente'] = pd.to_datetime(dataframe['Date_vente'])
dataframe['annee_vente'] = dataframe['Date_vente'].dt.year
dataframe['mois_vente'] = dataframe['Date_vente'].dt.month
dataframe['jour_semaine_vente'] = dataframe['Date_vente'].dt.dayofweek

# Suppression de la colonne originale 'Date_vente'
dataframe.drop(columns=['Date_vente'], inplace=True)

# Division des données en ensembles d'entraînement et de test
X = dataframe.drop(columns=['Montant_total'])  # Features
y = dataframe['Montant_total']  # Target variable
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modélisation et évaluation sur l'ensemble d'entraînement
model = LinearRegression()
model.fit(X_train, y_train)
train_score = model.score(X_train, y_train)
print("Score R² sur l'ensemble d'entraînement :", train_score)

# Validation croisée sur l'ensemble d'entraînement
cross_val_scores = cross_val_score(model, X_train, y_train, cv=5)
print("Scores R² de validation croisée sur l'ensemble d'entraînement :", cross_val_scores)

# Prédiction et évaluation sur l'ensemble de test
test_score = model.score(X_test, y_test)
print("Score R² sur l'ensemble de test :", test_score)
