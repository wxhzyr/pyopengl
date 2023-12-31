"""最简单的着色器程序"""

from time import sleep
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
from OpenGL.GL import shaders
from utils.shader import Shader
from utils.camera import Camera
import pyrr

VERTICES = None
COLORS = None
myShader = None
indices = vbo.VBO(np.array([0, 1, 2], dtype=np.uint32), target=GL_ELEMENT_ARRAY_BUFFER)
myCamera = Camera(pyrr.Vector3([0.0, 0.0, 3.0]))
width = 600
height = 400
curPosx = width / 2
curPosy = height / 2
delTime = 0.1
curTime = 0.0
def prepare():
    """准备模型数据"""
    global myShader, VERTICES, COLORS
    myShader = Shader(r"shaders/posAndColor.vs", r"shaders/posAndColor.fs")
    VERTICES = vbo.VBO(np.array([[0, 1, 0], [-1, -1, 0], [1, -1, 0]], dtype=np.float32))
    COLORS = vbo.VBO(np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float32))

def draw():
    """绘制模型"""
    global delTime, curTime
    delTime = glutGet(GLUT_ELAPSED_TIME) - curTime
    delTime = delTime / 1000
    curTime = glutGet(GLUT_ELAPSED_TIME)  
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)        # 清除缓冲区
    myShader.use()
    myShader.bindDataToShader('a_Position', VERTICES)
    myShader.bindDataToShader('a_Color', COLORS)
    model = pyrr.matrix44.create_identity()
    view  = myCamera.getViewMatrix()
    projection = pyrr.matrix44.create_perspective_projection_matrix(myCamera.zoom, width / height, 0.1, 100)
    myShader.setMatrix4('model', model)
    myShader.setMatrix4('view', view)
    myShader.setMatrix4('projection', projection)
    with indices:
        glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, indices)
    print(f"fps is {1 / delTime}")
    glUseProgram(0)
    glutSwapBuffers()
    # glFlush() # 清空缓冲区指令（改为双缓冲写法）

def click(btn, state, x, y):
    """鼠标按键和滚轮事件函数"""
    # button：表示鼠标操作的是左键(GLUT_LEFT_BUTTON)、中键(GLUT_MIDDLE_BUTTON)、右键(GLUT_RIGHT_BUTTON)，也可分别用整数0、1、2表示。
    # state:表示鼠标按键状态，包括按下(GLUT_DOWN)和抬起(GLUT_UP)，也可分别用整数0和1表示
    # x,y：表示鼠标的坐标位置，注意这里的x和y是以左上角为原点，向右为x正向，向下为y正向
    # 但糟糕的是，opengl绘制是以左下角为原点，相当于y轴偏转，在做pick时要注意
    if (btn == 0 or btn == 2) and state == 0: # 左键或右键被按下
        print(x, y) # 输出鼠标位置

    # glutPostRedisplay() # 更新显示

def drag(x, y):
    """鼠标拖拽事件函数"""

    global curPosx, curPosy
    dx, dy = x - curPosx, curPosy - y
    curPosx = x
    curPosy = y
    mode = glutGetModifiers()
    if mode == GLUT_ACTIVE_SHIFT:
        myCamera.processMouseMovement(dx, dy)
        # glutPostRedisplay() # 更新显示

def reshape(w, h):
    """改变窗口大小事件函数"""

    global width, height    
    width = w
    height = h
    # csize = (w, h) # 保存窗口大小
    # aspect = w/h if h > 0 else 1e4 # 更新窗口宽高比
    glViewport(0, 0, width, height) # 设置视口
    # glutPostRedisplay() # 更新显示

def keyProcess(c, x, y):
    if c == b'\x1b':
        glutLeaveMainLoop()
    elif c == b'w':
        myCamera.processKeyMomvement("forward", delTime)
    elif c == b's':
        myCamera.processKeyMomvement('backward', delTime)
    elif c == b'a':
        myCamera.processKeyMomvement('left', delTime)
    elif c == b'd':
        myCamera.processKeyMomvement('right', delTime)
    elif c == b'q':
        myCamera.processKeyMomvement('up', delTime)
    elif c == b'e':
        myCamera.processKeyMomvement('down', delTime)
    # glutSwapBuffers()
    # glutPostRedisplay() # 更新显示

def special():
    draw()
    sleep(5 / 1000)

if __name__ == "__main__":
    glutInit()                          # 1. 初始化glut库
    glutInitWindowSize(width, height)   # 2. 初始化窗口大小
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutCreateWindow('bj_sim_heart')    # 3. 创建glut窗口
    prepare()                           # 4. 生成着色器程序、顶点数据集、颜色数据集
    glutReshapeFunc(reshape)            # 6. 绑定窗口大小改变事件函数
    glutMouseFunc(click)                # 7. 绑定鼠标按键
    glutPassiveMotionFunc(drag)         # 8. 绑定鼠标（无点击）移动函数
    glutKeyboardFunc(keyProcess)        # 9. 响应键盘事件
    glutDisplayFunc(draw)               # 5. 绑定模型绘制函数
    glutIdleFunc(special)
    glutMainLoop()                      # 10. 进入glut主循环
