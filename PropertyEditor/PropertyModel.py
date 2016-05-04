from Property import Property
from PyQt4 import QtCore, QtGui

# todo add property filter that can edit only selected values


class PropertyModel(QtCore.QAbstractItemModel):
    """ Class that creates an Qt model to the MVC so properties can be changed and
        accessed by the GUI widget. """

    def __init__(self, parent=None):
        super(PropertyModel, self).__init__(parent)
        self._root = Property('Root', None, None)
        self._items = []

    def get_root(self):
        return self._root

    def rowCount(self, parent):
        if not parent.isValid():
            parent_node = self._root
        else:
            parent_node = parent.internalPointer()

        return parent_node.childCount()

    def columnCount(self, parent):
        """ Need only 2 columns. One for name and second for value."""
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
                pixmap = QtGui.QPixmap(26, 26)
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
        parent_node = self.getNode(parent)
        child_node = parent_node.child(row)

        if child_node is not None:
            return self.createIndex(row, column, child_node)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        node = self.getNode(index)
        parent_node = node.parent()

        if parent_node == self._root:
            return QtCore.QModelIndex()

        return self.createIndex(parent_node.row(), 0, parent_node)

    def getNode(self, index):
        if index.isValid():
            return index.internalPointer()

        return self._root

    def add_property_object(self, obj):
        properties = vars(obj)
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(self._root), self.rowCount(self._root))

        for key, value in properties.items():
            self._items.append(Property(key, obj, self.get_root()))

        self.endInsertRows()

    def clear(self):
        self.beginRemoveRows(QtCore.QModelIndex(), 0, self.rowCount(self._rootNode))
        self._root = Property('Root', None, self)
        self._items = []
        self.endRemoveRows()
