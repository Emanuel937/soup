import pandas as pd
import os

dataframes = []
d = os.path.dirname(os.path.abspath(__file__))
# Obtenir le chemin absolu du fichier data_1.xlsx
def gatering_data(file_name):
    global dataframes, d
    # Répertoire contenant les fichiers XLS
    repertoire = d

    # Liste pour stocker les DataFrames de chaque fichier XLS
    

    # Parcourir tous les fichiers dans le répertoire
    for fichier in os.listdir(repertoire):
        if fichier.endswith('.xls') or fichier.endswith('.xlsx'):
            # Chemin complet du fichier
            chemin_fichier = os.path.join(repertoire, fichier)
            # Lire le fichier XLS et stocker son contenu dans un DataFrame
            df = pd.read_excel(chemin_fichier)
            # Ajouter le DataFrame à la liste
            dataframes.append(df)

    # Concaténer tous les DataFrames en un seul
    df_concatene = pd.concat(dataframes, ignore_index=True)

    # Chemin pour sauvegarder le fichier contenant toutes les données

    # Sauvegarder le DataFrame concaténé dans un fichier XLS
    df_concatene.to_excel(file_name, index=True)

    print("Fichier concaténé créé avec succès ")
