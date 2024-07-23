from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import urls 
import time


data = []
total = 0

links = urls.urls
def check_internet_connection():
    url = "http://www.google.com"  # URL à vérifier pour la connexion Internet
    timeout = 5  # Temps d'attente en secondes pour la tentative de connexion

    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("not connected")
        return False

# Vérifier la connexion Internet
# Parcourir chaque URL
url_index = 1
for index, url in enumerate(urls.urls, start=1):
    stop = 0
    for pageIndex in range(1, 300):
        while not check_internet_connection():
            time.sleep(10)  # Attendre 10 secondes avant de vérifier à nouveau
        response = requests.get(f"{url}?page={pageIndex}")
        name = None 
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            scripts = soup.find_all('script')
            for index, script in enumerate(scripts, start=1):
                name = None
                if index == 20:
                    data_json = json.loads(script.text)
                    businesses = data_json["props"]["pageProps"]["businessUnits"]["businesses"]
                    for business in businesses:
                        name = business["displayName"]
                        if name:
                            total +=1
                        numberOfview = business["numberOfReviews"]
                        score = business["trustScore"]
                        location = business.get("location", {})
                        adress = location.get("address", "")
                        city = location.get("city", "")
                        codeZip = location.get("zipCode", "")
                        country = location.get("country", "")
                        contact_info = business.get("contact", {})
                        website = contact_info.get("website", "")
                        mail = contact_info.get("email", "")
                        tel = contact_info.get("phone", "")
                        categories = business["categories"]
                        # Récupérer toutes les catégories de l'entreprise
                        all_category = [category["displayName"] for category in categories]
                        all_category_str = ",".join(all_category)
                        # Ajouter les données de l'entreprise à la liste
                        data.append({
                            "Name": name,
                            "Number of Reviews": numberOfview,
                            "Trust Score": score,
                            "Address": adress,
                            "City": city,
                            "Zip Code": codeZip,
                            "Country": country,
                            "Website": website,
                            "Email": mail,
                            "Phone": tel,
                            "Categories": all_category_str,
                            "pageIndex":pageIndex,
                            "link"     :url
                        })
        print(f"name now is ---------:{name} ({total})")
        if name is None:
            print(" waiting .......")
            print(f"current url is {url}&page={pageIndex}")
            time.sleep(10)
            stop += 1 
       

        if stop >= 7:
           print(f" nexting ...... {stop}")
           break
else:
    df = pd.DataFrame(data)
    df.to_excel(f"final-data.xlsx", index=False)

  
    