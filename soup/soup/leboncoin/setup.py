from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Définir le user-agent
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
options = Options()
options.add_argument(f"user-agent={user_agent}")

# Initialiser le pilote du navigateur avec les options spécifiées
driver = webdriver.Firefox(options=options)

try:
    # Aller sur le site pour vérifier le user-agent
    driver.get("http://www.whatsmyua.info/")
    print("Page chargée avec succès.")
    
    # Attendre que l'élément contenant le user-agent soit chargé
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "custom-ua-string"))
    )
    
    # Récupérer et imprimer le user-agent affiché sur la page
    displayed_user_agent = driver.find_element(By.ID, "custom-ua-string").text
    print(f"User-Agent affiché sur la page : {displayed_user_agent}")

    # Vérifier le user-agent directement via JavaScript
    actual_user_agent = driver.execute_script("return navigator.userAgent;")
    print(f"User-Agent récupéré via JavaScript : {actual_user_agent}")
    
    # Comparer les user-agents
    if displayed_user_agent == user_agent:
        print("Le user-agent de la page correspond au user-agent attendu.")
    else:
        print("Le user-agent de la page ne correspond pas au user-agent attendu.")
    
    if actual_user_agent == user_agent:
        print("Le user-agent récupéré via JavaScript correspond au user-agent attendu.")
    else:
        print("Le user-agent récupéré via JavaScript ne correspond pas au user-agent attendu.")
except TimeoutException:
    print("Le chargement de la page a dépassé le temps imparti.")
finally:
    # Fermer le pilote du navigateur
    driver.quit()
