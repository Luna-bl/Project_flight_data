import pandas as pd
from src.io import load_csv
from src.derive import compute_vertical_speed, segment_phases

def prepare_knn_dataset(csv_path: str) -> pd.DataFrame:
    # 1. Charger les données
    df = load_csv(csv_path)

    # 2. Calculer la vitesse verticale pour voir si l'avoin monte ou descent 
    df['vs_mps'] = compute_vertical_speed(df)

    # 3. Segmenter les phases de vol
    df['phase'] = segment_phases(df)

    # 4. Extraire les colonnes features + label = caracteristiques pour le modele 
    features = ['alt_m', 'gs_mps', 'tas_mps', 'vs_mps', 'hdg_deg']
    df_knn = df[features + ['phase']].copy() # on cree un new data frame avec es colonnes + phase 

    # 5. Vérifier valeurs manquantes
    if df_knn.isnull().any().any():
        print("Attention : data missing, delete line.")
        df_knn = df_knn.dropna()

    return df_knn

if __name__ == '__main__':
    dataset = prepare_knn_dataset('flight_sample.csv')
    print(dataset.head())
    print(dataset.describe())  # affiche résumé statistique

    
