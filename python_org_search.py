from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from dotenv import load_dotenv
import os

load_dotenv()
driver = webdriver.Chrome()
driver.maximize_window() # Maximize the window for better visibility and element interaction
driver.get('https://www.espn.com/fantasy/football/')
user_trigger = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a#global-user-trigger"))
)
user_trigger.click()
login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.global-user div.global-user-container ul.account-management a[href='#']"))
    )
login_button.click()
WebDriverWait(driver, 15).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "oneid-iframe")))
email_input  = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "InputIdentityFlowValue"))
)
email = os.getenv("EMAIL")
email_input.send_keys(email)
email_input.send_keys(Keys.ENTER)
password_input  = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "InputPassword"))
)
password = os.getenv("PASSWORD")
password_input.send_keys(password)
password_input.send_keys(Keys.ENTER)
driver.switch_to.default_content()

try:
    logged_in_dashboard_element_xpath = "//a[contains(@href, '/myteams') and normalize-space()='My Teams']"
    WebDriverWait(driver, 10).until( 
        EC.presence_of_element_located((By.XPATH, logged_in_dashboard_element_xpath))
    )
    print("Main fantasy page appears settled and logged in.")
    time.sleep(3) 
except Exception as e:
    print(f"WARNING: Logged-in dashboard element not found. Page might not be fully loaded or logged in: {e}")
    
mock_draft_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//li[@class='quicklinks_list__item']/a[.//span[@class='quicklinks_list__name' and normalize-space()='Mock Draft Lobby']]"))
)
actions = ActionChains(driver)
actions.move_to_element(mock_draft_link).click().perform()
WebDriverWait(driver, 15).until(EC.url_contains("mockdraftlobby"))

practice_draft_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@class='Button Button--alt' and normalize-space()='Practice Draft']"))
)
practice_draft_button.click()
start_draft_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@class='Button Button--default Button--custom KonaForm__SubmitButton' and normalize-space()='Start Practice Draft']"))
)
start_draft_button.click()

time.sleep(5)
driver.quit()

