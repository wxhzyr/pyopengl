from pyrr import Vector3, vector, vector3, matrix44
import math
from OpenGL.GL import *
from OpenGL.GLUT import *

class Camera(object):
    # yaw和pitch是欧拉角
    yaw              = -90.0
    pitch            = 0.0
    # 以下三个参数用于调节鼠标交互
    momventSpeed     = 5.0
    mouseSensitivity = 0.05
    zoom             = 45.0
    #  摄像头的向量参数
    position = None
    front    = None
    up       = None
    right    = None
    worldUp  = None
    # 摄像头是否移动的参数
    moveForward = False
    moveBackward = False
    moveLeft = False
    moveRight = False
    moveUp = False
    moveDown = False
    # 摄像头视角偏移所需的参数
    xOffset = 0
    yOffset = 0
    needUpdate = False
    def __init__(self, position = Vector3([0.0, 0.0, 0.0]), up = Vector3([0.0, 1.0, 0.0])) -> None:
        self.position = position
        self.worldUp  = up
        self.updateCameraVectors()

    def updateCameraVectors(self):
        front = Vector3([0.0, 0.0, 0.0])
        front.x = math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        front.y = math.sin(math.radians(self.pitch))
        front.z = math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        self.front = vector.normalise(front)
        self.right = vector.normalise(vector3.cross(self.front, self.worldUp))
        self.up    = vector.normalise(vector3.cross(self.right, self.front))
    
    def getViewMatrix(self):
        return matrix44.create_look_at(self.position, self.position + self.front, self.up)

    def processMouseMovement(self):
        if self.needUpdate:
            self.xOffset *= self.mouseSensitivity
            self.yOffset *= self.mouseSensitivity

            self.yaw += self.xOffset
            self.pitch += self.yOffset

            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0

            self.updateCameraVectors()
        self.needUpdate = False

    # def processMouseMovement(self, xoffset, yoffset):
    #     xoffset *= self.mouseSensitivity
    #     yoffset *= self.mouseSensitivity

    #     self.yaw += xoffset
    #     self.pitch += yoffset

    #     if self.pitch > 89.0:
    #         self.pitch = 89.0
    #     if self.pitch < -89.0:
    #         self.pitch = -89.0

    #     self.updateCameraVectors()
    
    def processKeyMomvement(self, deltaTime):
        velocity = self.momventSpeed * deltaTime
        if self.moveForward:
            self.position = self.position + self.front * velocity
        elif self.moveBackward:
            self.position = self.position - self.front * velocity
        elif self.moveLeft:
            self.position = self.position - self.right * velocity
        elif self.moveRight:
            self.position = self.position + self.right * velocity
        elif self.moveUp:
            self.position = self.position + self.up * velocity
        elif self.moveDown:
             self.position = self.position - self.up * velocity

    def processMouseScroll(self, yoffset):
        self.zoom -= yoffset
        if self.zoom < 1.0:
            self.zoom = 1.0
        if self.zoom > 60.0:
            self.zoom = 60.0
        