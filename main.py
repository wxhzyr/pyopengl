"""最简单的着色器程序"""

import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
from OpenGL.GL import shaders
from utils.shader import Shader

VERTICES = None
COLORS = None
myShader = None
indices = vbo.VBO(np.array([0, 1, 2], dtype=np.uint32), target=GL_ELEMENT_ARRAY_BUFFER)
def prepare():
    """准备模型数据"""
    global myShader, VERTICES, COLORS
    myShader = Shader(r"shaders/posAndColor.vs", r"shaders/posAndColor.fs")
    VERTICES = vbo.VBO(np.array([[0, 1, 0], [-1, -1, 0], [1, -1, 0]], dtype=np.float32))
    COLORS = vbo.VBO(np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float32))

def draw():
    """绘制模型"""

    glClear(GL_COLOR_BUFFER_BIT)        # 清除缓冲区
    myShader.use()
    myShader.bindDataToShader('a_Position', VERTICES)
    myShader.bindDataToShader('a_Color', COLORS)
    with indices:
        glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, indices)
    glUseProgram(0)
    glFlush() # 执行缓冲区指令

if __name__ == "__main__":
    glutInit()                          # 1. 初始化glut库
    glutCreateWindow('OpenGL Demo')     # 2. 创建glut窗口
    prepare()                           # 3. 生成着色器程序、顶点数据集、颜色数据集
    glutDisplayFunc(draw)               # 4. 绑定模型绘制函数
    glutMainLoop()                      # 5. 进入glut主循环
