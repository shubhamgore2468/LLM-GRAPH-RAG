from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import yaml

with open('../configs/config.yaml','r') as file:
    config = yaml.safe_load(file)

# PATH = '/Users/shubhamgore/Downloads/chromedriver-mac-arm64/chromedriver'  # Replace with your actual path
PATH = config['selenium']['driver_path']  # Replace with your actual path

url = "https://www.amazon.com/Capstar-Fast-Acting-Treatment-Small-CA4920Y07AMZ1/dp/B07PXHQ5JR/ref=sr_1_1_sspa?_encoding=UTF8&content-id=amzn1.sym.48a26550-be05-4ac8-96bd-17c43e450b37&dib=eyJ2IjoiMSJ9.pg2nrFAQp6-1I84qGQCtFdxbvyeHDJTfXbvg6YvUL4lhPZIaph0jVQmw2nlU7yzD_bI5Jv-xd0QtzvNhyQ-ebCQVkMtCiWHyiR7k6kyfsF_Ely4b0hiwVmmSSB6PKVVm1_nQAovXYFLTUtHsUJs-g_vTwqfGUiBHOHw6OMdzH0OjTlahjcLhR7jfsylgUZAPFzUfA2IpQEPkeYYZQc3ufBLvWSs5urBhzn0QfBxPr3e9qhPsPzYdpZADtKCPQ6z_iLxwLAB1v25k8JHEFlYCk9P7i4LykISJFnFJkmQoQkQ.MWlRMA6j1PCcZGPCDUSgWoFVdh0BCHIVCo1ABaTyIVs&dib_tag=se&keywords=Dog%2BFlea%2B%26%2BTick%2BControl&pd_rd_r=31f88c00-c940-4ffc-903f-998a9930e918&pd_rd_w=Sh0oP&pd_rd_wg=9YN6B&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=48a26550-be05-4ac8-96bd-17c43e450b37&pf_rd_r=FDAMYWPH5BET60P6FVH8&pf_rd_s=desktop-top-slot-2&qid=1726174842&rdc=1&s=pet-supplies&sr=1-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1"


chromeOptions = Options()
chromeOptions.add_argument("--incognito")
def scrape(urls : str):
    try:
        # for url in urls:
            lst = []
            
            service  = Service(PATH)
            driver = webdriver.Chrome(service = service, options = chromeOptions)

            driver.get(url)
            wait = WebDriverWait(driver, 30)
            all_matches = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-hook="review"]')))
            
            for match in all_matches:
                print(match.text)
                lst.extend([match.text])
                print("************************************************************************************************")
            
            return lst

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == '__main__' : 
    scrape()


# HAVENT ADDED LOOP FOR URLs YET