from PyQt4 import QtGui
import sys

from PropertyEditor.PropertyEditorWidget import PropertyEditorWidget
from TestClass import TestClass


class SampleApp(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(SampleApp, self).__init__(parent)
        self.setWindowTitle("Property Editor")

        self.widget = QtGui.QWidget()
        self.layout = QtGui.QVBoxLayout()
        self.widget.setLayout(self.layout)

        self.nodeEdit = PropertyEditorWidget()

        self.button = QtGui.QPushButton("Print")

        self.test_class = TestClass(self)
        self.button.clicked.connect(self.get_dict)

        self.nodeEdit.addObject(self.test_class)

        self.layout.addWidget(self.nodeEdit)
        self.layout.addWidget(self.button)

        self.setCentralWidget(self.widget)
        self.show()

    def get_dict(self):
        print self.test_class.__dict__


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = SampleApp()
    window.show()
    sys.exit(app.exec_())
