from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time
# Charger les liens depuis le fichier Excel
file = pd.read_excel('categories_data.xlsx')
timer = 0
data  = {"code_ean":[], "url":[] }

# Démarrer le navigateur web Firefox
dir_path = os.path.dirname(os.path.abspath(__file__))
driver_path = f"{dir_path}/geckodriver"
options = webdriver.FirefoxOptions()
options.binary_location = driver_path
driver = webdriver.Firefox(options=options)

def accept_cookies():
    # Attendre que le bouton d'acceptation des cookies soit présent
    button = waiter_fn(10, "button#onetrust-accept-btn-handler")
    button[0].click()

def waiter_fn(timer, css_selector):
    # Attendre que l'élément soit présent dans le DOM
    find_data = WebDriverWait(driver, timer).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
    return find_data

# Parcourir tous les liens
for index in file.index:
    if index >= 114:
        # Initialiser la variable page_index à 1
        # Ouvrir chaque lien
        page_index = 1  
        lien = file.loc[index, "URL"]
        not_this = ["Nouveautés", "Bons plans du moment", "Déstockage"]
        if any(word.replace(" ", "") in file.loc[index, "Category"].replace(" ", "") for word in not_this):
            continue
        else:
            # Votre code ici
            while True:
                driver.get(f"{lien}?page={page_index}")
                # Attendre que la page soit chargée
                time.sleep(8)
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.TAG_NAME, "div")))
                # Récupérer le code HTML de la page
                html = driver.page_source
                # Utiliser BeautifulSoup pour analyser le code HTML
                soup = BeautifulSoup(html, "html.parser")
                # Vérifier s'il n'y a pas de résultats
                not_found = soup.select_one(".no-results")
                if not_found and not_found.get("style"):
                    # Trouver tous les éléments div avec la classe "ais-hits--item"
                    items = soup.find_all("div", class_="ais-hits--item")
                    print(f"Total : {len(items)}")
                    for item in items:
                        try:
                            # Trouver le texte contenu dans les parenthèses
                            code = item.find("span", class_="smaller-text-heading").text.strip("()").strip()
                            data["code_ean"].append(code)
                            data["url"].append(lien)
                        except Exception:
                            print("not found")
                    # Incrémenter page_index pour passer à la page suivante
                    page_index += 1
                else:
                    break

# Créer un DataFrame et enregistrer les données dans un fichier Excel
df = pd.DataFrame(data)
df.to_excel("output4.xlsx", index=False)

# Fermer le navigateur
driver.quit()
