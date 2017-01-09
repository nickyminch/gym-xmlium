from xmlium.envs.xmliumob import XmliumOb

class XmliumAction:
    def __init__(self, action, xmliumob):
        self.action = action
        self.xmliumob = xmliumob
    @property
    def action(self):
        return self.__action
    @action.setter
    def action(self, action):
        self.__action = action
    @property
    def xmliumob(self):
        return self.__xmliumob
    @xmliumob.setter
    def xmliumob(self, xmliumob):
        self.__xmliumob = xmliumob
