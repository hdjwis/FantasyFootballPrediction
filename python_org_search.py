from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get('https://www.espn.com/fantasy/football/')
element = driver.find_element(By.LINK_TEXT, 'Mock Draft Lobby')
# element = driver.find_element(By.LINK_TEXT, 'Practice Draft')
driver.close()