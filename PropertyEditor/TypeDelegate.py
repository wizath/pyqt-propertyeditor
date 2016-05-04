from PyQt4 import QtCore, QtGui
from Property import Property


class TypeDelegate(QtGui.QItemDelegate):

    def __init__(self, parent = None):
        super(TypeDelegate, self).__init__(parent)
        self.boolProperties = {}

    def createEditor(self, parent, option, index):
        item = index.internalPointer()
        var = type(item.property())

        if var is int:
            editor = QtGui.QSpinBox(parent)
        elif var is float:
            editor = QtGui.QDoubleSpinBox(parent)
        elif var is str:
            editor = QtGui.QLineEdit(parent)
        elif isinstance(item, Property):
            editor = item.createEditor(parent, option, index)       

        return editor

    def setEditorData(self, editor, index):
        item = index.internalPointer()
        var = type(item.property())

        self.blockSignals(True)

        if var is int:
            editor.setValue(item.property())
        elif var is float:
            editor.setValue(item.property())
        elif var is str:
            editor.setText(item.property())
        elif isinstance(item, Property):
            item.setEditorData(editor, index)

        self.blockSignals(False)

    def setModelData(self, editor, model, index):
        item = index.internalPointer()
        var = type(item.property())
        
        if var is int:
            item.set_property(editor.value())
        elif var is float:
            item.set_property(editor.value())
        elif var is str:
            item.set_property(str(editor.text()))
        elif isinstance(item, Property):
            item.setModelData(editor, model, index)

    def boolHandler(self, painter, index):
        editor = QtGui.QCheckBox(self.parent())
        editor.setChecked(index.internalPointer().property())
        if not self.parent().indexWidget(index):
            self.parent().setIndexWidget(index, editor)
        editor.stateChanged.connect(self.currentValueChanged)

        # add to dict
        if not editor in self.boolProperties.keys():
            self.boolProperties[editor] = index

    def paint(self, painter, option, index):
        item = index.internalPointer()
        if type(item.property()) == bool and index.column() == 1:
            self.boolHandler(painter, index)
        else:
            super(TypeDelegate, self).paint(painter, option, index)

    def currentValueChanged(self):
        item = self.boolProperties[self.sender()].internalPointer()
        item.set_property(self.sender().isChecked())