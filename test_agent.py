#!/usr/bin/python

import gym
import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

env = gym.make('xmlium-v0')
username='..'
password = '..'

#self.driver = webdriver.Chrome('./chromedriverlinux')  # Optional argument, if not specified will search path.
env.driver = webdriver.Firefox(executable_path='./geckodriverlinux')  # Optional argument, if not specified will search path.

env.wait = WebDriverWait(env.driver, 4)

env.driver.get('http://localhost:8080/');
time.sleep(1) # Let the user actually see something!
login =env.wait.until(EC.presence_of_element_located( (By.XPATH, '''//span[.='??To Login??']''') ))
#login = env.driver.find_element(By.XPATH, '''//span[.='Zur Anmeldung']''')
login.click()
user_elem = env.wait.until(EC.presence_of_element_located( (By.XPATH, '''//input[@id='loginform:username']''') ))
user_elem.send_keys(username)
password_elem = env.wait.until(EC.presence_of_element_located( (By.XPATH, '''//input[@id='loginform:password']''') ))
password_elem.send_keys(password)
submit_elem = env.wait.until(EC.presence_of_element_located( (By.XPATH, '''//span[.='Login']''') ))
submit_elem.click()
time.sleep(1)
env.wait = WebDriverWait(env.driver, 0.5)

#env.configure()
observation = env.reset()
while True:
    for action in random.choice(env.action_space):
            action3 =  random.choice(action)
    
            print("index=%s form_id=%s element_id=%s elemType=%s"%(action3.action, action3.xmliumob.form, action3.xmliumob.element, action3.xmliumob.elemType))
            
            #print(action.elems[action.index])
            #elem =  action.elems[action.index];
            #print(elem.get_attribute("id"))
            observation, r, done, info = env.step(action3)
            #print(env.action_space)
            env.render()
            time.sleep(0.3)
            if info==True:
                break
