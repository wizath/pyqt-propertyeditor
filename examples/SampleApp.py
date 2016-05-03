from PyQt4 import QtGui
import sys

from PropertyEditor.PropertyEditorWidget import PropertyEditorWidget
from TestClass import TestClass


class SampleApp(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(SampleApp, self).__init__(parent)
        self.setWindowTitle("Property Editor")
        self.nodeEdit = PropertyEditorWidget()

        test_class = TestClass(self)
        self.nodeEdit.addObject(test_class)
        self.setCentralWidget(self.nodeEdit)
        self.show()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = SampleApp()
    window.show()
    sys.exit(app.exec_())
