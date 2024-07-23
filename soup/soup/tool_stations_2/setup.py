from selenium import webdriver
from selenium.webdriver.common.by import By
import var as marques
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options



request_status  = None
excel_file      = []
result_per_page = 50
total_product   = 0
wait_time       = 10000
options         = Options()
options.add_argument("--headless")
driver          = webdriver.Firefox(options=options)

def storeSimpleDataToExcel(title, img, price, marque, link_product,ref, cd_ean,sumary, description, category):
    global excel_file
    excel_file.append({'Product_name': title, 'img_1':img,'Price_ttc':price , 
                        'marque':marque, 'fiche_produt':link_product, 'Reference':ref, 
                        'code_ean':cd_ean,'summary':sumary,'description':description,
                        'category':category })
    
def set_url(marks, page_index):
    global driver
    url      = "https://www.toolstation.fr/search?"
    per_page = 72
    driver.set_page_load_timeout(10000)
    driver.get(f"{url}q={marks}&page={page_index}&hitsPerPage={per_page}")  




#go the site web
def get_product_info(container, mark):
    global total_product, wait_time
    print("the script is running")
    driver.implicitly_wait(5)
    product_card = WebDriverWait(driver, wait_time).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "search-product-container"))
    )
    for product in product_card:
        title = WebDriverWait(product, wait_time).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "f4.f-medium"))
        ).text
        reference = WebDriverWait(product, wait_time).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "smaller-text-heading"))
        ).text
        price = WebDriverWait(product, wait_time).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "sp-price"))
        ).text
        product_img  = WebDriverWait(product, wait_time).until(
            EC.visibility_of_element_located((By.CLASS_NAME,  'product-img'))).get_attribute("src")

        product_link       = product.find_element(By.CLASS_NAME,"product-suggestion").get_attribute("href")
         ################
        
      
        #using beautiful soup to remove data 
        total_product += 1
        storeSimpleDataToExcel(title, product_img, price, mark, product_link, reference,
                               cd_ean=None, sumary=None, description=None, category=None)
        print(f"##### :{product_link} ")
        print(f"Total of the product n° {total_product}")
        print(f"Title {title} reference ***** {reference}")
     
 
#try:
def get_request_status(mark):
    global request_status
    if not driver.find_element(By.XPATH, "/html/body/section[2]/div[1]/div/div/div/div/section/span").is_displayed():

        container = driver.find_element(By.XPATH, "//*[@id='product-list']")  
        get_product_info(container, mark)
        request_status = 200
    else:
        request_status = 400
    return request_status
#block it  
for marque_ord, marque in enumerate(marques.marques):
    print(f" °°°°°°°°°°°°°°°°°°  marques pos ===== {marque}")
    for page_index in range(1, 1000):
        
        #initilize request 
        # get the link for request
        set_url(marque, page_index)
        ###########################
        assert "Recherche" in driver.title
        status =  get_request_status(mark=marque)
        print(f"#######  Status ##########  {status}")
        if  status != 200:
            break
        else:
            print(f" Page index  ////////    ##########   {page_index}")
    df = pd.DataFrame(excel_file)
    df.to_excel(f"tool_stations_{marque}.xlsx", index=True)
    excel_file.clear()

    if marque_ord == len(marques.marques) -1:
        
        print("all data is save now")
#driver.close()
