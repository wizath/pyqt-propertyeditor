from PyQt4 import QtCore, QtGui
from Property import *


class PropertyModel(QtCore.QAbstractItemModel):

    def __init__(self, parent = None, customProperties = {}):
        super(PropertyModel, self).__init__(parent)
        self._rootNode = Property('Root', None, None)

        self.customProperties = customProperties

    def getRoot(self):
        return self._rootNode

    def rowCount(self, parent):
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()

    def columnCount(self, parent):
        return 2

    def data(self, index, role):
        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 0:
                return node.name()
            else:
                return node.property()

        if role == QtCore.Qt.DecorationRole and index.column() == 1:
            if type(node.property()) == QtGui.QColor:
                pixmap = QtGui.QPixmap(26,26)
                pixmap.fill(node.property())

                icon = QtGui.QIcon(pixmap)
                return icon

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return 'Name'
            else:
                return 'Value'

    def flags(self, index):
        if index.column() == 0:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        else:
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable

    def index(self, row, column, parent):
        parentNode = self.getNode(parent)
        childItem = parentNode.child(row)

        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        node = self.getNode(index)
        parentNode = node.parent()

        if parentNode == self._rootNode:
            return QtCore.QModelIndex()

        return self.createIndex(parentNode.row(), 0, parentNode)

    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node

        return self._rootNode

    def addItem(self, propertyObject):
        properties = vars(propertyObject)
        length = len(properties)
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(self._rootNode), self.rowCount(self._rootNode))

        for key, value in properties.items():
            var = type(value)

            if var in self.customProperties.keys():
                prop = self.customProperties[var]
                try:
                    childNode = prop(key, value, self.getRoot())
                except:
                    print 'Error in custom property'''
            else:
                childNode = Property(key, value, self.getRoot())

        self.endInsertColumns()

    def clear(self):
        self.beginRemoveRows(QtCore.QModelIndex(), 0, self.rowCount(self._rootNode))
        self._rootNode = Property('Root', None, self)
        self.endRemoveRows()

    def registerCustom(self, propKey, propVal):
        self.customProperties[propKey] = propVal

    def unregisterCustom(self, propKey):
        if propKey in self.customProperties.keys():
            del self.customProperties[propKey]