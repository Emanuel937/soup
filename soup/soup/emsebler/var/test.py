from bs4 import BeautifulSoup
import pandas as pd 
import html_file

dom   = html_file.texto
soup  = BeautifulSoup(dom, 'html.parser')

categories_list    = []
subcategories_list = []
child_sub_category = []
urls_list          = []

elements = soup.select(".megamenu__item")
liens     = None
for element in elements:
    category_name = element.select_one(".megamenu__title-wrapper a").text
    print(f"#### parente: {category_name}")
    
    find_sub_cat = element.select(".subdept-nav")
    for sub_cat_elem in find_sub_cat:
        subcategories = sub_cat_elem.select_one(".subdept-nav__title-wrapper").text
        print(f"subcategories is: {subcategories}")

        # Recherchez les sous-catégories uniquement s'il en existe
        try:
            for child in sub_cat_elem.select("ul li a"):
                child_name = child.text
                lien       = child.get("href")
                print(f"last child {child_name}")
                print(f" le liens {lien}")

                categories_list.append(category_name)
                subcategories_list.append(subcategories)
                child_sub_category.append(child_name)
                urls_list.append(lien)
                
        except Exception as e:
            lien = sub_cat_elem.select_one(".subdept-nav__title-wrapper a")
            lien = lien.get("href")
            categories_list.append(category_name)
            subcategories_list.append(subcategories)
            child_sub_category.append("NONE")
            urls_list.append(liens)

# Créer un DataFrame à partir des listes
df = pd.DataFrame({
    'Category': categories_list,
    'Subcategory': subcategories_list,
    'Child_Subcategories':child_sub_category,
    'URL': urls_list
})

# Écrire le DataFrame dans un fichier Excel
df.to_excel('categories_data.xlsx', index=False)

