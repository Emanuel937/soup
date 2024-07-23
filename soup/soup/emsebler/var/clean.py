import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Fonction pour attendre que les éléments se chargent
def wait_for_elements(driver, timeout, selector):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, selector)))

# Démarrer le navigateur web Firefox
driver = webdriver.Firefox()

# Charger le fichier Excel
df = pd.read_excel('liens.xlsx')
"""
# ""Récupérer les liens de la colonne "Lien"
liens = df['Lien'].dropna() # Supprimer les valeurs nulles et convertir en liste
# Parcourir les liens
for lien in liens:
    # Ouvrir chaque lien dans le navigateur
    for page in range(1, 1000):
        
        driver.get(f"{lien}?page={page}")

        # Attendre que la page se charge et accepter les cookies si nécessaire
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body")))
        accept_cookies_button = driver.find_element(By.CSS_SELECTOR, "button#onetrust-accept-btn-handler")
        if accept_cookies_button.is_displayed():
            accept_cookies_button.click()

        # Analyser le contenu de la page avec BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Vérifier si la page indique qu'il n'y a pas de résultats
        if soup.find('span', class_='no-results'):
            break
        else:
            # Trouver tous les éléments div avec la classe "ais-Hits--item"
            items = soup.find_all("div", class_="ais-hits--item")

            # Parcourir tous les éléments et extraire le code entre parenthèses
            for item in items:
                # Trouver le texte contenu dans les parenthèses
                code = item.find("span", class_="smaller-text-heading").text.strip("()").strip()
                print(code)

# Fermer le navigateur
driver.quit()
print(liens)
"""