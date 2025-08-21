import pandas as pd
import numpy as np
from collections import Counter

# def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
#     df_norm = df.copy()
#     for column in df.columns:
#         if column != 'phase':  # on ne normalise pas la colonne 'phase' car ce n est pas une valeur numerique
#             mean = df[column].mean()
#             std = df[column].std() # std calcul l'ecart-type
#             df_norm[column] = (df[column] - mean) / std #  # valeur normalisee = (valeur - moyenne)/std
#     return df_norm

def normalize_with_params(df: pd.DataFrame, mean: pd.Series, std: pd.Series) -> pd.DataFrame:
    df_norm = df.copy()
    for col in mean.index:
        df_norm[col] = (df[col] - mean[col]) / std[col]
    return df_norm

def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

def knn_predict(X_train, y_train, X_test, k):
    y_pred = []
    for test_point in X_test:
        distances = [euclidean_distance(test_point, train_point) for train_point in X_train] # on calcule la distamce entre le point test et tous les poinst d'entrainememt
        k_indices = np.argsort(distances)[:k] # on selectionne les k points d'entrainenemt les plus proches 
        k_nearest_labels = [y_train[i] for i in k_indices] # À partir des indices des voisins proches, on récupère leurs classes (labels) dans y_train.
        most_common = Counter(k_nearest_labels).most_common(1)[0][0] # on compte et on choisit la classe majoritaire
        y_pred.append(most_common)
    return y_pred
