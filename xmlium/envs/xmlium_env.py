from time import sleep
import gym
from universe.spaces import vnc_event
import dogtail.utils
from dogtail.tree import Application
import numpy as np
from universe.spaces import VNCActionSpace
from universe.wrappers import BlockingReset


class XmliumEnv(BlockingReset):
    metadata = {'render.modes': ['human']}
    
    def __init__(self):
        super(XmliumEnv, self).__init__()
        self.action_space = VNCActionSpace()
        self.safe_action_space = self.action_space
        dogtail.config.config.logDebugToStdOut = True
        dogtail.config.config.logDebugToFile = False
    

    def _isEditable(self):
        if self.elem.roleName=='entry' or self.elem.roleName=='text':
            return True
        else:
            return False
    def _isClickable(self):
        if self.elem.roleName=='combo box'or self.elem.roleName=='link' or self.elem.roleName=='menu item':
            return True
        else:
            return False
    def _step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        if self.action_space.contains(action):
            for a in action:
                if isinstance(a, vnc_event.KeyEvent):
                    if self.elem is None:
                        return (), -100, False, ()
                    elif self.isEditable():
                        return (), 100, False, ()
                    else:
                        return (), -1000, False, ()
                elif isinstance(a, vnc_event.PointerEvent):
                    self.elem = None
                    self.elem = self.app.getChildAtPoint(a.x, a.y)
                    if self.elem is None:
                        return (), -100, False, ()
                    elif self.isClickable():
                        return (), 100, False, ()
                    else:
                        return (), -1000, False, ()
    
        return (), 100000, False, ()
  
    def _reset(self):
        self.elem = None

        username='kawaman@mail.bg'
        password = 'niki1234'
        self.pid = dogtail.utils.run('firefox http://http://jens-stahl-dev.de/views/login.xhtml')
        self.app = Application('Firefox')
        tree = self.app.child(name='Weltportfolio', roleName='document frame')
        tree.child(name='E-Mail*', roleName='entry').typeText(username)
        tree.child(name='Passwort*', roleName='entry').typeText(password)
        tree.child(name=' Anmelden', roleName='push button').doActionNamed('click')
         
        sleep(0.5)
       
        return self.step()
      
    def _render(self, mode='human', close=False):
        #... TODO
        pass
