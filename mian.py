# -*-coding:utf-8-*-
import cv2
from temp import WindowManager, CaptureManager

class Cameo(object):
    def __init__(self):
        # ����һ�����ڣ��������̵Ļص���������
        self._windowManager = WindowManager('Cameo', self.onKeypress)
        # ���߳���������������ͷ�� ���о���Ч��
        self._captureManager = CaptureManager(capture=cv2.VideoCapture(0), previewWindowManager=self._windowManager,
                                              shouldMirrorPreview=True)

    def run(self):
        """Run the main loop."""
        self._windowManager.createWindow()
        while self._windowManager.isWindowCreated:
            # �����enterFrame���Ǹ��߳��������ͷ��ȡ����
            self._captureManager.enterFrame()
            # ��������frame��ԭʼ֡���ݣ�����û�����κ��޸ģ�����Ľ̳̻�����֡���ݽ����޸�
            frame = self._captureManager._frame
            # exitFrame�������������˳�����˼����ʵ��Ҫ���ܶ��������﷽����ʵ�ֵģ�������¼����������
            self._captureManager.exitFrame()
            # �ص�����
            self._windowManager.processEvents()

    # ������̵Ļص�����������self._windowManager.processEvents()�ĵ���
    def onKeypress(self, keycode):
        '''
        ��ݼ����ã�
        �����¡��ո񡱼���ʱ�򣬻����ץ����
        �����¡�tab������ʱ�򣬾Ϳ�ʼ����ֹͣ¼��
        ��Ȼ��Ӧ��Ŀ¼Ҳ������ͼƬ������Ƶ�ļ�
        '''
        if keycode == 32:  # space
            # ����������ļ�����
            self._captureManager.writeImage('D:\Python27\ChangeOnePixel.png')
        elif keycode == 9:  #tab
            if not self._captureManager.isWritingVideo:
                # ���߳���¼�񱣴���ļ�����
                self._captureManager.startWritingVideo('D:\Python27\Record.avi')
            else:
                self._captureManager.stopWritingVideo()
        elif keycode == 27:  #escape
            self._windowManager.destroyWindow()


if __name__ == "__main__":
    Cameo().run()