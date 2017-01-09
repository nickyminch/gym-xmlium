class XmliumOb:
    def __init__(self, elemType, form, element):
        self.elemType = elemType
        self.form = form
        self.element = element
    @property
    def elemType(self):
        return self.__elemType

    @elemType.setter
    def elemType(self, elemType):
        self.__elemType = elemType
        
    @property
    def form(self):
        return self.__form

    @form.setter
    def form(self, form):
        self.__form = form
    @property
    def element(self):
        return self.__element

    @element.setter
    def element(self, element):
        self.__element = element
