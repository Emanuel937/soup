
import pandas as pd
import os

dir_path   = os.path.dirname(os.path.abspath(__file__))
# Lire le fichier Excel
excel_file = pd.read_excel(f"{dir_path}/all_stations.xlsx")
print(excel_file["Reference"].head())