from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5.QtOpenGL import *
import numpy as np
from PIL import Image

# implementing a custom openGl widget
class glWidget(QGLWidget):

    def __init__(self, parent):
        self.parent = parent
        QGLWidget.__init__(self, parent)
        self.setMinimumSize(100, 400)

        self.p = 0
        self.bar_height = 1.0
        self.bar_width = 0.6

    def initializeGL(self):

        # define vertices to be drawn
                    #  position coordinates                      # texture coordinates
        vertices = [[self.bar_width / 2, self.bar_height / 2, 0.0,      1.0, 1.0],
                    [self.bar_width / 2, -self.bar_height / 2, 0.0,     1.0, 0.0],
                    [-self.bar_width / 2, -self.bar_height / 2, 0.0,    0.0, 0.0],
                    [-self.bar_width / 2, self.bar_height / 2, 0.0,     0.0, 1.0]]

        indices = [[0, 1, 3],
                   [1, 2, 3]]


        # vertex shader code
        vertexShaderCode = """#version 420 core \n
                           layout (location = 0) in vec3 aPos;\n
                           layout (location = 1) in vec2 aTexCoord;\n
                           out float y_pos;\n
                           out vec2 TexCoord;\n
                           void main()\n
                           {\n
                               gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);\n
                               y_pos = aPos.y;\n
                               TexCoord = vec2(aTexCoord.x, aTexCoord.y);\n                    
                           }"""

        # fragment shader code
        fragmentShaderCode = """#version 420 core\n
                             out vec4 FragColor;\n
                             uniform float in_val; \n
                             in float y_pos; \n
                             in vec2 TexCoord;\n
                             uniform sampler2D in_texture;\n
                             void main()\n
                             {\n
                                if (y_pos < in_val)\n
                                    FragColor = texture(in_texture, TexCoord);\n
                                else\n
                                    FragColor = vec4(0.8f, 0.0f, 0.0f, 1.0f);\n
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

        # Bind the VAO first, then bind VBO and EBO and configure the vertex attributes
        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, 20 * 4, np.array(vertices, dtype=np.float32), GL_STATIC_DRAW)

        # add the EBO
        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, 6 * 4, np.array(indices, dtype=np.uint32), GL_STATIC_DRAW)

        # specify via VAO how the data in VBO should be used (vertex attributes)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 5 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # specify via VAO how the data in VBO should be used (texture attributes)
        # attribute for the texture data
        glVertexAttribPointer(1, 2, GL_FLOAT, False, 5 * 4, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        # unbind the VAO - not important right now because we have a single VAO
        # but will be important later on, once we have more than one OpenGL widget running
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        # load and create the texture
        glBindTexture(GL_TEXTURE_2D, 0)
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        # set up the texture wrapping methods
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        # set up the textures filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # load image
        im = Image.open("texture.png")
        width, height, img_data = im.size[0], im.size[1], im.tobytes("raw", "RGB", 0, -1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)


    def resizeGL(self, w: int, h: int) -> None:
        # override resizeGL method to handle screen resizing
        glViewport(0, 0, w, h)

    def paintGL(self):
        # override paintGL method to customize how to draw on screen
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # bind the texture before drawing
        glBindTexture(GL_TEXTURE_2D, self.texture)

        glUseProgram(self.shaderProgram)
        vertexColorLocation = glGetUniformLocation(self.shaderProgram, "in_val")
        glUniform1f(vertexColorLocation, self.p)
        glBindVertexArray(self.VAO)

        # draw the triangle
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        glBindVertexArray(0)
        glUseProgram(0)

    def setPercentVal(self, val: int) -> None:

        if val > 100:
            val = 100
        elif val < 0:
            val = 0

        self.p = self.bar_height * val / 100.0 - (self.bar_height / 2)











