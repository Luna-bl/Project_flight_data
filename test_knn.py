from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
from knn_function import knn_predict


train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

X_train = train.drop(columns=['phase'])
y_train = train['phase']
X_test = test.drop(columns=['phase'])
y_test = test['phase']


# Convertir en tableaux numpy si nécessaire (sécurité)
X_train_np = X_train.values
y_train_np = y_train.values
X_test_np = X_test.values
y_test_np = y_test.values

# Choisir une valeur de k
k = 5

# Lancer la prédiction
y_pred = knn_predict(X_train_np, y_train_np, X_test_np, k)

# Évaluer le modèle
accuracy = accuracy_score(y_test_np, y_pred)
print(f"Accuracy: {accuracy:.2f}") # resultat affiche en %

print("Rapport de classification :")
print(classification_report(y_test_np, y_pred))
