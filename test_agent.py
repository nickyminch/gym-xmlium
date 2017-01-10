#!/usr/bin/python

import gym
import time
import random
import xmlium
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
executed_form_actions = {}
action3 = None
while True:
    #print(env.action_space.keys())
    form_keys = list(env.action_space)
    #print(list(form_keys))
    form_keys_len = len(form_keys)
    form_indexes = list(range(0, form_keys_len-1))
    
    for form_index in form_indexes:
        form_key = form_keys[form_index]
        #print(form_key)
        elem_dict = env.action_space.get(form_key, {})
        #print(elem_dict.keys())
        executed_elem_actions = executed_form_actions.get(form_key, {})
        arr = [(form_key, executed_elem_actions)]
        dict = {}
        executed_form_actions.update(dict)

        elem_keys = list(elem_dict)
        #print(list(elem_keys))
        elem_keys_len = len(elem_keys)
        elem_indexes = list(range(0, elem_keys_len-1))
        for elem_index in elem_indexes:
            elem_key =elem_keys[elem_index]
            print(elem_key)
            actions = elem_dict.get(elem_key, [])
            executed_actions = executed_elem_actions.get(elem_key, {})
            action3 =  random.choice(actions)
            arr = [(action3.action,True)]
            dict = {}
            executed_actions.update(dict)
            arr = [(elem_key,executed_actions)]
            dict = {}
            executed_elem_actions.update(dict)
    
            print("index=%s form_id=%s element_id=%s elemType=%s"%(action3.action, action3.xmliumob.form, action3.xmliumob.element, action3.xmliumob.elemType))
            
            #print(action.elems[action.index])
            #elem =  action.elems[action.index];
            #print(elem.get_attribute("id"))
            observation, r, done, info = env.step(action3)
            #print(env.action_space)
            env.render()
            time.sleep(0.3)
            form = env.action_space.get(action3.xmliumob.form, None)
            if info==True:
                if action3.xmliumob.form not in env.action_space:
                    print("==========================break=============================")
                    break
            if len(executed_elem_actions.keys())>=len(actions):
                print("==========================!!!break!!!=============================")
                break
        if form is None:
            print("==========================break=============================")
            if action3.xmliumob.form in env.action_space:
                executed_form_actions.pop(form)
            break
                