import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore
from customGLwidget import *

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Custom GL app")
        self.resize(600, 600)

        # add out custom pyOpenGL widget to the window
        # define opengl version used and using opengl core-profile
        self.gl = glWidget(self)
        self.gl.format().setVersion(4, 2)
        self.gl.format().setProfile(QGLFormat.CoreProfile)

        # Set the central widget of the Window.
        self.setCentralWidget(self.gl)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()