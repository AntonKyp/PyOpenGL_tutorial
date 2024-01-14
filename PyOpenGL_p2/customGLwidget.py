from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5.QtOpenGL import *
import numpy as np

# implementing a custom openGl widget
class glWidget(QGLWidget):

    def __init__(self, parent):
        self.parent = parent
        QGLWidget.__init__(self, parent)
        self.setMinimumSize(400, 400)

    def initializeGL(self):

        # define vertices to be drawn
        vertices = [[-0.5, -0.5, 0.0],
                    [0.5, -0.5, 0.0],
                    [0.0, 0.5, 0.0]]

        # vertex shader code
        vertexShaderCode = """#version 420 core \n
                           layout (location = 0) in vec3 aPos;\n
                           void main()\n
                           {\n
                               gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);\n
                           }"""

        # fragment shader code
        fragmentShaderCode = """#version 420 core\n
                             out vec4 FragColor;\n
                             void main()\n
                             {\n
                                 FragColor = vec4(0.7f, 0.0f, 0.0f, 1.0f);\n
                            }"""

        # compiling the shaders
        vertexShader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertexShader, vertexShaderCode)
        glCompileShader(vertexShader)

        if not glGetShaderiv(vertexShader, GL_COMPILE_STATUS, None):
            print("vertexShader compilation failed")

        fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragmentShader, fragmentShaderCode)
        glCompileShader(fragmentShader)

        if not glGetShaderiv(fragmentShader, GL_COMPILE_STATUS, None):
            print("fragmentShader compilation failed")

        # build the shader program
        self.shaderProgram = glCreateProgram()
        glAttachShader(self.shaderProgram, vertexShader)
        glAttachShader(self.shaderProgram, fragmentShader)
        glLinkProgram(self.shaderProgram)

        # check shader program status
        if glGetProgramiv(self.shaderProgram, GL_LINK_STATUS, None) == GL_FALSE:
            print("Shader program build failed")

        # define VAO and VBO and draw the triangle
        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        # Bind the VAO firsr, then bind VBO and configure the vertex attributes
        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)

        # specify via VAO how the data in VBO should be used (vertex attributes)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 3 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # send vertex data to the GPU via a vertex buffer object
        glBufferData(GL_ARRAY_BUFFER, 9 * 4, np.array(vertices, dtype=np.float32), GL_STATIC_DRAW)

        # unbind the VAO - not important right now because we have a single VAO
        # but will be important later on, once we have more than one OpenGL widget running
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def resizeGL(self, w: int, h: int) -> None:
        # override resizeGL method to handle screen resizing
        glViewport(0, 0, w, h)

    def paintGL(self):
        # override paintGL method to customize how to draw on screen
        glClearColor(0.0, 0.0, 0.5, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(self.shaderProgram)
        glBindVertexArray(self.VAO)

        # draw the triangle
        glDrawArrays(GL_TRIANGLES, 0, 3)

        glBindVertexArray(0)
        glUseProgram(0)

