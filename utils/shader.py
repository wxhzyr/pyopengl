from OpenGL.GL import shaders
from OpenGL.GL import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, glUseProgram, glGetAttribLocation
from OpenGL.GL import glEnableVertexAttribArray, glVertexAttribPointer, GL_FLOAT, GL_FALSE
from OpenGL import GL
from OpenGL.arrays import vbo

class Shader(object):
    vShader        = None # 顶点着色器
    fShader        = None # 片段着色器
    shaderProgram  = None # 一个着色器程序附加顶点，片段，几何（可选）着色器
    def __init__(self, vRoad, fRoad) -> None:
        vSrc = None
        fSrc = None
        with open(vRoad, 'r', encoding='utf-8') as file:
            vSrc = file.read()
        with open(fRoad, 'r', encoding='utf-8') as file:
            fSrc = file.read()
        self.vShader       = shaders.compileShader(vSrc, GL_VERTEX_SHADER)
        self.fShader       = shaders.compileShader(fSrc, GL_FRAGMENT_SHADER)
        self.shaderProgram = shaders.compileProgram(self.vShader, self.fShader)

    def bindDataToShader(self, name, Data: vbo.VBO):
        # 本函数只支持n个3维的32位的数据，更多的形式如n个1维或者其他的形式不被支持
        loc = glGetAttribLocation(self.shaderProgram, str(name))
        Data.bind()
        glVertexAttribPointer(loc, 3, GL_FLOAT, GL_FALSE, 3 * 4, Data)
        glEnableVertexAttribArray(loc)
        Data.unbind()

    def changeUniformData(self):
        # 修改uniform变量
        pass

    def use(self):
        glUseProgram(self.shaderProgram)
