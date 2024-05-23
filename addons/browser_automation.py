import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import subprocess

load_dotenv()

user_data_dir = "C:/Users/prakash/AppData/Local/Microsoft/Edge/User Data"
profile = "Profile 3"

def setup_driver():
    print("Killing existing Edge processes.")
    subprocess.call("taskkill /f /im msedge.exe")
    
    print("Setting up Edge options.")
    edge_options = EdgeOptions()
    edge_options.add_argument(f"user-data-dir={user_data_dir}")
    edge_options.add_argument(f"profile-directory={profile}")
    edge_options.add_argument("--start-maximized")
    edge_options.add_argument("--disable-blink-features=AutomationControlled")
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--no-sandbox")
    edge_options.add_argument("--disable-dev-shm-usage")
    edge_options.add_argument("--remote-debugging-port=9223")

    print("Initializing Edge WebDriver.")
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=edge_options)
    return driver

def perform_steps(url: str, tag: str, keyword: str, seo_title: str, meta_description: str):
    print("Setting up the WebDriver.")
    driver = setup_driver()
    
    try:
        print(f"Opening URL: {url}")
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(0.5)

        print("Filling in the tag.")
        tag_xpath = '//*[@id="components-form-token-input-0"]'
        tag_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, tag_xpath)))
        tag_element.send_keys(tag)
        time.sleep(0.5)

        print("Filling in the keyword.")
        keyword_xpath = '//*[@id="focus-keyword-input-metabox"]'
        keyword_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, keyword_xpath)))
        keyword_element.send_keys(keyword)
        time.sleep(0.5)

        print("Filling in the SEO title.")
        seo_title_xpath = '//*[@id="yoast-google-preview-title-metabox"]/div/div/div'
        seo_title_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, seo_title_xpath)))
        seo_title_element.click()
        time.sleep(0.5)
        seo_title_element.send_keys('\b' * 15)  # Press backspace 15 times
        time.sleep(0.5)
        seo_title_element.send_keys(seo_title)
        time.sleep(0.5)

        print("Filling in the meta description.")
        meta_description_xpath = '//*[@id="yoast-google-preview-description-metabox"]/div/div/div'
        meta_description_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, meta_description_xpath)))
        meta_description_element.send_keys(meta_description)
        time.sleep(30)

        print("Clicking the save button.")
        button_xpath = '//*[@id="editor"]/div[1]/div[1]/div[1]/div/div[3]/button'
        button_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, button_xpath)))
        button_element.click()
        time.sleep(8)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Quitting the WebDriver.")
        driver.quit()

