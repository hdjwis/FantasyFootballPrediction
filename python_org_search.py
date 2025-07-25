from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time
from dotenv import load_dotenv
import os
import pandas as pd

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
draft_board_loaded_locator = (By.XPATH, "//h1[contains(@class, 'title') and contains(text(), 'ESPN Fantasy Football Draft')]")
original_window = driver.current_window_handle
old_window_handles = driver.window_handles # Get all current open windows/tabs
WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(len(old_window_handles) + 1))

# Loop through all window handles and switch to the new one
new_window_handle = None
for handle in driver.window_handles:
    if handle != original_window:
        new_window_handle = handle
        break
driver.switch_to.window(new_window_handle)
qb_pred = pd.read_csv('qb_pred.csv')
qb_pred['2025 PPR Prediction'] = qb_pred['2025 PPR Prediction']*0.8
rb_pred = pd.read_csv('rb_pred.csv')
wr_pred = pd.read_csv('wr_pred.csv')
te_pred = pd.read_csv('te_pred.csv')
pred = pd.concat([qb_pred, rb_pred, wr_pred, te_pred])
pred.sort_values(by='2025 PPR Prediction', ascending=False, inplace=True)
pred.reset_index(inplace=True)
pred.drop(['index', 'Unnamed: 0'], axis=1, inplace=True)
pred_ls = list(pred.head(192)['Player'])
# checkbox_input_locator = (By.CSS_SELECTOR, "div.autoPick-toggle.form__group--toggle input[type='checkbox']")
# checkbox_input_element = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located(checkbox_input_locator) # Use presence if it's hidden but clickable
# )
# checkbox_input_element.click()
for i in range(192):
    player_name_input_locator = (By.CSS_SELECTOR, "input[placeholder='Player Name']")
    player_name_input_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(player_name_input_locator) # Use element_to_be_clickable for inputs
    )
    # You can now interact with the input box, e.g., send keys
    player_name_input_element.send_keys(pred_ls[i])
    player_name_input_element.click()
    player_match_button_locator = (By.XPATH, f"//button[contains(@class, 'player--search--match')]//span[normalize-space()='{pred_ls[i]}']/ancestor::button")
    try:
        player_match_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(player_match_button_locator)
        )
        player_match_button.click()
        player_link_locator = (By.XPATH, f"//a[normalize-space()='{pred_ls[i]}']")
        player_link_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(player_link_locator)
        )
        player_link_element.click()
        queue_button_locator = (By.XPATH, "//button[@class='Button Button--lg Button--alt ttu Button--queue PlayerCard__action-btn' and normalize-space()='Queue']")
        queue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(queue_button_locator)
        )
        queue_button.click()
        close_button_locator = (By.CSS_SELECTOR, "div.jsx-3684495974.lightbox__closebtn")
        close_button_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(close_button_locator)
        )
        close_button_element.click()
    except:
        print(pred_ls[i])

    player_name_input_element.clear()

time.sleep(1000)
driver.quit()