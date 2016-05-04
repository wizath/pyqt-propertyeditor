import weakref


class Property(object):
    """ Class that holds the (weak) reference to the parent object and name of property
        that we want to manage."""

    def __init__(self, name, obj=None, parent=None):
        self._name = name
        if obj is not None:
            self._ref = weakref.ref(obj)
        self._parent = parent
        self._children = []

        if parent is not None:
            parent.addChild(self)

    def isValid(self):
        return False

    def addChild(self, child):
        self._children.append(child)

    def name(self):
        return self._name

    def property(self):
        return getattr(self._ref(), self._name)

    def set_property(self, value):
        setattr(self._ref(), self._name, value)

    def childCount(self):
        return len(self._children)

    def child(self, row=None):
        if row is not None:
            return self._children[row]
        else:
            return  self._children

    def parent(self):
        return self._parent

    def row(self):
        if self._parent is not None:
            return self.parent().child().index(self)

    def createEditor(self, parent, option, index):
        raise NotImplementedError

    def setEditorData(self, editor, data):
        raise NotImplementedError

    def editorData(self, editor):
        raise NotImplementedError
