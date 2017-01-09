import time
from universe.wrappers import BlockingReset
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException, StaleElementReferenceException, WebDriverException, TimeoutException
from xmlium.envs.xmliumob import XmliumOb
from xmlium.envs.xmliumaction import XmliumAction
import string

class XmliumEnv(BlockingReset):
    metadata = {'render.modes': ['human']}
    def __init__(self):
        pass
    
    @property
    def driver(self):
        return self.__driver

    @driver.setter
    def driver(self, driver):
        self.__driver = driver
    @property
    def wait(self):
        return self.__wait

    @wait.setter
    def wait(self, wait):
        self.__wait = wait
    def _configure(self, display=None):
        pass
    def _step(self, action):
        #assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
    
        return self.get_observations(action)
  
    def _reset(self):
        print("reseting................................")
        self.observation_space = None
        self.action_space = None
        self.action = None
        observation, reward, done, info = self.get_observations()
        return observation
      
    def render(self, mode='human', close=False):
        #... TODO
        pass
    def get_observations(self, action=None):
        reward = 0;
        done = False
        info = None
        if self.observation_space is None:
            forms = self.driver.find_elements_by_tag_name('form')
            self.observation_space = []
            self.action_space = []
            forms_new = []
            for form in forms:
                form_id = form.get_attribute("id")
                if form.is_displayed() and form_id is not None and len(form_id)>0:
                    length = 0
                    elems = form.find_elements_by_xpath(".//*")
                    for elem in elems:
                        id = elem.get_attribute("id")
                        if elem.is_displayed() and id is not None and len(id)>0:
                            length = length+1
                            break
                    if length>0:
                        forms_new.append(form_id)
            index = 0
            for form1 in forms_new:
                self.action_space.append([])
                form = self.driver.find_element(By.ID, form1)
                elems = form.find_elements_by_xpath(".//*")
                elems_new = []
                for elem in elems:
                    elem_id = elem.get_attribute("id")
                    displayed = False
                    try:
                        displayed = elem.is_displayed()
                    except WebDriverException:
                        print(elem)
                    if displayed and elem_id is not None and len(elem_id)>0:
                        elems_new.append(elem_id)
                
                str = string.printable
                index2 = 0
                for elem1 in elems_new:
                    self.action_space[index].append([])
                    elem = self.driver.find_element(By.ID, elem1)
                    tag_name = elem.tag_name
                    if tag_name=="input":
                        elem_type = elem.get_attribute("type")
                        xo = XmliumOb(3, form1, elem1)
                        if elem_type!="text":
                            self.observation_space.append(xo)
                            self.action_space[index][index2].append(XmliumAction("click", xo))
                        else:
                            xo2 = XmliumOb(5, form1, elem1)
                            self.observation_space.append(xo2)
                            index3 = 0
                            
                            for char in str:
                                self.action_space[index][index2].append(XmliumAction(char, xo2))
                                index3 = index3+1
                                if index3%10==0:
                                    self.action_space[index][index2].append(XmliumAction("click", xo))
                            self.action_space[index][index2].append(XmliumAction(13, xo2))
                    elif tag_name=="textarea":
                        xo2 = XmliumOb(5, form1, elem1)
                        self.observation_space.append(xo2)
                        for char in str:
                            self.action_space[index][index2].append(XmliumAction(char, xo2))
                        self.action_space[index][index2].append(XmliumAction(13, xo2))
                    else:
                        xo2 = XmliumOb(5, form1, elem1)
                        self.observation_space.append(xo2)
                        for char in range(0, 46):
                            self.action_space[index][index2].append(XmliumAction(char, xo2))
                        xo = XmliumOb(3, form1, elem1)
                        self.observation_space.append(xo)
                        self.action_space[index][index2].append(XmliumAction("click", xo))
                    index2 = index2+1

                    #self.action_space.append(XmliumAction(index, elems_new, xo))
                index = index+1
        else:
            if type(action) is XmliumAction:
                reward=1
                xmliumob = action.xmliumob
                if xmliumob.elemType == 3:
                    reward = reward+5
                    if action.action == "click":

                        id = action.xmliumob.element
                        elem = self.driver.find_element(By.ID, id)
                        try:
                            elem.click()
                            time.sleep(0.4)
                        except ElementNotVisibleException:
                            print(elem.tag_name)
                            return self.reset(), 0, True, None
                        except StaleElementReferenceException:
                            print(self.action_space);
                        self.reset()
                        info = True
                elif xmliumob.elemType == 5:
                    id = action.xmliumob.element
                    elem = self.driver.find_element(By.ID, id)
                    elem.send_keys(action.action)
            else:
                print("%r (%s) invalid"%(action, type(action)))
                raise TypeError
        try:
            self.wait.until(EC.presence_of_element_located( (By.XPATH,"//li[contains(@class,'infoMessage') or contains(@class,'errorMessage')]") ))
            reward = reward+131
        except TimeoutException:
            pass
        #print(self.action_space);
        return self.observation_space, reward, done, info
