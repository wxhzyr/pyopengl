import glfw
import numpy as np
from OpenGL.GL import *


class OffScreen(object):
    frameBuffer  = None
    outTexture   = None
    depthTexture = None
    def __init__(self, w, h) -> None:
        # Setup framebuffer
        self.frameBuffer = glGenFramebuffers (1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.frameBuffer)

        # Setup depthbuffer
        self.depthTexture = glGenRenderbuffers (1)
        glBindRenderbuffer (GL_RENDERBUFFER, self.depthTexture)
        glRenderbufferStorage (GL_RENDERBUFFER, GL_DEPTH_COMPONENT, w, h)

        # Create texture to render to
        self.outTexture = glGenTextures (1)
        glBindTexture (GL_TEXTURE_2D, self.outTexture)
        glTexParameteri (GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri (GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D (GL_TEXTURE_2D, 0, GL_RGB32F, w, h, 0,GL_RGB, GL_UNSIGNED_BYTE, None)
        glFramebufferTexture2D (GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0,GL_TEXTURE_2D, self.outTexture, 0)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.depthTexture)

        glReadBuffer(GL_NONE)

        glDrawBuffer(GL_COLOR_ATTACHMENT0)

        status = glCheckFramebufferStatus (GL_FRAMEBUFFER)
        if status != GL_FRAMEBUFFER_COMPLETE:
            print("Error in framebuffer activation")
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
    
    def resize(self, w, h):
        glBindFramebuffer(GL_FRAMEBUFFER, self.frameBuffer)
        glBindTexture(GL_TEXTURE_2D, self.outTexture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB32F, w, h,
                    0, GL_RGB, GL_FLOAT, None)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D,
                    self.outTexture, 0)

        glBindTexture(GL_TEXTURE_2D, self.depthTexture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, w, h,
                    0, GL_DEPTH_COMPONENT, GL_FLOAT, None)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D,
                    self.depthTexture, 0)

        glReadBuffer(GL_NONE)

        glDrawBuffer(GL_COLOR_ATTACHMENT0)

        status = glCheckFramebufferStatus (GL_FRAMEBUFFER)
        if status != GL_FRAMEBUFFER_COMPLETE:
            print("FB error")

        glBindTexture(GL_TEXTURE_2D, 0)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        return True

    def enableOffRender(self):
        # 开启离屏渲染
        glBindFramebuffer(GL_DRAW_FRAMEBUFFER, self.frameBuffer)
    
    def disableOffRender(self):
        glBindFramebuffer(GL_DRAW_FRAMEBUFFER, 0)

    def readPixel(self, x, y):
        # 注意这里的x，y并不是直接的鼠标屏幕坐标
        # 传入时应该做转换x = x， y = h - y - 1
        glBindFramebuffer(GL_READ_FRAMEBUFFER, self.frameBuffer)
        glReadBuffer(GL_COLOR_ATTACHMENT0) 
        data = glReadPixels (x, y, 1, 1, GL_RGB,  GL_FLOAT)
        glReadBuffer(GL_NONE)
        glBindFramebuffer(GL_READ_FRAMEBUFFER, 0)
        return data.reshape(1, 3)