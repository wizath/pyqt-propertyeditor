import sys
from PyQt4 import QtCore, QtGui

# TODO chagnge the way of accessing the properties with getattr's and setattr's


class Property(object):

    def __init__(self, name, propertyObject, parent = None):
        self._name = name
        self._property = propertyObject
        self._parent = parent
        self._children = []

        if parent is not None:
            parent.addChild(self)

    def isValid(self):
        return False

    def addChild(self, child):
        self._children.append(child)

    def insertChild(self, position, child):
        if position < 0 or position > self.childCount():
            return False

        self._children.insert(position, child)
        child.setParent(self)

        return True

    def setParent(self, parent):
        self._parent = parent

    def name(self):
        return self._name

    def property(self):
        return self._property

    def setProperty(self, value):
        self._property = value

    def childCount(self):
        return len(self._children)

    def child(self, row):
        return self._children[row]

    def parent(self):
        return self._parent

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)

    def createEditor(self, parent, option, index):
        print 'Not implemented'
        return None

    def setEditorData(self, editor, data):
        print 'Not implemented'
        return None

    def editorData(self, editor):
        print 'Not implemented'
        return None