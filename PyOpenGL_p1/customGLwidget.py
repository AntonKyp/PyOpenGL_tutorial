from OpenGL.GL import *
from PyQt5.QtOpenGL import *

# implementing a custom openGL widget
class glWidget(QGLWidget):

    def __init__(self, parent):
        self.parent = parent
        QGLWidget.__init__(self, parent)

    def initializeGL(self) -> None:
        pass

    def resizeGL(self, w: int, h: int) -> None:
        # override resizeGL method to handle screen resizing
        glViewport(0, 0, w, h)

    def paintGL(self) -> None:
        # override paintGL method to customize how to draw on screen
        glClearColor(0.0, 0.0, 0.5, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

