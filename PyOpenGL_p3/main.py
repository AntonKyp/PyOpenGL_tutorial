import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from customGLwidget import *

# custom widget to be set as the main window central widget
class customWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.file_open = False

        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        gl_layout = QHBoxLayout()

        # create two buttons
        btn1 = QPushButton("Open File")
        btn1.pressed.connect(self.openFile)
        btn2 = QPushButton("Play")
        btn2.pressed.connect(self.play)

        button_layout.addStretch()
        button_layout.addWidget(btn1)
        button_layout.addWidget(btn2)
        button_layout.addStretch()

        # create two OpenGL widgets
        self.gl1 = glWidget(self)
        self.gl1.format().setVersion(4, 2)
        self.gl1.format().setProfile(QGLFormat.CoreProfile)

        self.gl2 = glWidget(self)
        self.gl2.format().setVersion(4, 2)
        self.gl2.format().setProfile(QGLFormat.CoreProfile)

        gl_layout.addWidget(self.gl1)
        gl_layout.addWidget(self.gl2)

        # add a timer to refresh the openGL widgets
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateGLWidgets)
        self.timer.setInterval(100)  # arbitrarly set to 100[ms]

        main_layout.addLayout(button_layout)
        main_layout.addLayout(gl_layout)

        self.setLayout(main_layout)

    def updateGLWidgets(self):

        line = self.file.readline()
        if line != "":
            vals = line.split(",")
            self.gl1.setPercentVal(int(vals[0]))
            self.gl2.setPercentVal(int(vals[1]))
            self.gl1.update()
            self.gl2.update()
        else:
            self.timer.stop()

    def openFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "data files (*.csv)")
        self.file = open(fname[0], 'r')
        self.file_open = True

    def play(self):
        if self.file_open:
            self.timer.start()

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Custom GL app")
        self.resize(600, 600)

        self.widget = customWidget()
        self.setCentralWidget(self.widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()