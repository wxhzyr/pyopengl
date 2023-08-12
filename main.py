"""最简单的着色器程序"""
import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
from utils.shader import Shader
from utils.camera import Camera
from utils.offScreen import OffScreen
from utils.help import find_closest_vector, custom_distance, readData
import pyrr

# windos参数
width = 1280
height = 720
windowPointer = None
# 绘制数据
vertices = None
colors   = None
indices  = None 
VERTICES = None
COLORS   = None
INDICES  = None 
n = 0
# 设定的预制数据，无需修改
PLANE    = None
PLANEINDICES = vbo.VBO(np.array([0, 1, 3, 1, 2, 3], dtype=np.uint32), target=GL_ELEMENT_ARRAY_BUFFER)
# 着色器程序
drawShader = None 
offRenderShader = None 
# 离屏渲染程序
pickOffScreen = None
posOffScreen  = None
# 摄像头类
myCamera = Camera(pyrr.Vector3([0.0, 0.0, 3.0]))
curPosx = width / 2
curPosy = height / 2
# 计算FPS的参数
delTime = 0.1
curTime = 0.0
# 选中点的index
chooseIndex = -1
# 是否在拖动
isDrag = False

def prepare():
    """准备模型数据"""
    global vertices, VERTICES, colors, COLORS, indices, INDICES, n , drawShader, offRenderShader, pickOffScreen, posOffScreen, PLANE
    vertices, colors, indices = readData(r'resources\data.json')
    n = vertices.shape[0]
    VERTICES = vbo.VBO(vertices)
    COLORS = vbo.VBO(colors)
    INDICES = vbo.VBO(indices, target=GL_ELEMENT_ARRAY_BUFFER)
    # 无需修改
    PLANE = vbo.VBO(np.array([1 , 1 , 0, 1, -1, 0, -1, -1, 0, -1, 1, 0], dtype=np.float32))
    drawShader = Shader(r"shaders/posAndColor.vs", r"shaders/posAndColor.fs")
    offRenderShader = Shader(r"shaders/pickTexture.vs", r"shaders/pickTexture.fs")
    pickOffScreen = OffScreen(width, height)
    posOffScreen  = OffScreen(width, height)

def pickRender():
    # 目前对pick的实现回到了计算坐标上面，不确定在顶点较多时的表现力
    pickOffScreen.enableOffRender()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    offRenderShader.use()
    VERTICES.set_array(vertices)
    offRenderShader.bindDataToShader('aPos', VERTICES)
    # pickShader.bindIndexToShader('vId', INDEX)
    model = pyrr.matrix44.create_identity()
    view  = myCamera.getViewMatrix()
    projection = pyrr.matrix44.create_perspective_projection_matrix(myCamera.zoom, width / height, 0.1, 100)
    offRenderShader.setMatrix4('model', model)
    offRenderShader.setMatrix4('view', view)
    offRenderShader.setMatrix4('projection', projection)
    offRenderShader.setFloat('rate', 1000)
    with INDICES:
        glDrawElements(GL_TRIANGLES, indices.shape[0], GL_UNSIGNED_INT, INDICES) 
    pickOffScreen.disableOffRender()

def posRender():
    global PLANE, PLANEINDICES
    depth = 3.0
    len   = 20000.0
    if chooseIndex > 0 and isDrag:
        direction = vertices[chooseIndex - 1] - np.array(list(myCamera.position))
        front     = np.array(list(myCamera.front))
        front     = front / np.linalg.norm(front)
        depth     = np.dot(direction, front) # 距离该点所在平面的深度
    top_right = myCamera.position + depth * myCamera.front + len / 2 * myCamera.right + len / 2 * myCamera.up
    bottom_right = top_right - len * myCamera.up
    bottom_left = bottom_right - len * myCamera.right
    top_left = top_right - len * myCamera.right
    plane = [   top_right.x,    top_right.y, top_right.z,   
                bottom_right.x, bottom_right.y,bottom_right.z,
                bottom_left.x, bottom_left.y, bottom_left.z,
                top_left.x,     top_left.y,  top_left.z]
    plane = np.array([plane], dtype=np.float32)
    PLANE.set_array(plane)
    posOffScreen.enableOffRender()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    offRenderShader.use()
    offRenderShader.bindDataToShader('aPos', PLANE)
    model = pyrr.matrix44.create_identity()
    view  = myCamera.getViewMatrix()
    projection = pyrr.matrix44.create_perspective_projection_matrix(myCamera.zoom, width / height, 0.1, 100)
    offRenderShader.setMatrix4('model', model)
    offRenderShader.setMatrix4('view', view)
    offRenderShader.setMatrix4('projection', projection)
    offRenderShader.setFloat('rate', 20000)
    with PLANEINDICES:
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, PLANEINDICES)
    posOffScreen.disableOffRender()


def draw():
    """绘制模型"""
    global vertices, delTime, curTime, VERTICES, COLORS
    glEnable(GL_DEPTH_TEST)
    if isDrag and chooseIndex > 0:
        data = posOffScreen.readPixel(curPosx, height - curPosy - 1) * 20000
        data.reshape(1, 3)
        vertices[chooseIndex - 1] = data
        # print(vertices)
    delTime = glutGet(GLUT_ELAPSED_TIME) - curTime
    delTime = delTime / 1000
    curTime = glutGet(GLUT_ELAPSED_TIME) 
    camearUpdate()
    pickRender()
    posRender()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)        # 清除缓冲区
    drawShader.use()
    VERTICES.set_array(vertices)
    COLORS.set_array(colors)
    drawShader.bindDataToShader('a_Position', VERTICES)
    drawShader.bindDataToShader('a_Color', COLORS)
    model = pyrr.matrix44.create_identity()
    view  = myCamera.getViewMatrix()
    projection = pyrr.matrix44.create_perspective_projection_matrix(myCamera.zoom, width / height, 0.1, 100)
    drawShader.setMatrix4('model', model)
    drawShader.setMatrix4('view', view)
    drawShader.setMatrix4('projection', projection)
    with INDICES:
        glDrawElements(GL_TRIANGLES, indices.shape[0], GL_UNSIGNED_INT, INDICES) 
    glfw.set_window_title(windowPointer, f"fps is {round(1 / delTime)}")
    # print(f"fps is {1 / delTime}")
    glUseProgram(0)

def click(window, button, action, mods):
    global chooseIndex, isDrag
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS: 
        data = pickOffScreen.readPixel(curPosx, height - curPosy - 1) * 1000
        v, vId = find_closest_vector(vertices, data)
        chooseIndex = vId + 1
        if custom_distance(v, data) < 0.1:
            # print(f"最近的点为{vId + 1}，点坐标为{v}")
            colors[chooseIndex - 1] = np.array([0.5, 0.5, 0.5], dtype=np.float32)

        isDrag = True
    elif button == glfw.MOUSE_BUTTON_LEFT and action == glfw.RELEASE:
        isDrag = False

def drag(window, x, y):
    """鼠标拖拽事件函数"""

    global curPosx, curPosy, vertices
    myCamera.xOffset, myCamera.yOffset = x - curPosx, curPosy - y
    curPosx = x
    curPosy = y
    if glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
        myCamera.needUpdate = True

def reshape(window, w, h):
    """改变窗口大小事件函数"""

    global width, height    
    width = w
    height = h
    glViewport(0, 0, width, height) # 设置视口
    pickOffScreen.resize(w, h)
    posOffScreen.resize(w, h)

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
        
def updateData():
    # 此处更新数据vertices, colors
    pass

if __name__ == "__main__":
    glfw.init()                                                         # 1. 初始化glfw
    window = glfw.create_window(width, height, "bj_sim_heart", None, None)  # 2. 创建glfwwindow
    windowPointer = window
    glfw.set_window_pos(window, 400, 200)                               # 3. 设置windows窗口位置
    glfw.set_window_size_callback(window, reshape)                      # 4. 提供回调函数
    glfw.set_cursor_pos_callback(window, drag)
    glfw.set_key_callback(window, keyProcess)
    glfw.set_mouse_button_callback(window, click)
    glfw.make_context_current(window)                                   # 5. 将输出绑定到当前windows
    prepare()                                                           # 6. 准备数据
    while not glfw.window_should_close(window):                         # 7. 绘制主循环
        glfw.poll_events()
        updateData()                                                    # 8. 更新数据
        draw()
        glfw.swap_buffers(window)

    glfw.terminate()
