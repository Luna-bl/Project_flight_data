import pandas as pd
import numpy as np
from collections import Counter
from knn_data_preparation import prepare_knn_dataset
from knn_function import knn_predict, euclidean_distance, normalize_with_params 

# Préparation du dataset
df = prepare_knn_dataset('flight_sample.csv')

# Mélanger le dataset original (non normalisé) avant split
df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Split train/test
train_size = int(0.8 * len(df_shuffled))
train = df_shuffled.iloc[:train_size]
test = df_shuffled.iloc[train_size:]

# Calcul des paramètres de normalisation sur le train uniquement
mean = train.drop(columns=['phase']).mean()
std = train.drop(columns=['phase']).std()

# Normaliser train et test avec les mêmes paramètres
train_norm = normalize_with_params(train, mean, std)
test_norm = normalize_with_params(test, mean, std)

# Sauvegarder les fichiers normalisés
train_norm.to_csv('train.csv', index=False)
test_norm.to_csv('test.csv', index=False)

# Préparer les variables d'entrée et labels
X_train = train_norm.drop(columns=['phase'])
y_train = train_norm['phase']
X_test = test_norm.drop(columns=['phase'])
y_test = test_norm['phase']

