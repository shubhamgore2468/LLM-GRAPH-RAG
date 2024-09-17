from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import yaml
import sys
import os
from dotenv import load_dotenv
import random
import time
import logging
import json
# import sys
# sys.path.append("..")

# Load environment variables from .env file
load_dotenv()

# Add the root directory of your project to sys.path
sys.path.append(os.getenv('PYTHONPATH'))

def load_config():
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../configs/config.yaml'))
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

config = load_config()

# PATH = '/Users/shubhamgore/Downloads/chromedriver-mac-arm64/chromedriver'  # Replace with your actual path
PATH = config['selenium']['driver_path']  # Replace with your actual path

# url = "https://www.amazon.in/Motorola-Brilliant-Green-128GB-Storage/dp/B0DDYBQWLW/ref=sr_1_3?crid=1ZEVH9VBTG5V3&dib=eyJ2IjoiMSJ9.xSK__cXfm1_pM6Dmm1HbX8qracVGl605lwxf0ctD9fHoVkj3PwTSXgBa7Tx1o_CEZMRb0ZM3e38MUTm9YDP6_Rd2uszH7QpCLBzuWjncj5zj0KMESF_1IY2rhSKWsPVXTd57N2CspgVSkCzWfxqh8bDkoK-DerDrQNG4xn4jIhrq91620cmfu2XQSdd8XPTXj1p6fiBIlD8NZ65wQWoRchJQDNa6IEVdIaGPU10E_Ymb5czeG66-krnPKVrjF_IKpx9DJ6u7HYK0XDmy-WF8LsDDZ5vhUAR_qcOM8SKF3wM.BoZAXjWS-LlECq2BGfotRqzNJ56FS6wpoa3ga1_uNgM&dib_tag=se&keywords=motorola&nsdOptOutParam=true&qid=1726529362&s=electronics&sprefix=%2Celectronics%2C680&sr=1-3"
url = "https://www.walmart.com/ip/50PCS/8004357405?classType=VARIANT&athbdg=L1600"
def get_domain(url):
    url = url.split("/")[2]
    return url.split(".")[1]

chromeOptions = Options()
chromeOptions.add_argument("--incognito")

results_json = {}

def scrape(urls):
    # for url in urls:
    delay = random.uniform(5, 20)
    logging.info(f"Sleeping for {delay:.2f} seconds")
    time.sleep(delay)

    lst = []
    
    try:
        service = Service(PATH)
        driver = webdriver.Chrome(service=service, options=chromeOptions)

        driver.get(url)
        wait = WebDriverWait(driver, 30)
        domain = get_domain(url)
        if domain == "amazon":
            all_matches = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-hook="review"]')))
        elif domain == "another_domain":  # Replace with the actual domain you want to check
            all_matches = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//li[@class="dib w-100 mb3"]')))
        else:
            logging.error(f"Unsupported domain: {domain}")
            # continue

        for match in all_matches:
            logging.info(match.text)
            lst.extend([match.text])
            logging.info("************************************************************************************************")
        
        results_json[domain].extend(lst)
        return lst

    except Exception as e:
        logging.error(f"An error occurred while processing URL {url}: {e}")
    finally:
        driver.quit()


if __name__ == '__main__' : 
    results = scrape()
    logging.info(results)

    if os.path.exists('matches.json'):
    # Read the existing content
        with open('matches.json', 'r') as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    # Append the new data
    existing_data.append(results_json)

    # Write the updated content back to the file
    with open('matches.json', 'w') as f:
        json.dump(existing_data, f, indent=4)

    print('\n')


# HAVENT ADDED LOOP FOR URLs YET