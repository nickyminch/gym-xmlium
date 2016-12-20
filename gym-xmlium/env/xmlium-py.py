#!/usr/bin/python
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

username='kawaman@mail.bg'
password = 'niki1234'

driver = webdriver.Chrome('./chromedriverlinux')  # Optional argument, if not specified will search path.
driver.get('http://localhost:8080/');
time.sleep(1) # Let the user actually see something!
login = driver.find_element(By.XPATH, '''//span[.='Zur Anmeldung']''')
login.click()
user_elem = driver.find_element(By.XPATH, '''//input[@id='login:login-email-text']''')
user_elem.send_keys(username)
password_elem = driver.find_element(By.XPATH, '''//input[@id='login:login-password-text']''')
password_elem.send_keys(password)
submit_elem = driver.find_element(By.XPATH, '''//span[.='Anmelden']''')
submit_elem.click()
