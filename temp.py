
import cv2
import numpy
import time


# 视频图像管理类
class CaptureManager(object):
    # 类变量前加 _ 代表将变量设置保护变量，只有类对象和子类才能访问
    # 类变量前加 __ 代表将变量设置私有变量，只有类对象才能访问
    def __init__(self, capture, previewWindowManager=None, shouldMirrorPreview=False):
        self.previewWindowManager = previewWindowManager
        self.shouldMirrorPreview = shouldMirrorPreview
        self._capture = capture
        self._channel = 0
        self._enteredFrame = False
        self._frame = None
        self._imageFilename = None
        self._videoFilename = None
        self._videoEncoding = None
        self._videoWriter = None
        self._startTime = None
        self._framesElapsed = float(0)
        self._fpsEstimate = None

    # 设置只读属性
    @property
    def channel(self):
        return self._channel

    # 设置可写属性
    @channel.setter
    def channel(self, value):
        if self._channel != value:
            self._channel = value
            self._frame = None

    # 设置只读属性
    @property
    def frame(self):
        if self._enteredFrame and self._frame is None:
            _, self._frame = self._capture.retrieve()
        return self._frame

    # 设置只读属性
    @property
    def isWritingImage(self):
        # return self._imageFilename is not None 首先判断self._imageFilename是否为None，若是，返回False，否则返回True
        # if self._imageFilename:
        #     return True
        # else:
        #     return False
        return self._imageFilename is not None

    # 设置只读属性
    @property
    def isWritingVideo(self):
        return self._videoFilename is not None

    # 启动摄像头录制功能
    def enterFrame(self):
        """Capture the next frame, if any"""
        assert not self._enteredFrame, 'previous enterFrame() had no mathcing exitFrame'
        if self._capture is not None:
            self._enteredFrame = self._capture.grab()

    # 程序里最复杂的就是这方法了，担负了视频显示、视频视频录制、截屏保存的功能。
    def exitFrame(self):
        """Draw to the window. Write to files. Release the frame"""
        if self.frame is None:
            self._enteredFrame = False
            return
        # 计算fps
        if self._framesElapsed == 0:
            self._startTime = time.time()
        else:
            timeElapsed = time.time() - self._startTime
            self._fpsEstimate = self._framesElapsed / timeElapsed

        self._framesElapsed += 1
        # 显示图像
        if self.previewWindowManager is not None:
            if self.shouldMirrorPreview:
                # 向左/右方向翻转阵列，翻转图像
                mirroredFrame = numpy.fliplr(self._frame).copy()
                self.previewWindowManager.show(mirroredFrame)
            else:
                self.previewWindowManager.show(self._frame)

        # 图片文件生成
        if self.isWritingImage:
            cv2.imwrite(self._imageFilename, self._frame)
            self._imageFilename = None

        # 录像生成
        self._writeVideoFrame()

        self._frame = None
        self._enteredFrame = False

    # 设置图片文件名
    def writeImage(self, filename):
        """Wirte the next exited frame to an image file."""
        self._imageFilename = filename

    # 开始录制
    def startWritingVideo(self, filename, encodeing=cv2.VideoWriter_fourcc('I', '4', '2', '0')):
        """Start wirting exited frames to a video file."""
        self._videoFilename = filename
        self._videoEncoding = encodeing

    # 停止录制
    def stopWritingVideo(self):
        """Stop writing eited frames to a video file."""
        self._videoFilename = None
        self._videoEncodding = None
        self._videoWriter = None

    # 录制视频
    def _writeVideoFrame(self):
        if not self.isWritingVideo:
            return
        if self._videoWriter is None:
            fps = self._capture.get(cv2.CAP_PROP_FPS)
            if fps == 0.0:
                if self._framesElapsed < 20:
                    return
                else:
                    fps = self._fpsEstimate
            size = (int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self._videoWriter = cv2.VideoWriter(self._videoFilename, self._videoEncoding, fps, size)
        self._videoWriter.write(self._frame)


# 创建界面管理类
class WindowManager(object):
    def __init__(self, windowName, keypressCallback=None):
        self.keypressCallback = keypressCallback
        self._windowName = windowName
        self._isWindowCreated = False

    # 设置只读属性
    @property
    def isWindowCreated(self):
        return self._isWindowCreated

    # 创建窗口
    def createWindow(self):
        cv2.namedWindow(self._windowName)
        self._isWindowCreated = True

    # 显示窗口
    def show(self, frame):
        cv2.imshow(self._windowName, frame)
        cv2.waitKey(1)

    # 注销窗口
    def destroyWindow(self):
        cv2.destroyWindow(self._windowName)
        self._isWindowCreated = False

    # 执行键盘操作的回调函数
    def processEvents(self):
        keycode = cv2.waitKey(1)
        if self.keypressCallback is not None and keycode != 255:
            # Discard any non-ASCII info encoded by GTK.
            keycode &= 0xFF
            self.keypressCallback(keycode)
