import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from random import randint


class XmliumEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    self.src = QuandlEnvSrc() 
    self.trading_cost_bps = 1e-3
    self.time_cost_bps    = 1e-4
    self.action_space = spaces.Discrete( 3 )
    self.observation_space= spaces.Box( self.src.min_values,
                                        self.src.max_values)
    self.reset()

  def _configure(self, display=None):
    self.display = display
    self.driver = None
    self.form = None
    self.elem = None
    username='kawaman@mail.bg'
    password = 'niki1234'
    
    self.driver = webdriver.Chrome('./chromedriverlinux')  # Optional argument, if not specified will search path.
    self.driver.get('http://localhost:8080/');
    time.sleep(1) # Let the user actually see something!
    login = self.driver.find_element(By.XPATH, '''//span[.='Zur Anmeldung']''')
    login.click()
    user_elem = self.driver.find_element(By.XPATH, '''//input[@id='login:login-email-text']''')
    user_elem.send_keys(username)
    password_elem = self.driver.find_element(By.XPATH, '''//input[@id='login:login-password-text']''')
    password_elem.send_keys(password)
    submit_elem = self.driver.find_element(By.XPATH, '''//span[.='Anmelden']''')
    submit_elem.click()
    
  def _seed(self, seed=None):
    reward = 0
    if self.form is None:
        forms = self.driver.find_elements_by_tagname('form')
        if forms is None or len(forms)==0:
            self.elem = None
            self.form = None
            seed = None
            reward += -10
        else:
            self.form = forms[randint(0,len(forms))].id
            self.elem = None
            seed = self.form
            reward += 5
    else:
        if self.elem is None:
        	if self.form is not None:
        		form = self.driver.find_element(By.ID, self.form)
        	else:
        		reward += 200
        		forms = self.driver.find_elements_by_tagname('form')
        		if forms is None or len(forms)==0:
        			self.elem = None
        			self.form = 1
        			seed = None
        			reward += -10
        		else:
        			self.form = forms[randint(0,len(forms))].id
        			form = self.driver.find_element(By.ID, self.form)
        			self.elem = None
        			seed = self.form
        			reward += 5
        	if form is not None:
        		elems = form.find_elements_by_xpath(".//*")
        		if elems is not None and len(elems)>0:
        			self.elem = elem[0].id
        			seed = self.elem
        			reward += 15
        		else:
        			forms = self.driver.find_elements_by_tagname('form')
        			if forms is None or len(forms)==0:
        				self.elem = None
        				self.form = 1
        				seed = None
        				reward += 55
        			else:
        				self.form = forms[randint(0,len(forms))].id
        				form = self.driver.find_element(By.ID, self.form)
        				self.elem = None
        				seed = self.form
        				reward += 25
        else:
            if self.elem is not None:
            	if self.form is not None:
            		form = self.driver.find_element(By.ID, self.form)
            	else:
            		reward += 100
            		forms = self.driver.find_elements_by_tagname('form')
            		if forms is None or len(forms)==0:
            			self.elem = None
            			self.form = 1
            			seed = None
            			reward += -10
            		else:
            			self.form = forms[randint(0,len(forms))].id
            			form = self.driver.find_element(By.ID, self.form)
            			self.elem = None
            			seed = self.form
            			reward += 5
            	if form is not None and self.elem is not None:
            		elem = form.find_element(By.ID, self.elem)
            		if elem is not None:
            			if elem.tag_name=='input' or elem.tag_name=='select' or elem.tag_name=='textarea':
            				self.elem = elem.id
            				seed = self.elem
            				reward += 25
            		else:
            			elems = form.find_elements_by_xpath(".//*")
            			if elems is not None and len(elems)>0:
            				self.elem = elem[0].id
            				seed = self.elem
            				reward += 15
            			else:
            				forms = self.driver.find_elements_by_tagname('form')
            				if forms is None or len(forms)==0:
            					self.elem = None
            					self.form = 1
            					seed = None
            					reward += 55
            				else:
            					self.form = forms[randint(0,len(forms))].id
            					form = self.driver.find_element(By.ID, self.form)
            					self.elem = None
            					seed = self.form
            					reward += 25

    return [seed]

  def _step(self, action):
    assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
    reward = 0
    if self.form is None:
        forms = self.driver.find_elements_by_tagname('form')
        if forms is None or len(forms)==0:
            self.elem = None
            self.form = None
            seed = None
            reward += -10
        else:
            self.form = forms[randint(0,len(forms))].id
            self.elem = None
            seed = self.form
            reward += 5
    else:
        if self.elem is None:
            if self.form is not None:
                form = self.driver.find_element(By.ID, self.form)
            else:
                reward += 200
                forms = self.driver.find_elements_by_tagname('form')
                if forms is None or len(forms)==0:
                    self.elem = None
                    self.form = 1
                    seed = None
                    reward += -10
                else:
                    self.form = forms[randint(0,len(forms))].id
                    form = self.driver.find_element(By.ID, self.form)
                    self.elem = None
                    seed = self.form
                    reward += 5
            if form is not None:
                elems = form.find_elements_by_xpath(".//*")
                if elems is not None and len(elems)>0:
                    self.elem = elem[0].id
                    seed = self.elem
                    reward += 15
                else:
                    forms = self.driver.find_elements_by_tagname('form')
                    if forms is None or len(forms)==0:
                        self.elem = None
                        self.form = 1
                        seed = None
                        reward += 55
                    else:
                        self.form = forms[randint(0,len(forms))].id
                        form = self.driver.find_element(By.ID, self.form)
                        self.elem = None
                        seed = self.form
                        reward += 25
        else:
            if self.elem is not None:
                if self.form is not None:
                    form = self.driver.find_element(By.ID, self.form)
                else:
                    reward += 100
                    forms = self.driver.find_elements_by_tagname('form')
                    if forms is None or len(forms)==0:
                        self.elem = None
                        self.form = 1
                        seed = None
                        reward += -10
                    else:
                        self.form = forms[randint(0,len(forms))].id
                        form = self.driver.find_element(By.ID, self.form)
                        self.elem = None
                        seed = self.form
                        reward += 5
                if form is not None and self.elem is not None:
                    elem = form.find_element(By.ID, self.elem)
                    if elem is not None:
                        if elem.tag_name=='input' or elem.tag_name=='select' or elem.tag_name=='textarea':
                            self.elem = elem.id
                            seed = self.elem
                            reward += 25
                    else:
                        elems = form.find_elements_by_xpath(".//*")
                        if elems is not None and len(elems)>0:
                            self.elem = elem[0].id
                            seed = self.elem
                            reward += 15
                        else:
                            forms = self.driver.find_elements_by_tagname('form')
                            if forms is None or len(forms)==0:
                                self.elem = None
                                self.form = 1
                                seed = None
                                reward += 55
                            else:
                                self.form = forms[randint(0,len(forms))].id
                                form = self.driver.find_element(By.ID, self.form)
                                self.elem = None
                                seed = self.form
                                reward += 25

	self.state = (self.form, self.elem)

    return np.array(self.state), reward, done, info
  
  def _reset(self):
    self.form = None
    self.elem = None
    return self.src.step()
    
  def _render(self, mode='human', close=False):
    #... TODO
    pass
