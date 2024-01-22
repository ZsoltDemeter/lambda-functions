try:
    import json
    from selenium.webdriver import Chrome
    from selenium.webdriver.chrome.options import Options
    import os
    import shutil
    import uuid
    import boto3
    from datetime import datetime
    import datetime
    from pymongo import MongoClient

    print("All Modules are ok ...")

except Exception as e:

    print("Error in Imports ")

client = MongoClient(host=os.environ.get("OFP_URI"))


class WebDriver(object):

    def __init__(self):
        self.options = Options()

        self.options.binary_location = '/opt/headless-chromium'
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--start-fullscreen')
        self.options.add_argument('--single-process')
        self.options.add_argument('--disable-dev-shm-usage')

    def get(self):
        driver = Chrome('/opt/chromedriver', options=self.options)
        return driver



def lambda_handler(event, context):
    db = client['OFP-DB']
    collection = db['energy_reports']

    instance_ = WebDriver()
    driver = instance_.get()
    driver.get("https://www.transelectrica.ro/widget/web/tel/sen-harta/-/harta_WAR_SENOperareHartaportlet")
    
    getDate = driver.find_element_by_id("SEN_date")
    getCons = driver.find_element_by_id("SEN_Harta_CONS_value")
    getProd = driver.find_element_by_id("SEN_Harta_PROD_value")
    getCarb = driver.find_element_by_id("SEN_Harta_CARB_value")
    getGaze = driver.find_element_by_id("SEN_Harta_GAZE_value")
    getApe = driver.find_element_by_id("SEN_Harta_APE_value")
    getNucl = driver.find_element_by_id("SEN_Harta_NUCL_value")
    getEolian = driver.find_element_by_id("SEN_Harta_EOLIAN_value")
    getFoto = driver.find_element_by_id("SEN_Harta_FOTO_value")
    getBMASA = driver.find_element_by_id("SEN_Harta_BMASA_value")
    getSold = driver.find_element_by_id("SEN_Harta_SOLD_value")
    
    
    data_to_insert = {
        'Data': getDate.get_attribute('innerHTML'),
        'ConsumMW': getCons.get_attribute('innerHTML'),
        'ProductieMW': getProd.get_attribute('innerHTML'),
        'CarbuneMW': getCarb.get_attribute('innerHTML'),
        'HidrocarburiMW': getGaze.get_attribute('innerHTML'),
        'ApeMW': getApe.get_attribute('innerHTML'),
        'NuclearMW': getNucl.get_attribute('innerHTML'),
        'EolianMW': getEolian.get_attribute('innerHTML'),
        'FotoMW': getFoto.get_attribute('innerHTML'),
        'BiomasaMW': getBMASA.get_attribute('innerHTML'),
        'SoldMW': getSold.get_attribute('innerHTML')
    }
    print(data_to_insert)
    #print("Collection:",collection)
    collection.insert_one(data_to_insert)

    return True
