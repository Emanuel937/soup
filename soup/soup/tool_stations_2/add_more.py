import re
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
repeat_it = 0

dir_path = os.path.dirname(os.path.abspath(__file__))
# Lire le fichier Excel
excel_file = pd.read_excel(f"{dir_path}/tool_file.xlsx", index_col=0)
driver_path = f"{dir_path}/geckodriver"
options.binary_location = driver_path
driver = webdriver.Firefox()
index = 5355
total = 0

def re_start():
    global driver
    driver_path = f"{dir_path}/geckodriver"
    options.binary_location = driver_path
    driver = webdriver.Firefox()



def waiter_fn(timer, css_selector):

    global driver
    # FIND DATA ON DOM
    find_data = WebDriverWait(driver, timer).until(
       EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector)))

    return find_data

def send_request(url):

    # URL OF THE SITE TO
    # EXTRACT DATA
    driver.get(url)
    time.sleep(1)

def accept_cookies():
    button = waiter_fn(3, "button#onetrust-accept-btn-handler" )
    button[0].click()

def send_key_input(reference_code):
    global driver
    wait = 15
    try:
        input_element = waiter_fn(wait, "input#search-autocomplete-input")[0]
        #time.sleep(1)
        input_element.clear()
        input_element.send_keys(reference_code)
        # Soumettre le formulaire en appuyant sur la touche "Entrée"
        input_element.send_keys(Keys.RETURN)
       
        print(f"THE SEND KEY IS : {reference_code}")

    except Exception as e :
        print(e)
        print("Stale element reference exception occurred. Retrying...")
        send_key_input(reference_code)
        # Ajouter une attente courte pour laisser la page se mettre à jour
        # Localiser à nouveau l'élément et réessayer l'envoi des touches
       
      


def data_found(father, child, timer, index):
    try:
        # Attendez jusqu'à ce que l'élément parent soit présent sur la page
        parent_elem = waiter_fn(timer, father)
        if parent_elem:
            # Si l'élément parent est trouvé, trouvez les éléments enfants correspondants
            child_elems = parent_elem[index].find_elements(By.CSS_SELECTOR, child)
            return child_elems
        else:
            # Si l'élément parent n'est pas trouvé, retournez None
            return None
    except Exception as error:
        #print(f"Une erreur s'est produite lors de la recherche de l'élément : {error}")
        return print(error)

def get_product_info(file, index):

    #code_ean    = None
    #main_img    = data_found(father="div.product-image", child="img[role='presentation']", timer=5, index=0)
    #img_2       = data_found(father="div.product-gallery__item", child="img", timer=2, index=1)
    #img_3       = data_found(father="div.product-gallery__item", child="img", timer=1, index=2)
    #description = data_found(father="div.product-main", child=".product-details", timer=5, index=0)
    #details     = data_found(father=".toggled-content", child=".table", timer=7, index=0)
    categories  = None
    cat_2 = None
    cat_3 = None
    def find(html, arg:str)->str:
        soup =  BeautifulSoup(str(html), 'html.parser')
        elem = soup.find('td', string=arg)
        if elem:
            next_elem = elem.find_next_sibling('td')
            return next_elem.text.strip().replace(" ", "").replace(".", "")
        else:
            return None
    try:
        categories = data_found(father=".breadcrumb", child=".breadcrumb-item", timer=1, index=0)
        cat_2  = categories[1].text
        file.loc[index, "Catégorie Produit Niveau 1"] = cat_2
    except Exception as e:
        cat_2 = None
    try:
        categories[2]
        cat_3  = categories[2].text
        file.loc[index, "Catégorie Produit Niveau 2"] = cat_3
    except Exception:
        cat_3 = None
       
    print(cat_2)
    print(cat_3)

def save_data():

    global dir_path
    excel_file.to_excel("tool_file.xlsx", index=True )

def man_script(excel_file, current_index):
    global total
    for row_pos in excel_file.index:
        if row_pos >= 10000:
            reference_vendeur = excel_file.loc[row_pos, "Référence_vendeur"]
            categorie_produit_niveau_1 = excel_file.loc[row_pos, "Catégorie Produit Niveau 1"]
            if pd.isna(categorie_produit_niveau_1):
                # Si la cellule est vide
                clean_ref = re.sub(r'\(([^()]+)\)', r'\1', reference_vendeur)
                send_key_input(clean_ref)
                time.sleep(2)
                get_product_info(excel_file, index=row_pos)
                print(f"index : {row_pos}")
        
        else: 
            continue
def run(attempt=0, max_attempts=10000):
    global index, driver
    try:
        send_request("https://www.toolstation.fr/")
        accept_cookies()
        man_script(excel_file, index)
        save_data()
        print("data saved now ..")
    except Exception as e:
        if attempt % 5 == 0:
            save_data()
            print("data saved now")
            driver.quit()
            re_start()
            run(attempt=attempt + 1, max_attempts=max_attempts)
            
        if attempt < max_attempts:
            print(f"An error occurred: {e}. Retrying...")
            run(attempt=attempt + 1, max_attempts=max_attempts)
        else:
            print(f"Max attempts reached. Exiting.")
            save_data()

    

if __name__ == "__main__":
            run()
            
   
