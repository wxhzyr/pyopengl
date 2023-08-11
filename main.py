"""最简单的着色器程序"""
import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
from utils.shader import Shader
from utils.camera import Camera
from utils.offScreen import OffScreen
import pyrr
# windos参数
width = 1280
height = 720
# 绘制数据
VERTICES = None
COLORS   = None
INDEX    = None
indices = vbo.VBO(np.array([0, 1, 2], dtype=np.uint32), target=GL_ELEMENT_ARRAY_BUFFER)
n = 0
# 着色器程序
drawShader = None 
pickShader = None 
# 离屏渲染程序
pickOffScreen = None
# 摄像头类
myCamera = Camera(pyrr.Vector3([0.0, 0.0, 3.0]))
curPosx = width / 2
curPosy = height / 2
# 计算FPS的参数
delTime = 0.1
curTime = 0.0

def prepare():
    """准备模型数据"""
    global VERTICES, COLORS, INDEX, drawShader, pickShader, pickOffScreen, n
    vertices = np.array([[0, 1, 0], [-1, -1, 0], [1, -1, 0]], dtype=np.float32)
    n = vertices.shape[0]
    VERTICES = vbo.VBO(vertices)
    COLORS = vbo.VBO(np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float32))
    INDEX = vbo.VBO(np.array([1.0, 2.0, 3.0], dtype=np.float32))
    drawShader = Shader(r"shaders/posAndColor.vs", r"shaders/posAndColor.fs")
    pickShader = Shader(r"shaders/pickTexture.vs", r"shaders/pickTexture.fs")
    pickOffScreen = OffScreen(width, height)

def pickRender():
    pickOffScreen.enableOffRender()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    pickShader.use()
    pickShader.bindDataToShader('aPos', VERTICES)
    pickShader.bindIndexToShader('vId', INDEX)
    model = pyrr.matrix44.create_identity()
    view  = myCamera.getViewMatrix()
    projection = pyrr.matrix44.create_perspective_projection_matrix(myCamera.zoom, width / height, 0.1, 100)
    pickShader.setMatrix4('model', model)
    pickShader.setMatrix4('view', view)
    pickShader.setMatrix4('projection', projection)
    pickShader.setFloat('rate', n + 1)
    with indices:
        glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, indices) 
    pickOffScreen.disableOffRender()

def draw():
    """绘制模型"""
    global delTime, curTime
    delTime = glutGet(GLUT_ELAPSED_TIME) - curTime
    delTime = delTime / 1000
    curTime = glutGet(GLUT_ELAPSED_TIME) 
    camearUpdate()
    pickRender()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)        # 清除缓冲区
    drawShader.use()
    drawShader.bindDataToShader('a_Position', VERTICES)
    drawShader.bindDataToShader('a_Color', COLORS)
    model = pyrr.matrix44.create_identity()
    view  = myCamera.getViewMatrix()
    projection = pyrr.matrix44.create_perspective_projection_matrix(myCamera.zoom, width / height, 0.1, 100)
    drawShader.setMatrix4('model', model)
    drawShader.setMatrix4('view', view)
    drawShader.setMatrix4('projection', projection)
    with indices:
        glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, indices) 
    # print(f"fps is {1 / delTime}")
    glUseProgram(0)

def click(window, button, action, mods):
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS: 
        data = pickOffScreen.readPixel(curPosx, height - curPosy - 1)
        print(data * (n + 1))
    elif button == glfw.MOUSE_BUTTON_LEFT and action == glfw.RELEASE:
        pass

def drag(window, x, y):
    """鼠标拖拽事件函数"""

    global curPosx, curPosy
    myCamera.xOffset, myCamera.yOffset = x - curPosx, curPosy - y
    curPosx = x
    curPosy = y
    if glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
        myCamera.needUpdate = True
        # myCamera.processMouseMovement(dx, dy)
        # glutPostRedisplay() # 更新显示

def reshape(window, w, h):
    """改变窗口大小事件函数"""

    global width, height    
    width = w
    height = h
    glViewport(0, 0, width, height) # 设置视口
    pickOffScreen.resize(w, h)

def keyProcess(window, key, scancode, action, mode):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key == glfw.KEY_W and action == glfw.PRESS:
        myCamera.moveForward = True
    elif key == glfw.KEY_W and action == glfw.RELEASE:
        myCamera.moveForward = False
    if key == glfw.KEY_S and action == glfw.PRESS:
        myCamera.moveBackward = True
    elif key == glfw.KEY_S and action == glfw.RELEASE:
        myCamera.moveBackward = False
    if key == glfw.KEY_A and action == glfw.PRESS:
        myCamera.moveLeft = True
    elif key == glfw.KEY_A and action == glfw.RELEASE:
        myCamera.moveLeft = False
    if key == glfw.KEY_D and action == glfw.PRESS:
        myCamera.moveRight = True
    elif key == glfw.KEY_D and action == glfw.RELEASE:
        myCamera.moveRight = False
    if key == glfw.KEY_Q and action == glfw.PRESS:
        myCamera.moveUp = True
    elif key == glfw.KEY_Q and action == glfw.RELEASE:
        myCamera.moveUp = False
    if key == glfw.KEY_E and action == glfw.PRESS:
        myCamera.moveDown = True
    elif key == glfw.KEY_E and action == glfw.RELEASE:
        myCamera.moveDown = False

def camearUpdate():
    myCamera.processKeyMomvement(delTime)
    myCamera.processMouseMovement()
        

if __name__ == "__main__":
    glfw.init()                                                         # 1. 初始化glfw
    window = glfw.create_window(width, height, "bj_sim_heart", None, None)  # 2. 创建glfwwindow
    glfw.set_window_pos(window, 400, 200)                               # 3. 设置windows窗口位置
    glfw.set_window_size_callback(window, reshape)                      # 4. 提供回调函数
    glfw.set_cursor_pos_callback(window, drag)
    glfw.set_key_callback(window, keyProcess)
    glfw.set_mouse_button_callback(window, click)
    glfw.make_context_current(window)                                   # 5. 将输出绑定到当前windows
    prepare()                                                           # 6. 准备数据
    while not glfw.window_should_close(window):                         # 7. 绘制主循环
        glfw.poll_events()
        draw()
        glfw.swap_buffers(window)

    glfw.terminate()
