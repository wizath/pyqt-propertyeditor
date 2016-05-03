from PyQt4 import QtCore, QtGui
from Property import Property

# TODO add metaclass with auto-property registering for easier use
# TODO format with PEP8


class ListProperty(Property):

    def __init__(self, name, propertyList, parent = None):
        super(ListProperty, self).__init__(name, None, parent)
        self._list = []
        for i, item in enumerate(propertyList):
            self._list.append(Property(str(i), item, self))


class ColorProperty(Property):

    def __init__(self, name, property, parent = None):
        super(ColorProperty, self).__init__(name, property, parent)

    def createEditor(self, parent, option, index):
        editor = QtGui.QComboBox(parent)
        editor.currentIndexChanged.connect(editor.clearFocus)

        colorNames = QtGui.QColor().colorNames()

        for i in range(len(colorNames)):
            color = QtGui.QColor(colorNames[i])
            editor.insertItem(i, colorNames[i])
            editor.setItemData(i, color, QtCore.Qt.DecorationRole)

        return editor

    def setEditorData(self, editor, data):
        color = data.internalPointer().property()
        editor.setCurrentIndex(editor.findData(color, QtCore.Qt.DecorationRole))
        if editor.currentIndex() == -1:
            editor.addItem(color.name())
            editor.setItemData(editor.count() - 1, color, QtCore.Qt.DecorationRole)
            editor.setCurrentIndex(editor.count() - 1)

    def setModelData(self, editor, model, index):
        item = index.internalPointer()
        color = editor.itemData(editor.currentIndex(), QtCore.Qt.DecorationRole).toPyObject() 

        item.setProperty(color)


class DictProperty(Property):

    def __init__(self, name, propertyDict, parent = None):
        super(DictProperty, self).__init__(name, None, parent)

        for i, j in propertyDict.items():
            parent = Property(str(i), j, self)