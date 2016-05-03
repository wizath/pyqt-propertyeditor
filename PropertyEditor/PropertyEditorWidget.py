from PyQt4 import QtCore, QtGui
from PropertyModel import PropertyModel
from TypeDelegate import TypeDelegate
from CustomProperties import *


class PropertyEditorWidget(QtGui.QTreeView):

    def __init__(self, parent = None):
        super(PropertyEditorWidget, self).__init__(parent)
        self._model = PropertyModel(self)
        self.setModel(self._model)
        self.setItemDelegate(TypeDelegate(self))

        self.registerCustom(list, ListProperty)
        self.registerCustom(QtGui.QColor, ColorProperty)
        self.registerCustom(dict, DictProperty)

    def addObject(self, propertyObject):
        self._model.addItem(propertyObject)
        self.expandToDepth(0)

    def setObject(self, propertyObject):
        self._model.clear()
        if propertyObject:
            self._model.addItem(propertyObject)
        self.expandToDepth(0)

    def registerCustom(self, propKey, propVal):
        self._model.registerCustom(propKey, propVal)

    def unregisterCustom(self, propKey):
        self._model.unregisterCustom(propKey)